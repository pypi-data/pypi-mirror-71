"""
The entry point to running permutation-based statistics.


Usage
-----

run_permutation_stats.run(test_data/registration_test_data/baseline,
                        data/registration_test_data/mutant,
                        test_data/stats_test_data/test_output,
                        1000)


Currently, this module works only with organ volume data. The voxel-based methods are currently too big to do this.
Think about including voxel-based stats in the future

Outline of pipeline
-------------------
Before running the permutation statistics we need to have run jobrunner.py on the baseline and mutant data.

The main function in this module run() calles the following functions during the pipeline:

get_organ_volume_data and get_staging_data
    search the registration output folders for the CSVs that contain the organ volumes
    and staging data and collate into single csvs.


distributions.null and distributions.alternative
    Use the dataframes from the precedding functions to generate null and alternative p-value distributiuon dataframes

p_thresholds.get_thresholds
    Using the null and alternative distributions, these functions generate organ-spceific p-value thresholds.
    These are generated for both line-level and specimen level calls.

annotate
    This function creates final results CSVs.
        Puts a line-level csv in the line/output/stats_/
        Puts specimen-level csv files in line/output/stats_/specimen_level

"""

from pathlib import Path
from datetime import date

import pandas as pd
import numpy as np
from logzero import logger as logging
import yaml

from lama import common
from lama.stats.permutation_stats import distributions
from lama.stats.permutation_stats import p_thresholds
from lama.paths import specimen_iterator
from lama.qc.organ_vol_plots import make_plots, pvalue_dist_plots
from lama.common import write_array, read_array, init_logging



GENOTYPE_P_COL_NAME = 'genotype_effect_p_value'
PERM_SIGNIFICANT_COL_NAME = 'significant_cal_p'


def get_organ_volume_data(root_dir: Path) -> pd.DataFrame:
    """
    Given a root registration directory, collate all the organ volume CSVs into one file.
    Write out the combined organ volume CSV into the root registration directory.

    Parameters
    ----------
    root_dir
        The path to the root registration directory

    Returns
    -------
    The combined data frame of all the organ volumes
    specimen id in index organs in rows
    """
    output_dir = root_dir / 'output'

    dataframes = []

    for line_dir, specimen_dir in specimen_iterator(output_dir):

        organ_vol_file = specimen_dir / 'output' / common.ORGAN_VOLUME_CSV_FILE

        if not organ_vol_file.is_file():
            raise FileNotFoundError(f'Cannot find organ volume file {organ_vol_file}')

        df = pd.read_csv(organ_vol_file, index_col=0)

        if len(df) == 0:
            raise ValueError(f'{organ_vol_file} is empty')

        dataframes.append(df)

    # Write the concatenated organ vol file to single csv
    all_organs = pd.concat(dataframes)

    # outpath = output_dir / common.ORGAN_VOLUME_CSV_FILE
    # all_organs.to_csv(outpath)

    return all_organs


def get_staging_data(root_dir: Path) -> pd.DataFrame:
    """
    Given a root registration directory, collate all the staging CSVs into one file.
    Write out the combined organ volume CSV into the root registration directory.

    Parameters
    ----------
    root_dir
        The path to the root registration directory

    Returns
    -------
    The combined dataframe of all the organ volumes
    """
    output_dir = root_dir / 'output'

    dataframes = []

    for line_dir, specimen_dir in specimen_iterator(output_dir):

        staging_info = specimen_dir / 'output' / common.STAGING_INFO_FILENAME

        if not staging_info.is_file():
            raise FileNotFoundError(f'Cannot find staging info file {staging_info}')

        df = pd.read_csv(staging_info, index_col=0)
        df['line'] = line_dir.name
        dataframes.append(df)

    # Write the concatenated staging info to the
    all_staging = pd.concat(dataframes)
    outpath = output_dir / common.STAGING_INFO_FILENAME
    all_staging.to_csv(outpath)

    return all_staging


