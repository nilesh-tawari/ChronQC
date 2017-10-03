# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 17:01:10 2017

@author: tawarinr
"""
from __future__ import absolute_import, division, print_function, with_statement, unicode_literals
import os
import os.path as op
import sys
import time
import logging
import numpy as np
import pandas as pd
import sqlite3
import json
try:
    from . import utils
except (ValueError, SystemError, ImportError):
    import utils
    
try:
    import configparser
    Config = configparser.ConfigParser()  # ver. < 3.0
except:
    import ConfigParser
    Config = ConfigParser.ConfigParser()


def updir(path, n):
    """
    (str) -> int
    From the path return nth upper dir
    """
    folders = []
    while 1:
        path, folder = op.split(path)
        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)
            break
    folders.reverse()
    return folders[-n]


def creation_date(path_to_file):
    """
    (str) -> time
    Given path of the file return last modified time of file else np.nan
    str -> time
    """
    try:
        file_time = op.getmtime(path_to_file)
        return time.strftime("%m/%d/%Y", time.localtime(file_time))
    except:
        return np.nan


###############################################################################


def main(args):
    """
    (args) -> SQLitedb
    takes number of arguments and produces ChronQC SQLite database
    """
    if args.mode == 'update' and not args.db:
        print("can't update database {} without a -db argument".format(args.mode))
    elif args.mode == 'update' and args.prefix:
        print("can't use prefix in update mode so ignoring it")
    elif args.mode == 'create' and not args.output:
        print("provide output directory --output argument for creating db".format(args.mode))

# output dir and file
    # Get output directory 1. user defined 2. db dir 3. multiqc_stats dir
    # Get output file name prefix and out file name
    multiqc_stats = op.abspath(args.mstats)
    if args.db is not None:
        output_directory, output_prefix = utils.path_leaf(args.db)
        out_file = op.abspath(args.db)
    else:
        output_directory = op.abspath(args.output)
        output_directory = op.join(output_directory, "chronqc_db")
        if op.exists(output_directory) and not args.force:
            print("FATAL: Output directory {0} already exists, use -f to overwrite".format(output_directory))
            sys.exit(1)
        elif op.exists(output_directory) and args.force:
            pass
        if not op.exists(output_directory):
            os.makedirs(output_directory)
        output_prefix = '{0}.{1}'.format(args.prefix, 'chronqc.stats.sqlite') if args.prefix is not None else '{0}'.format('chronqc.stats.sqlite')
        out_file = op.join(output_directory, output_prefix)
        output_cols = '{0}.{1}'.format(args.prefix, 'chronqc.stats.cols.txt') if args.prefix is not None else '{0}'.format('chronqc.stats.cols.txt')
        out_cols = op.join(output_directory, output_cols)
        output_json = '{0}.{1}'.format(args.prefix, 'chronqc.default.json') if args.prefix is not None else '{0}'.format('chronqc.default.json')
        out_json = op.join(output_directory, output_json)

# create logger
    log_file = op.join(output_directory, 'chronqc_stats.log')
    logging.basicConfig(filename=log_file,
                        format='%(asctime)s - %(name)s - %(levelname)s \
                        - %(message)s')
    logger = logging.getLogger('chronqc')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.CRITICAL)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -'
                                  '%(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.info("Started ChronQC {} SQLite db generation".format(out_file))

# Get parameters
    table_name = args.db_table
    table_name = table_name if table_name is not None else 'chronqc_stats_data'
    panel = args.panel
    if args.run_dir_level is not None:
        run_dir_level = int(args.run_dir_level)
    logger.info("Got required parameters for generating ChronQC SQLite db")
    utils.print_progress(1, 4, prefix='Running ChronQC', decimals=1, bar_length=50)
# Get run id and date info
    if args.run_date_info is not None:
        run_date_info = op.abspath(args.run_date_info)
        df_run = pd.read_csv(run_date_info, comment='#', chunksize=1000,
                             low_memory=False, iterator=True)
        df_run = pd.concat(list(df_run), ignore_index=True)
        logger.info("Generated run and date information from {0}".format(run_date_info))
    else:
        multiqc_sources = op.abspath(args.multiqc_sources)
        df_run = pd.read_csv(multiqc_sources, sep='\t', comment='#',
                             chunksize=1000, low_memory=False, iterator=True)
        df_run = pd.concat(list(df_run), ignore_index=True)
        df_run.rename(columns={'Sample Name': 'Sample'}, inplace=True)
        df_run_m = df_run.loc[df_run.Module.str.contains(args.module)]
        # stick to defined module (FASTQC)
        df_run = df_run_m.copy() if len(df_run_m) > 0 else df_run.copy()
        # Get date and run
        df_run['Source_path'] = df_run['Source'].apply(op.abspath)
        df_run['Date'] = df_run['Source_path'].apply(creation_date)
        multiqc_sources_time = time.localtime(op.getmtime(multiqc_sources))
        multiqc_sources_time = time.strftime("%m/%d/%Y", multiqc_sources_time)
        df_run['Date'].fillna(multiqc_sources_time, inplace=True)
        df_run['Run'] = df_run.apply(lambda row: updir(row['Source_path'], run_dir_level), axis=1)
        logger.info("Generated run and date information from {0}".format(multiqc_sources))
    df_run['Date'] = pd.to_datetime(df_run.Date, dayfirst=True)
    df_run.sort_values(by=['Date'], inplace=True)
    df_run.drop_duplicates(subset=['Sample'], inplace=True)
    if len(df_run) == 0:
        logger.critical("FATAL: For run and date information no records found")
        sys.exit(1)
    utils.print_progress(2, 4, prefix='Running ChronQC', decimals=1, bar_length=50)
# Read multiqc_stats
    df = pd.read_csv(multiqc_stats, sep='\t', comment='#', chunksize=1000,
                     low_memory=False, iterator=True)
    df = pd.concat(list(df), ignore_index=True)
    logger.info("Got {0} records from {1} for ChronQC SQLite db generation".format(len(df), multiqc_stats))
    if len(df) == 0:
        logger.critical("FATAL: No records found in {0}".format(multiqc_stats))
        sys.exit(1)
    utils.print_progress(3, 4, prefix='Running ChronQC', decimals=1, bar_length=50)

# Read config and get default parameters
    #sdir = op.dirname(op.abspath('__file__'))
    sdir = op.abspath(op.join(op.dirname(__file__), 'config'))
    config_file = op.join(sdir, 'chronqc.conf')
    Config.read(config_file)
    # [ignore_columns]
    ignore_columns = Config.get('ignore_columns', 'columns').split(',')
    ignore_columns = [s.strip() for s in ignore_columns]
    # [time_series_with_box_whisker_plot]
    box_whisker_plot = Config.get('time_series_with_box_whisker_plot', 'columns').split(',')
    box_whisker_plot = [s.strip() for s in box_whisker_plot]
    # [time_series_with_mean_and_stdev]
    mean_and_stdev = Config.get('time_series_with_mean_and_stdev', 'columns').split(',')
    mean_and_stdev = [s.strip() for s in mean_and_stdev]
    # [time_series_with_absolute_threshold]
    absolute_threshold_c = Config.get('time_series_with_absolute_threshold', 'columns').split(',')
    absolute_threshold_c = [s.strip() for s in absolute_threshold_c]
#    absolute_threshold = Config.get('time_series_with_absolute_threshold', 'threshods').split(',')
#    absolute_threshold = [int(s.strip()) for s in absolute_threshold]
    # [time_series_with_percentage_of_samples_above_threshold]
    percentage_of_samples_above_threshold_c = Config.get('time_series_with_percentage_of_samples_above_threshold', 'columns').split(',')
    percentage_of_samples_above_threshold_c = [s.strip() for s in percentage_of_samples_above_threshold_c]
#    percentage_of_samples_above_threshold = Config.get('time_series_with_percentage_of_samples_above_threshold', 'threshods').split(',')
#    percentage_of_samples_above_threshold = [int(s.strip()) for s in percentage_of_samples_above_threshold]
    # [time_series_with_percentage_category]
    percentage_category_c = Config.get('time_series_with_percentage_category', 'columns').split(',')
    percentage_category_c = [s.strip() for s in percentage_category_c]
#    percentage_category = Config.get('time_series_with_percentage_category', 'categories').split(',')
#    percentage_category = [s.strip() for s in percentage_category]
    logger.info("Finished reading parameters from config file for generating \
                chronqc db and json")

# remove unwanted columns
    cols = [col for col in list(df.columns)]
    cols = ['Sample'] + sorted(cols[1:])
    df = pd.DataFrame(df, columns=cols)

# process df for adding in to chronqc db
    # Add panel
    df['Panel'] = panel
    # Add run and date information
    df = pd.merge(df_run, df, left_on='Sample', right_on='Sample', how='inner')
    if len(df) == 0:
        logger.critical("FATAL: Run ID's do not match the sample information in {0}".format(multiqc_stats))
        sys.exit(1)
    df['Date'] = pd.to_datetime(df.Date, dayfirst=True)
    # remove blank spaces in column names
    df.columns = [x.strip().replace(' ', '_') for x in df.columns]
    logger.info("Kept {0} records after merging run, date and stats for ChronQC SQLite db".format(len(df)))
# convert boolean types This method will not work for object type column
#    booleandf = df.select_dtypes(include=[bool])
#    booleanDictionary = {True: 'TRUE', False: 'FALSE'}
#    for column in booleandf:
#        df[column] = df[column].map(booleanDictionary)        
    df.replace(to_replace=True, value='TRUE', inplace=True)
    df.replace(to_replace=False, value='FALSE', inplace=True)
# write db
    cnx = sqlite3.connect(out_file)
    if args.mode == 'create':
        df.to_sql(table_name, cnx, index=False, if_exists='replace', chunksize = 1000)
        out_cols = open(out_cols, 'w')
        for item in list(df.columns):
            out_cols.write("%s\n" % item)
        out_cols.close()
        # create default JSON file
        # only numeric columns
        df_num = df._get_numeric_data()
        num_cols = list(df_num)
        #############################################################
        default_json = []
        # absolute_threshold
        absolute_threshold_c = [c for c in absolute_threshold_c if c not in ignore_columns]
        absolute_threshold_c = [c for c in absolute_threshold_c if c in num_cols]
        abst = '{{"table_name": "{0}", "chart_type": "time_series_with_absolute_threshold", "chart_properties": {{"y_value": "{1}",  "lower_threshold": 30}}}}'
        for col in absolute_threshold_c:
            default_json.append(json.loads(abst.format(table_name, col)))  
        # percentage_of_samples_above_threshold
        percentage_of_samples_above_threshold_c = [c for c in percentage_of_samples_above_threshold_c if c not in ignore_columns]
        percentage_of_samples_above_threshold_c = [c for c in percentage_of_samples_above_threshold_c if c in num_cols]
        pctth = '{{"table_name": "{0}", "chart_type": "time_series_with_percentage_of_samples_above_threshold", "chart_properties": {{"y_value": "{1}",  "threshold": 30}}}}'
        for col in percentage_of_samples_above_threshold_c:
            default_json.append(json.loads(pctth.format(table_name, col)))  
        # percentage_category
        percentage_category_c = [c for c in percentage_category_c if c not in ignore_columns]
        percentage_category_c = [c for c in percentage_category_c if c in num_cols]
        pctcat = '{{"table_name": "{0}", "chart_type": "time_series_with_percentage_category", "chart_properties": {{"y_value": "{1}",  "category": "TRUE"}}}}'
        for col in percentage_category_c:
            default_json.append(json.loads(pctcat.format(table_name, col))) 
        # mean_and_stdev
        mean_and_stdev = [c for c in mean_and_stdev if c not in ignore_columns]
        mean_and_stdev = [c for c in mean_and_stdev if c in num_cols]
        if 'QualiMap_percentage_aligned' and 'Bamtools_mapped_reads_pct' in mean_and_stdev:
            mean_and_stdev.remove('Bamtools_mapped_reads_pct')
        if 'FastQC_percent_gc' and 'QualiMap_avg_gc' in mean_and_stdev:
            mean_and_stdev.remove('QualiMap_avg_gc')
        if 'QualiMap_mapped_reads' and 'Samtools_Flagstat_mapped_passed' in mean_and_stdev:
            mean_and_stdev.remove('Samtools_Flagstat_mapped_passed')
        if 'FastQC_total_sequences' and 'QualiMap_total_reads' in mean_and_stdev:
            mean_and_stdev.remove('QualiMap_total_reads')            
        mstd = '{{"table_name": "{0}", "chart_type": "time_series_with_mean_and_stdev", "chart_properties": {{"y_value": "{1}"}}}}'
        for col in mean_and_stdev:
            default_json.append(json.loads(mstd.format(table_name, col)))  
        # box_whisker_plot
        box_whisker_plot = [c for c in box_whisker_plot if c not in ignore_columns]
        box_whisker_plot = [c for c in box_whisker_plot if c in num_cols]
        bwp = '{{"table_name": "{0}", "chart_type": "time_series_with_box_whisker_plot", "chart_properties": {{"y_value": "{1}"}}}}'
        for col in box_whisker_plot:
            default_json.append(json.loads(bwp.format(table_name, col)))  
        # remaining cols 
        
        num_cols = [c for c in num_cols if c not in ignore_columns]
        num_cols = [c for c in num_cols if c not in box_whisker_plot]
        num_cols = [c for c in num_cols if c not in mean_and_stdev]
        num_cols = [c for c in num_cols if c not in absolute_threshold_c]
        num_cols = [c for c in num_cols if c not in percentage_of_samples_above_threshold_c]
        num_cols = [c for c in num_cols if c not in percentage_category_c]
        if len(num_cols) > 0:
            for col in num_cols:
                default_json.append(json.loads(mstd.format(table_name, col)))  
        with open(out_json, 'w') as out_json_file:
            json.dump(default_json, out_json_file, sort_keys = False, indent = 4,
               ensure_ascii = False) 
        logger.info("Created ChronQC db: {0} with {1} records".format(out_file, len(df)))
        logger.info("Created ChronQC default JSON file: {0}. Customize the JSON as needed before generating ChronQC plots.".format(out_json))
    elif args.mode == 'update':
        df.to_sql(table_name, cnx, index=False, if_exists='append', chunksize = 1000)
        logger.info("Updated ChronQC db: {0} with {1} records".format(out_file, len(df)))
    cnx.close()
    utils.print_progress(4, 4, prefix='Running ChronQC', decimals=1, bar_length=50)
    if args.mode == 'create':
        print("Created ChronQC db: {0} with {1} records".format(out_file, len(df)))
        print("Created ChronQC default JSON file: {0}. Customize the JSON as needed before generating ChronQC plots.".format(out_json))
    elif args.mode == 'update':
        print("Updated ChronQC db: {0} with {1} records".format(out_file, len(df)))
