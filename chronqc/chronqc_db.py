# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 17:01:10 2017

@author: tawarinr
"""
from __future__ import absolute_import, division, print_function, with_statement, unicode_literals
from . import utils
import os
import os.path as op
import sys
import time
import logging
import numpy as np
import pandas as pd
import sqlite3
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
    except FileNotFoundError:
        return np.nan


###############################################################################


def main(args):
    """
    (args) -> SQLitedb
    takes number of arguments and produces ChronQC SQLite database
    """
    if args.mode == 'update' and not args.db:
        parser.error("can't update database {} without a -db argument".format(args.mode))
    elif args.mode == 'update' and args.prefix:
        print("can't use prefix in update mode so ignoring it")
    elif args.mode == 'create' and not args.output:
        parser.error("provide output directory --output argument for creating db".format(args.mode))

# output dir and file
    # Get output directory 1. user defined 2. db dir 3. multiqc_stats dir
    # Get output file name prefix and out file name
    multiqc_stats = op.abspath(args.multiqc_stats)
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
#    sdir = op.dirname(op.abspath('__file__'))
#    config_file = op.join(sdir, 'config', 'chronqc.conf')
#    Config.read(config_file)
    # [ignore_columns]
#    ignore_columns = Config.get('ignore_columns', 'columns').split(',')
#    ignore_columns = [s.strip() for s in ignore_columns]
#    logger.info("Finished reading parameters from config file for generating \
#                chronqc db and json")

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
# write db
    cnx = sqlite3.connect(out_file)
    if args.mode == 'create':
        df.to_sql(table_name, cnx, index=False, if_exists='replace', chunksize = 1000)
        out_cols = open(out_cols, 'w')
        for item in list(df.columns):
            out_cols.write("%s\n" % item)
        out_cols.close()
        logger.info("Created ChronQC db: {0} with {1} records".format(out_file, len(df)))
    elif args.mode == 'update':
        df.to_sql(table_name, cnx, index=False, if_exists='append', chunksize = 1000)
        logger.info("Updated ChronQC db: {0} with {1} records".format(out_file, len(df)))
    cnx.close()
    utils.print_progress(4, 4, prefix='Running ChronQC', decimals=1, bar_length=50)
    if args.mode == 'create':
        print("Created ChronQC db: {0} with {1} records".format(out_file, len(df)))
    elif args.mode == 'update':
        print("Updated ChronQC db: {0} with {1} records".format(out_file, len(df)))