def annotate(thresholds: pd.DataFrame, lm_results: pd.DataFrame, lines_root_dir: Path, line_level: bool = True,
             label_info: Path = None, label_map: Path = None, write_thresholded_inv_labels=False,
             fdr_threshold: float=0.05):
    """
    Using the p_value thresholds and the linear model p-value results,
    create the following CSV files

        Line-level results
        specimen-level results

    Parameters
    ----------
    thresholds
        columns label(index), p_thresh, fdr, num_hits_across_all_lines/specimens
    lm_results
        The alternative distribution
        index: line/specimen id
        cols: labels (+ line_id for specimen_level)
    outdir
        The root directory to save the annotated CSV files
    line_level
        if not True, place results in specimen-level sub directory
    label_info
        CSV to map label number to name

    Notes
    -----
    Today's date added to the stats output folder in case it's run multiple times,
    TODO: Add file number prefixes so we don't overwrite mulyiple analyses done on the same day
    TODO: the organ_volumes folder name is hard-coded. What about if we add a new analysis type to the  permutation stats pipeline?
    """
    collated = []

    if label_map:
        label_map = read_array(label_map)

    for id_, row in lm_results.iterrows():

        # Create a dataframe containing p-value column. each organ on rows
        df = row.to_frame()

        if not line_level:
            # specimne-level has an extra line column we need to remove
            df = df.T.drop(columns=['line']).T

        # Rename the line_specimen column to be more informative
        df.rename(columns={id_: GENOTYPE_P_COL_NAME}, inplace=True)

        if line_level:
            line = id_
        else:
            line = row['line']

        # Merge the permutation results (p-thresh, fdr, number of hit lines fo this label) with the mutant results
        df.index = df.index.astype(np.int64)  # Index needs to be cast from object to enable merge
        df = df.merge(thresholds, left_index=True, right_index=True, validate='1:1')
        df.index.name = 'label'

        output_name = f'{id_}_organ_volumes_{str(date.today())}.csv'

        line_output_dir = lines_root_dir / line
        line_output_dir.mkdir(exist_ok=True)

        if not line_level:
            # If dealing with specimen-level stats, make subfolder to put results in
            line_output_dir = line_output_dir / 'specimen_level' / id_
            line_output_dir.mkdir(parents=True, exist_ok=True)

        output_path = line_output_dir / output_name

        add_significance(df, fdr_threshold)

        if label_info:
            df = add_label_names(df , label_info)

        df.to_csv(output_path)

        hit_df = df[df['significant_cal_p'] == True]
        collated.append(hit_df)

        hit_labels_out = line_output_dir / f'{line}__hit_labels.nrrd'

        hits = hit_df.index

        if write_thresholded_inv_labels:
            _write_thresholded_label_map(label_map, hits, hit_labels_out)
    return collated



def _write_thresholded_label_map(label_map: np.ndarray, hits, out: Path):
    """
    Write a label map with only the 'hit' organs in it
    """
    if label_map is None:
        return

    if len(hits) > 0:
        # Make a copy as it may be being used elsewhere
        l = np.copy(label_map)
        # Clear any non-hits
        l[~np.isin(l, hits)] = 0

        write_array(l, out)


def add_label_names(df: pd.DataFrame, label_info: Path) -> pd.DataFrame:

    label_df = pd.read_csv(label_info, index_col=0)

    df = df.merge(right=label_df[['label_name']], left_index=True, right_index=True)

    return df


def add_significance(df: pd.DataFrame, threshold: float):
    """
    Add a significance column to the output csv in place.
    Set significance to True if the genotype p-value is lower than the p threshold for that organ
    and the fdr is lower than fdr threshold.
    And sort values by significance
    """
    df[PERM_SIGNIFICANT_COL_NAME] = (df[GENOTYPE_P_COL_NAME] <= df['p_thresh']) & (df['fdr'] <= threshold)

    df.sort_values(by=[PERM_SIGNIFICANT_COL_NAME, GENOTYPE_P_COL_NAME], ascending=[False, True], inplace=True)


def prepare_data(wt_organ_vol: pd.DataFrame,
                 wt_staging: pd.DataFrame,
                 mut_organ_vol: pd.DataFrame,
                 mut_staging: pd.DataFrame,
                 label_meta: Path = None,
                 normalise_to_whole_embryo=False) -> pd.DataFrame:
    """
    Do some pre-processing on the input DataFrames and concatenate into one data frame.
    Normalise organ volumes by whole embryo volume (staging)


    Returns
    -------
    Concatenated data with line, genotype staging + organ volume columns

    """

    wt_staging.rename(columns={'value': 'staging'}, inplace=True)
    mut_staging.rename(columns={'value': 'staging'}, inplace=True)
    wt_staging.index = wt_staging.index.astype(str)

    if normalise_to_whole_embryo:
        wt_organ_vol = wt_organ_vol.divide(wt_staging['staging'], axis=0)
        mut_organ_vol = mut_organ_vol.divide(mut_staging['staging'], axis=0)
        logging.info('Normalising organ volume to whole embryo volume')

    # merge the organ vol
    organ_vols = pd.concat([wt_organ_vol, mut_organ_vol])

    # Drop any organ columns that has only zero values. These are the gaps in the label map caused by merging labels
    organ_vols = organ_vols.loc[:, (organ_vols != 0).any(axis=0)]

    # For the statsmodels linear mode to work, column names cannot start with a digid. Prefix with 'x'
    organ_vols.columns = [f'x{x}' if x.isdigit() else x for x in organ_vols.columns]


    staging = pd.concat([wt_staging, mut_staging])

    # Merge staging to the organvolume dataframe. First drop line so we don't get duplicate entries
    # staging.drop(columns=['line'], inplace=True)

    data = pd.concat([organ_vols, staging], axis=1)

    # Filter any flagged labels
    if label_meta:

        label_meta = pd.read_csv(label_meta, index_col=0)

        if 'no_analysis' in label_meta:  # If we have a no_analysis column, drop labels that are flagged
            flagged_lables = label_meta[label_meta.no_analysis == True].index
            data.drop(columns=[f'x{x}' for x in flagged_lables if f'x{x}' in data] , inplace=True)

    return data


def run(wt_dir: Path, mut_dir: Path, out_dir: Path, num_perms: int,
        label_info: Path = None, label_map_path: Path = None, line_fdr: float=0.05, specimen_fdr: float=0.2,
        normalise_to_whole_embryo:bool=True):
    """
    Run the permutation-based stats pipeline

    Parameters
    ----------
    wt_dir
        Root of the wild type registration output
        This should contain an 'output' folder that contains a single baseline folder that contains multiple specimen folders
    mut_dir
        Root of the mutant registration output
        This should contain 'output' folder that contains multiple mutant lines folder, each containing one or more mutant specimen folders
    out_dir
        Where to store the intermediate results of the permutation testing
    num_perms
        number of permutations to do
    log_dependent
        if True, apply numpy.log to all the dependent values (organ volumes)
    label_info
        if supplied, use it to annotate the results with label names. Also can be used to filter certain labels from the
        analysis using the 'no_analysis' column
    line_fdr
        the FDR threshold at which to accept line level calls
    specimen_fdr
        the FDR threshold at which to accept specimen-level calls
    normalise_to_whole_embryo:
        Whether to divide the organ each organ volume by whole embryo volume
    """
    # Collate all the staging and organ volume data into csvs
    np.random.seed(999)
    init_logging(out_dir / 'stats.log')
    logging.info(common.git_log())
    logging.info(f'Running {__name__} with followng commands\n{common.command_line_agrs()}')

    wt_staging = get_staging_data(wt_dir)
    mut_staging = get_staging_data(mut_dir)

    wt_organ_vol = get_organ_volume_data(wt_dir)
    mut_organ_vol = get_organ_volume_data(mut_dir)

    data = prepare_data(wt_organ_vol,
                        wt_staging,
                        mut_organ_vol,
                        mut_staging,
                        label_meta=label_info,
                        normalise_to_whole_embryo=normalise_to_whole_embryo)

    # Keep a record of the input data used in the analsysis
    data.to_csv(out_dir / 'input_data.csv')

    # Keep raw data for plotting
    raw_wt_vols = wt_organ_vol.copy()

    out_dir.mkdir(exist_ok=True, parents=True)  # Root directory for output

    # make directory to store distributions and thresholds
    dists_out = out_dir / 'distributions'
    dists_out.mkdir(exist_ok=True)

    # Get the null distributions
    line_null, specimen_null, null_ids = distributions.null(data, num_perms)

    with open(dists_out / 'null_ids.yaml', 'w') as fh:
        yaml.dump(null_ids, fh)

    null_line_pvals_file = dists_out / 'null_line_dist_pvalues.csv'
    null_specimen_pvals_file = dists_out / 'null_specimen_dist_pvalues.csv'

    # Write the null distributions to file
    line_null.to_csv(null_line_pvals_file)
    specimen_null.to_csv(null_specimen_pvals_file)

    # Get the alternative distribution
    line_alt, spec_alt = distributions.alternative(data)

    line_alt_pvals_file = dists_out / 'alt_line_dist_pvalues.csv'
    spec_alt_pvals_file = dists_out / 'alt_specimen_dist_pvalues.csv'

    # Write the alternative distributions to file
    line_alt.to_csv(line_alt_pvals_file)
    spec_alt.to_csv(spec_alt_pvals_file)

    line_organ_thresholds = p_thresholds.get_thresholds(line_null, line_alt)
    specimen_organ_thresholds = p_thresholds.get_thresholds(specimen_null, spec_alt)

    line_thresholds_path = dists_out / 'line_organ_p_thresholds.csv'
    spec_thresholds_path = dists_out / 'specimen_organ_p_thresholds.csv'

    line_organ_thresholds.to_csv(line_thresholds_path)
    specimen_organ_thresholds.to_csv(spec_thresholds_path)

    logging.info('Annotating lines')

    lines_root_dir = out_dir / 'lines'
    lines_root_dir.mkdir(exist_ok=True)

    # Annotate lines
    logging.info(f"Annotating lines, using a FDR threshold of {line_fdr}")
    annotate(line_organ_thresholds, line_alt, lines_root_dir, label_info=label_info,
             label_map=label_map_path, write_thresholded_inv_labels=True,fdr_threshold=line_fdr)

    # Annotate specimens
    logging.info(f"Annotating specimens, using a FDR threshold of {specimen_fdr}")
    annotate(specimen_organ_thresholds, spec_alt, lines_root_dir, line_level=False,
             label_info=label_info, label_map=label_map_path, fdr_threshold=specimen_fdr)

    mut_dir_ = mut_dir / 'output'
    make_plots(mut_dir_, raw_wt_vols, wt_staging, label_info, lines_root_dir)

    dist_plot_root = out_dir / 'distribution_plots'
    line_plot_dir = dist_plot_root / 'line_level'
    line_plot_dir.mkdir(parents=True, exist_ok=True)
    pvalue_dist_plots(line_null, line_alt, line_organ_thresholds, line_plot_dir)

    specimen_plot_dir = dist_plot_root / 'specimen_level'
    specimen_plot_dir.mkdir(parents=True, exist_ok=True)
    pvalue_dist_plots(specimen_null, spec_alt.drop(columns=['line']), specimen_organ_thresholds, specimen_plot_dir)








