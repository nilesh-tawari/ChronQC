# -*- coding: utf-8 -*-
"""
Created on Tue May 30 13:26:30 2017

@author: tawarinr
"""
from __future__ import absolute_import, division, print_function, with_statement, unicode_literals
import os
import sys
import os.path as op
import string
import logging
import pandas as pd
#from pandas.tseries.offsets import MonthEnd
import numpy as np
import sqlite3
import json
from datetime import date
from dateutil.relativedelta import relativedelta
import warnings
import io
try:
    from . import utils
except (ValueError, SystemError, ImportError):
    import utils
warnings.simplefilter(action="ignore", category=RuntimeWarning)


def add_dates(df, Date='Date'):
    """
    (df) -> df
    add dates with dumy values at the begning (previous month)
    and end of dataframe (next month than today)
    """
    df.sort_values(by=[Date], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.index = df.index + 1
    df.loc[0, Date] = df.loc[1, Date] + relativedelta(months=-1)
#    next_month = date.today() + relativedelta(months=+1)
    next_month = df.loc[len(df.index)-1, Date] + relativedelta(months=+1)
    df.loc[len(df.index), Date] = next_month
    df = df.sort_index()
    df.sort_values(by=[Date], inplace=True)
    return df


def format_date_names(df, Date='Date'):
    """
    (df) -> df
    Format date (as string) and name (as list) column for writing to html
    """
    df[Date] = df[Date].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['names'] = ''
    df['Run'] = df[['Run', 'names']].values.tolist()
    del df['names']
    return df

def fetch_stats_data(db, table_name, panel, categories='', ColumnName=''):
    """
    (file) -> df
    From sqlite database pull data based on user input
    """
    connection = sqlite3.connect(db)
    mycursor = connection.cursor()
    if categories != '':
        categories = list(set([s.strip() for s in categories.split(',')]))
        if len(categories) > 10:
            print("FATAL: More than 10 categories specified for Bar plot, only 10 categories can be plotted in a single Bar plot")
            sys.exit(1)
        category_que = '{0} LIKE'.format(ColumnName)
        category_str = ' "{0}" OR {1} LIKE '
        i = 0
        while i < len(categories)-1:
            category_que = category_que + category_str.format(categories[i], ColumnName)
            i = i + 1
        if i == len(categories)-1:
            category_que = category_que + ' "{0}" '.format(categories[i])
        #print('select * from {0} WHERE (Panel = "{1}") and ({2})'.format(table_name, panel, category_que))
        curr = mycursor.execute('select * from {0} WHERE (Panel = "{1}") and ({2})'.format(table_name, panel, category_que))
    else:
        curr = mycursor.execute('select * from {0} WHERE Panel = "{1}"'.format(table_name, panel))
    anndata = curr.fetchall()
    df = pd.DataFrame(anndata)
    df.columns = [c[0] for c in curr.description]
    df['First_Date'] = pd.to_datetime(df.Date, dayfirst=True).map(lambda x: x.replace(day=1))
    df['Date'] = pd.to_datetime(df.Date, dayfirst=True)
    #df['First_Date'] = pd.to_datetime(df['Date'], format="%Y%m") + MonthEnd(1)
    curr.close()
    return df


def get_samples_data(df, include_samples='all', exclude_samples='', per_sample='False'):
    """
    (df) -> df
    keep only desired samples data from the fetched data
    """
    if per_sample == 'True':
        if 'Run' not in df.columns:
            df['Run'] = df['Sample']
        if 'Sample' not in df.columns:
            df['Sample'] = df['Run']
    df['Sample'].fillna('-', inplace=True)
    if include_samples != 'all':
        include_samples = [s.strip() for s in include_samples.split(',')]
        df = df[df.Sample.str.contains('|'.join(include_samples))]
    if exclude_samples != '':
        exclude_samples = [s.strip() for s in exclude_samples.split(',')]
        df = df[~df.Sample.str.contains('|'.join(exclude_samples))]
    df = pd.DataFrame(df)
    df.sort_values(by=['Date'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def format_sample_names(df, column):
    """
    (df) -> df
    format sample_names as sample name (column)
    """
    df_names = df.copy()
    df_names['Sample'] = df_names[['Sample', column]].apply(lambda x: '{} ({})'.format(x[0], x[1]), axis=1)
    df_names = df_names.groupby(['Run', 'Date'])['Sample'].agg(lambda x: ', '.join(x)).reset_index()
    return df_names


def percentage_category(df, column, cat='PASS'):
    """
    get data for VCS pass percentage
    1. Count values of % cat in a run
    2. Add sample names and run names
    3. Add dumy dates at start and end, format data for html
    df -> df
    """
    # 1. Get data
    df[column] = df[column].str.upper()
    df_copy = df.copy()
    df_vcs = df.groupby(['Run', 'Date'], as_index=False)[column].apply(lambda c: ((c == cat.upper()).sum()/float(len(c)))*100).reset_index()
    name = '% Samples {0} = {1}'.format(column, cat)
    df_vcs.rename(columns={0: name}, inplace=True)
    df_vcs[name] = df_vcs[name].round(2)
    # 2. get sample names
    df_names = format_sample_names(df_copy, column)
    # Add names to calculated % df
    df_vcs = pd.merge(df_vcs, df_names, left_on='Run', right_on='Run',
                      how='left', suffixes=('', '_y'))
    df_vcs = pd.DataFrame(df_vcs, columns=['Date', name, 'Run', 'Sample'])
    # 3. Add dumy next month date
    df_vcs = add_dates(df_vcs)
    # 4. Format data for writing to html file
    df_vcs['Data'] = df_vcs[['Date', name]].values.tolist()
    df_vcs = format_date_names(df_vcs)
    return df_vcs


def percentage_of_samples_above_threshold(df, column, depth):
    """
    (df) -> df
    1. Calculate persentage of samples greater than X median depth
    2. Add sample names as sample name + (Depth)
    3. Add dumy dates at start and end, format data for html
    Get %  of samples greater than the depth median threshold
    """
    df[column] = pd.to_numeric(df[column], errors='coerce').round(2)
    df_dep_val = df.groupby(['Run', 'Date'], as_index=False)[column].apply(lambda c: ((c > float(depth)).sum()/float(len(c)))*100).reset_index()
    name = '% Samples greater than {0}'.format(depth)
    df_dep_val.rename(columns={0: name}, inplace=True)
    df_dep_val[name] = df_dep_val[name].round(2)
    df_names = format_sample_names(df, column)
    df_dep = pd.merge(df_dep_val, df_names, left_on=['Run', 'Date'],
                      right_on=['Run', 'Date'], how='left')
    # Add dumy next month date
    df_dep = add_dates(df_dep)
    # Format data for writing to html file
    df_dep['Data'] = df_dep[['Date', '% Samples greater than {0}'.format(depth)]].values.tolist()
    df_dep = format_date_names(df_dep)
    return df_dep


def rolling_mean(df_dup_all, Duplicates, win):
    """
    (df) -> df
    Compute rolling mean
    """
    df_dup_all.sort_values(by=['Date'], inplace=True)
    df_dup_all.set_index('Date', inplace=True)
    df_dup_all['mean'] = df_dup_all.rolling(win).mean().round(2)[Duplicates]
    # closed = 'left'
    df_dup_all['2std'] = df_dup_all.rolling(win).std().round(2)[Duplicates]
    df_dup_all['posstd'] = df_dup_all['mean'] + df_dup_all['2std']
    df_dup_all['negstd'] = df_dup_all['mean'] - df_dup_all['2std']
    df_dup_all['posstd'] = df_dup_all['posstd'].round(2)
    df_dup_all['negstd'] = df_dup_all['negstd'].round(2) 
    df_dup_all.reset_index(inplace=True)
    return df_dup_all


def mean_and_stdev(df, Duplicates, win, kind='lines', per_sample='False'):
    """
    (df) -> df
    get rolling mean (1 year window), positive and negative std
    """
    df[Duplicates] = pd.to_numeric(df[Duplicates], errors='coerce').round(2)
    if per_sample == 'False':
        # Add sample names (group names in run as sample (y-value))
        df_names = format_sample_names(df, Duplicates)
        # get mean Duplicates per run
        df_dup_all = df.groupby(['Run', 'Date'], as_index=False)[Duplicates].mean().round(2)
        # merge names with mean duplicates
        df_dup_all = pd.merge(df_dup_all, df_names, left_on=['Run', 'Date'],
                              right_on=['Run', 'Date'], how='left')
    else:
        df_dup_all = df.copy()
        #df_dup_all['Sample'] = df_dup_all[['Sample', Duplicates]].apply(lambda x: '{} ({})'.format(x[0], x[1]), axis=1)
        df_dup_all = pd.DataFrame(df_dup_all, columns=['Run', 'Date', 'Sample', Duplicates])
        # swap run and sample columns 
        df_dup_all.columns = ['Sample', 'Date', 'Run', Duplicates]
    # add rolling mean and std
    df_dup_all = rolling_mean(df_dup_all, Duplicates, win)
    # format columns for dygraph
    if kind == 'lines':
        columns = ['Run', 'Date', 'negstd', 'mean', 'posstd',
                   Duplicates, 'Sample']
    if kind == 'area':
        df_dup_all['{0}_1'.format(Duplicates)] = df_dup_all[Duplicates]
        df_dup_all['{0}_2'.format(Duplicates)] = df_dup_all[Duplicates]
        columns = ['Run', 'Date', 'negstd', 'mean', 'posstd',
                   '{0}_1'.format(Duplicates), Duplicates,
                   '{0}_2'.format(Duplicates), 'Sample']
    df_dup_all = pd.DataFrame(df_dup_all, columns=columns)
    # Add dumy next month date
    df_dup_all = add_dates(df_dup_all)
    # Format data for writing to html file
    if kind == 'lines':
        df_dup_all['Data'] = df_dup_all[['Date', 'negstd', 'mean', 'posstd', Duplicates]].values.tolist()
    if kind == 'area':
        df_dup_all['Range'] = df_dup_all[['negstd', 'mean', 'posstd']].values.round(2).tolist()
        df_dup_all['Values'] = df_dup_all[['{0}_1'.format(Duplicates), Duplicates, '{0}_2'.format(Duplicates)]].values.round(2).tolist()
        df_dup_all['Data'] = df_dup_all[['Date', 'Range', 'Values']].values.tolist()
    df_dup_all = format_date_names(df_dup_all)
    return df_dup_all


def absolute_threshold(df, column, lower_threshold=np.nan, upper_threshold=np.nan, Type='', per_sample='False'):
    """
    (df) -> df
    generate scatter plot for data with threshold
    """
    df[column] = pd.to_numeric(df[column], errors='coerce').round(2)
    df_data = df.copy()
    if Type != '':
        df_data = df[df['Type'].str.contains(Type)]
    if per_sample == 'False':
        # Add sample names
        df_names = format_sample_names(df_data, column)
        # get mean of values from run
        df_bq = df_data.groupby(['Run', 'Date'],
                                as_index=False)[column].mean().round(2)
        # merge names with values
        df_bq = pd.merge(df_bq, df_names, left_on=['Run', 'Date'],
                         right_on=['Run', 'Date'], how='left')
    else:
        df_bq = df_data.copy()
        # format names 
        #df_bq['Sample'] = df_bq[['Sample', column]].apply(lambda x: '{} ({})'.format(x[0], x[1]), axis=1)
        df_bq = pd.DataFrame(df_bq, columns=['Run', 'Date', 'Sample', column])
        # swap run and sample columns 
        df_bq.columns = ['Sample', 'Date', 'Run', column]
    # set threshold
    df_bq['lower_threshold'] = float(lower_threshold)
    df_bq['upper_threshold'] = float(upper_threshold)
    # Add dumy next month date
    df_bq = add_dates(df_bq)
    # Format data for writing to html file
    df_bq['Data'] = df_bq[['Date', 'upper_threshold', 'lower_threshold', column]].values.tolist()
    df_bq = format_date_names(df_bq)
    return df_bq


def box_whisker_plot(df, ColumnName, Type='', lower_threshold=np.nan, upper_threshold=np.nan):
    """
    (df) -> df
    generate box plot data form the df
    """
    df_copy = df.copy()
    # Format columns
    df_copy[ColumnName] = pd.to_numeric(df_copy[ColumnName], errors='coerce').round(2)
    if Type != '':
        df_copy = df_copy[df_copy['Type'].str.contains(Type)]
    if 'Run' not in df_copy.columns:
        df_copy['Run'] = df_copy['Sample']
    if 'Sample' not in df_copy.columns:
        df_copy['Sample'] = df_copy['Run']
    # Get quantiles  25, 50 and 75 %
    df_bp = df_copy.groupby('First_Date')[ColumnName].describe()
    df_bp = pd.DataFrame(df_bp, columns=['25%', '50%', '75%']).reset_index()
    # Get BP data
    bp = pd.DataFrame.boxplot(df_copy, by='First_Date', return_type='dict')
    a = bp[ColumnName]
    outliers = [flier.get_ydata() for flier in a["fliers"]]
#    boxes = [box.get_ydata() for box in a["boxes"]] # not needed
#    medians = [median.get_ydata() for median in a["medians"]] # not needed
    whiskers = [whiskers.get_ydata() for whiskers in a["whiskers"]]
    outliers = pd.Series(outliers, name="outliers")
    whiskers = pd.DataFrame(whiskers)
    whiskers = list(whiskers[1])
    Lower_whisker = []
    Upper_whisker = []
    w = 0
    while w < len(whiskers):
        Lower_whisker.append(whiskers[w])
        Upper_whisker.append(whiskers[w+1])
        w = w + 2
    Lower_whisker = pd.Series(Lower_whisker, name="Lower_whisker")
    Upper_whisker = pd.Series(Upper_whisker, name="Upper_whisker")
    df_whis = pd.concat([Lower_whisker, Upper_whisker, outliers], axis=1)
    df_bp = pd.merge(df_bp, df_whis, left_index=True, right_index=True,
                     how='outer', suffixes=['', 'y'])
    # split outliers list in column
    outlier_df = pd.DataFrame(df_bp['outliers'].apply(pd.Series).stack())
    if len(outlier_df) > 0:
        outlier_df = outlier_df.reset_index(level=1, drop=True)
        outlier_df.rename(columns={0: 'Outlier'}, inplace=True)
        # Group runs and sample names in dataset
        gp_df_run = df_copy.groupby(['First_Date', ColumnName])['Run'].agg(lambda x: ', '.join(x)).reset_index()
        gp_df_samp = df_copy.groupby(['First_Date', ColumnName])['Sample'].agg(lambda x: ', '.join(x)).reset_index()
        df_names = pd.merge(gp_df_run, gp_df_samp, left_index=True,
                            right_index=True, how='outer', suffixes=['', 'y'])
        # add outliers to bp
        df_bp = pd.merge(df_bp, outlier_df, left_index=True, right_index=True,
                         how='left')
        # Add labels to bp
        df_bp = pd.merge(df_bp, df_names, left_on=['First_Date', 'Outlier'],
                         right_on=['First_Date', ColumnName], how='left')
    # keeps only columns needed
    df_bp.rename(columns={'First_Date': 'Date'}, inplace=True)
    df_bp = pd.DataFrame(df_bp, columns=['Date', '25%', '75%', 'Upper_whisker',
                                         'Lower_whisker', '50%', 'Outlier',
                                         'Run', 'Sample'])
    df_bp['Sample'].fillna('NA', inplace=True)
    df_bp['Run'].fillna('NA', inplace=True)
    # set threshold
    df_bp['lower_threshold'] = float(lower_threshold)
    df_bp['upper_threshold'] = float(upper_threshold)
    # Add dumy dates at begnining and end of dataframe
    df_bp = add_dates(df_bp)
    # Format data for writing to html file
    df_bp['Data'] = df_bp[['Date', '25%', '75%', 'Upper_whisker', 'Lower_whisker', '50%', 'Outlier', 'upper_threshold', 'lower_threshold']].values.tolist()
    df_bp = format_date_names(df_bp)
    return df_bp

def bar_line_plot(df, column_name):
    """
    (df) -> df
    generate bar and line plot data form the df
    """
    df_copy = df.copy()
    if 'Sample' not in df_copy.columns:
        df_copy['Sample'] = df_copy['Run']
    df_dup_all = df_copy.groupby(['First_Date', column_name], as_index=False)['Sample'].count()
    #df_dup_all.to_clipboard(sep=',')
    df_dup_all = df_dup_all.pivot(index='First_Date', columns=column_name, values='Sample')
    df_dup_all["Total"] = df_dup_all.sum(axis=1)
    df_dup_all.fillna(0, inplace=True)
    df_dup_all.reset_index(inplace=True)
    df_dup_all.rename(columns={'First_Date': 'Date'}, inplace=True)
    # Add dumy dates at begnining and end of dataframe
    df_dup_all = add_dates(df_dup_all)
    #df_dup_all.to_clipboard(sep=',')
    return df_dup_all


def stacked_bar_plot(df, column_name):
    """
    (df) -> df
    generate stacked bar plot data form the df
    """
    df_copy = df.copy()
    if 'Sample' not in df_copy.columns:
        df_copy['Sample'] = df_copy['Run']
    df_dup_all = df_copy.groupby(['First_Date', column_name], as_index=False)["Sample"].count()
    df_dup_all = df_dup_all.pivot(index='First_Date', columns=column_name, values='Sample')
    # for drawing 
    df_dup_all_cumsum = df_dup_all.cumsum(axis="columns", skipna=True)
    df_dup_all_cumsum.reset_index(inplace=True)
    df_dup_all_cumsum.rename(columns={'First_Date': 'Date'}, inplace=True)
    # for display actual data
    df_dup_all["Total"] = df_dup_all.sum(axis=1)
    df_dup_all.fillna(0, inplace=True)
    df_dup_all.reset_index(inplace=True)
    df_dup_all.rename(columns={'First_Date': 'Date'}, inplace=True)
    # Add dumy dates at begnining and end of dataframe
    df_dup_all = add_dates(df_dup_all)
    df_dup_all_cumsum = add_dates(df_dup_all_cumsum)
    #df_dup_all.to_clipboard(sep=',')
    # data_draw df_dup_all_cumsum
    # data_dispay df_dup_all
    return df_dup_all, df_dup_all_cumsum
    
    
def create_dir(vals, df_chart, chart_id, chart_title, y_label, startdate, enddate, categories, ylabel2, df_chart_cumsum, per_sample, column_name):
    '''
    df, dir -> dir
    '''
    vals[chart_id + 'htmltemplates'] = {}
    vals[chart_id + 'htmltemplates']['data'] = df_chart['Data'].to_json(orient='values')
    try:
        vals[chart_id + 'htmltemplates']['run_name'] = df_chart['Run'].to_json(orient='values')
        vals[chart_id + 'htmltemplates']['sample_name'] = df_chart['Sample'].to_json(orient='values')
    except KeyError:
        pass
    # html variables to be replaced
    vals[chart_id + 'htmltemplates']['divname'] = chart_id + '_divname'
    vals[chart_id + 'htmltemplates']['fromdate'] = chart_id + '_fromdate'
    vals[chart_id + 'htmltemplates']['todate'] = chart_id + '_todate'
    vals[chart_id + 'htmltemplates']['graphvar'] = chart_id + '_graphvar'
    vals[chart_id + 'htmltemplates']['restorebutton'] = chart_id + '_restorebutton'
    vals[chart_id + 'htmltemplates']['labeldiv'] = chart_id + '_labeldiv'
    vals[chart_id + 'htmltemplates']['yearbutton'] = chart_id + '_yearbutton'
    # js variables
    vals[chart_id + 'htmltemplates']['dataname'] = chart_id + '_dataname'
    vals[chart_id + 'htmltemplates']['runname'] = chart_id + '_runname'
    vals[chart_id + 'htmltemplates']['samplename'] = chart_id + '_samplename'
    vals[chart_id + 'htmltemplates']['title'] = chart_title
    vals[chart_id + 'htmltemplates']['ylabel'] = y_label
    # id
    vals[chart_id + 'htmltemplates']['chart_id'] = chart_id
    vals[chart_id + 'htmltemplates']['startdate'] = startdate
    vals[chart_id + 'htmltemplates']['enddate'] = enddate
    # for bar plot
    vals[chart_id + 'htmltemplates']['categories'] = categories
    vals[chart_id + 'htmltemplates']['graphvar_labels'] = chart_id + '_labels'
    vals[chart_id + 'htmltemplates']['graphvar_series'] = chart_id + '_series'
    vals[chart_id + 'htmltemplates']['ylabel2'] = ylabel2 
    # for stacked bar plot
    try:
        vals[chart_id + 'htmltemplates']['labeldata'] = df_chart_cumsum['Data'].to_json(orient='values')
    except:
        pass
    vals[chart_id + 'htmltemplates']['label_dataname'] = chart_id + '_label_dataname'
    # for per_sample
    vals[chart_id + 'htmltemplates']['id_perSample_bool'] = per_sample
    vals[chart_id + 'htmltemplates']['id_perSample'] =  chart_id + '_per_sample'
    vals[chart_id + 'htmltemplates']['download_title'] =  column_name
    
    return vals


def process_y(column_name):
    """
    (str) -> str
    Do following processing in string
    1. replace _ with ""
    2. replace percent with %
    3. replace pct with %
    4. capitalize words
    """
    # .replace('percent', '%').replace('pct', '%')
    return column_name.replace('_', ' ').title().replace('Percent Gc', '% GC Content').replace('Tstv', 'Ts/Tv')


def process_title(column_name):
    """
    (str) -> str
    Do following processing in string
    1. replace _ with ""
    2. replace percent with %
    3. replace pct with %
    4. capitalize words
    """
    # .replace('percent', '%').replace('pct', '%')
    return column_name.replace(' ', '_').replace('>=', 'ge').replace('<=', 'le').replace('>', 'gt').replace('/', '_').replace('<', 'lt').replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(',', '').replace('%', 'Percent').replace('≥', 'ge').replace('≤', 'le')


###############################################################################
# Get parameters
def main(args):
    """
    (args) -> html
    takes number of arguments and produces interactive chronqc html report
    """
    db = op.abspath(args.db)
    panel = args.panel
    templates_dir = op.abspath(op.join(op.dirname(__file__), 'templates'))

# output dir and file
    # Get output directory 1. user defined 2. db dir 3. multiqc_stats dir
    # Output file name
    day = date.today().strftime("%d_%b_%Y")
    if args.prefix is not None:
        prefix = '{0}.{1}.{2}.{3}'.format(args.prefix, panel, 'chronqc',  day)
    else:
        prefix = '{0}.{1}.{2}'.format(panel, 'chronqc', day)

    # Get output file
    if args.output is not None:
        output_directory = op.abspath(args.output)
    else:
        output_directory, output_prefix = utils.path_leaf(db)

    output_directory = op.join(output_directory, "chronqc_output")
    if not op.exists(output_directory):
        os.makedirs(output_directory)
    elif op.exists(output_directory) and not args.force:
        # logger.fatal("Output directory %s already exists", output_directory)
        print("FATAL: Output directory {0} already exists, use -f to overwrite".format(output_directory))
        sys.exit(1)
    elif op.exists(output_directory) and args.force:
        pass
    # html report
    out_file = op.join(output_directory, "%s.html" % prefix)

# create logger
    log_file = op.join(output_directory, 'chronqc.log')

    logging.basicConfig(filename=log_file,
                        format='%(asctime)s - %(name)s - %(levelname)s - \
                        %(message)s')
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
    logger.info("Started chronqc {0}".format(day))
    # read plot config
    f = op.abspath(args.json)
    try:
        config = json.load(io.open(f, 'r', encoding = 'utf-8-sig'),strict=False)
        logger.info("Got required parameters for chronqc")
    except ValueError:
        e = sys.exc_info()[1]
        logger.critical("FATAL: Error in JSON file {0}:{1}".format(e, op.abspath(args.json)))
        sys.exit(1)

    # enddate = date.today() + relativedelta(months=+1)
    # enddate = enddate.strftime('%Y-%m-%d')
# Create dictionary of data tobe filled in html file
    datetime = date.today()
    vals = {'htmltemplates': '', 'calendartemplates': '',
            'javascripttemplate': '', 'sidebartemplates': '',
            'j': '$j', 'panel': panel, 'startdate': '$startdate',
            'enddate': '$enddate', 'datetime': datetime, 'pdfname': '$pdfname', 
            'table': '$table','headers': '$headers', 'rows':'$rows', 'row':'$row', 
            'cols':'$cols', 'col':'$col', 'text':'$text'}
    i = 1
    chart_ids = []
    group_ids = {}
    for chart in config:
        chart_id = 'g' + str(i)
        chart_ids.append(chart_id)
        table = chart.get('table_name', 'chronqc_stats_data')
        i = i + 1
        vals['htmltemplates'] = vals['htmltemplates'] + '$' + chart_id + '_html' + '\n'
        vals['calendartemplates'] = vals['calendartemplates'] + '$' + chart_id + '_calendar' + '\n'
        vals['javascripttemplate'] = vals['javascripttemplate'] + '$' + chart_id + '_js' + '\n'
        group_side = '<p class="nav-item2"> {0}</p>\n'.format(table.replace('_', ' ').title())
        #vals['sidebartemplates'] = vals['sidebartemplates'] + '$' + chart_id + '_sidebar' + '\n'
        if table not in group_ids:
            group_ids[table] = ['$' + chart_id + '_sidebar' ]
            vals['sidebartemplates'] =  vals['sidebartemplates'] + group_side + '$' + chart_id + '_sidebar' + '\n'
        else:
            vals['sidebartemplates'] = vals['sidebartemplates'] + '$' + chart_id + '_sidebar' + '\n'

    # SUBSTITUTION 1: create a template based on number of plots to be plotted
    tmpl = string.Template(open(op.join(templates_dir, "base_template.html")).read())
    tmpl = tmpl.substitute(**vals)
    logger.info("Finished creating base template based on number of plots")
    print('Started ChronQC')
    # SUBSTITUTION 2: for all plots to be plotted do data processing
    #   and substitute values in html, calander and js templates
    i = 1
    for chart in config:
        chart_id = 'g' + str(i)
        i = i + 1
        table = chart.get('table_name', 'chronqc_stats_data')
        column_name = chart["chart_properties"]["y_value"]
        include_samples = chart.get('include_samples', 'all')
        exclude_samples = chart.get('exclude_samples', '')
        per_sample = chart["chart_properties"].get('per_sample', 'False')
        categories = chart["chart_properties"].get('categories', '')
        category_str = '' 
        ylabel2 = ''
        df_chart_cumsum = ''
        logger.info("Plotting {0}".format(chart_id))
        # Fetch data from the sqlite database
        df = fetch_stats_data(db, table, panel, categories=categories, ColumnName=column_name)
        logger.info("For {0}: got total {1} records".format(chart_id, len(df)))
        if len(df) == 0:
            logger.critical("FATAL: For {0} {1}: no records found in {2}".format(chart_id, column_name, table))
            sys.exit(1)
        # keep only desired samples
        try:
            df = get_samples_data(df, include_samples, exclude_samples, per_sample=per_sample)
        except KeyError: 
            e = sys.exc_info()[1]
            logger.critical("FATAL: no {0} column found in {1}".format(e, table))
            sys.exit(1)
        except Exception: 
            e = sys.exc_info()[1]
            logger.critical("FATAL: please check {0} column in {1}".format(e, table))
            sys.exit(1)
        if len(df) == 0:
            logger.critical("FATAL: For {0} {1}: no records found for {2}".format(chart_id, column_name, include_samples))
            sys.exit(1)
        logger.info("For {0}: kept {1} records after filtering".format(chart_id, len(df)))
        # dates for display
        startdate_year = df.loc[len(df)-1, 'Date'].date() + relativedelta(months=-12)
        start_df = df.loc[0, 'Date'].date()
        if startdate_year > start_df:
            startdate = startdate_year.strftime('%Y-%m-%d')
        else:
            start_df = start_df + relativedelta(months=-1)
            startdate = start_df.strftime('%Y-%m-%d')
        enddate = df.loc[len(df)-1, 'Date'] + relativedelta(months=+1)
        vals['startdate'] = startdate
        vals['enddate'] = enddate
        # process y formatting 
        y = process_y(column_name)
        # generate data in format for html
        if chart['chart_type'] == 'time_series_with_percentage_category':
            cat = chart["chart_properties"].get('category', 'PASS')
            t = '% Samples per run with {0} = {1}'.format(y, cat)
            y = '% {0} = {1}'.format(y, cat)
            chart_title = chart["chart_properties"].get('chart_title', t)
            y_label = chart["chart_properties"].get('y_label', y)
            js_tmpl = string.Template(open(op.join(templates_dir, "percent_plot_threshold.txt")).read())
            if not column_name in df.columns:
                logger.critical("FATAL: no {0} column found in {1}".format(column_name, table))
                sys.exit(1)
            df_chart = percentage_category(df, column_name, cat)
            logger.info("For {0}: {1} data points will be written to html".format(chart_id, len(df_chart)))
        elif chart['chart_type'] == 'time_series_with_percentage_of_samples_above_threshold':
            threshold = chart["chart_properties"]["threshold"]
            t = '% Samples per run with {0} ≥ {1}'.format(y, threshold)
            y = '% {0} ≥ {1}'.format(y, threshold)
            chart_title = chart["chart_properties"].get('chart_title', t)
            y_label = chart["chart_properties"].get('y_label', y)
            js_tmpl = string.Template(open(op.join(templates_dir, "percent_plot_threshold.txt")).read())
            if not column_name in df.columns:
                logger.critical("FATAL: no {0} column found in {1}".format(column_name, table))
                sys.exit(1)
            df_chart = percentage_of_samples_above_threshold(df, column_name, threshold)
            logger.info("For {0}: {1} data points will be written to html".format(chart_id, len(df_chart)))
        elif chart['chart_type'] == 'time_series_with_mean_and_stdev':
            win = chart["chart_properties"].get('window', '365D')
            info = 'sample' if per_sample == 'True' else 'run'
            try:
                win = int(win)
                winf = "past {0} {1}s".format(win, info)
            except:
                winf = "past {0} {1}s".format(win, info)
            if win == '365D':
                winf = "past 1 year {}s".format(info)
            if per_sample == 'False':
                t = '{0} (Mean per run with {1} rolling mean and ±2 standard deviation)'.format(y, winf)
                y = '{0} (Mean per run)'.format(y)
            else:
                t = '{0} (with {1} rolling mean and ±2 standard deviation)'.format(y, winf)
                y = '{0}'.format(y)
            chart_title = chart["chart_properties"].get('chart_title', t)
            y_label = chart["chart_properties"].get('y_label', y)
            js_tmpl = string.Template(open(op.join(templates_dir, "mean_and_stdev.txt")).read())
            if not column_name in df.columns:
                logger.critical("FATAL: no {0} column found in {1}".format(column_name, table))
                sys.exit(1)
            df_chart = mean_and_stdev(df, column_name, win=win, per_sample=per_sample)
            logger.info("For {0}: {1} data points will be written to html".format(chart_id, len(df_chart)))
        elif chart['chart_type'] == 'time_series_with_absolute_threshold':
            if per_sample == 'False':
                t = '{0} (Mean per run)'.format(y)
                y = '{0} (Mean per run)'.format(y)
            else:
                t = '{0}'.format(y)
                y = '{0}'.format(y)
            chart_title = chart["chart_properties"].get('chart_title', t)
            y_label = chart["chart_properties"].get('y_label', y)
            js_tmpl = string.Template(open(op.join(templates_dir, "absolute_threshold.txt")).read())
            lower_threshold = chart["chart_properties"].get("lower_threshold", np.nan) 
            upper_threshold = chart["chart_properties"].get("upper_threshold", np.nan)
            Type = chart["chart_properties"].get("Type", '')
            if not column_name in df.columns:
                logger.critical("FATAL: no {0} column found in {1}".format(column_name, table))
                sys.exit(1)
            df_chart = absolute_threshold(df, column_name,
                                          lower_threshold=lower_threshold,
                                          upper_threshold=upper_threshold,
                                          Type=Type, per_sample=per_sample)
            #df_chart.to_clipboard(sep=',')
            logger.info("For {0}: {1} data points will be written to html".format(chart_id, len(df_chart)))
        elif chart['chart_type'] == 'time_series_with_box_whisker_plot':
            t = '{0} Monthly Box-and-Whisker Plot'.format(y)
            y = '{0}'.format(y)
            chart_title = chart["chart_properties"].get('chart_title', t)
            y_label = chart["chart_properties"].get('y_label', y)
            Type = chart["chart_properties"].get("Type", '')
            lower_threshold = chart["chart_properties"].get("lower_threshold", np.nan) 
            upper_threshold = chart["chart_properties"].get("upper_threshold", np.nan)
            js_tmpl = string.Template(open(op.join(templates_dir, "box_whisker_plot.txt")).read())
            if not column_name in df.columns:
                logger.critical("FATAL: no {0} column found in {1}".format(column_name, table))
                sys.exit(1)
            if Type != '':
                df_chart = box_whisker_plot(df, column_name, Type=Type, 
                                        lower_threshold=lower_threshold,
                                        upper_threshold=upper_threshold)
            else:
                df_chart = box_whisker_plot(df, column_name, lower_threshold=lower_threshold, upper_threshold=upper_threshold)
            logger.info("For {0}: {1} data points will be written to html".format(chart_id, len(df_chart)))
        elif chart['chart_type'] == 'time_series_with_bar_line_plot':
            if categories == '':
                logger.critical("FATAL: no categories defined in JSON for time_series_with_bar_line_plot")
                sys.exit(1)                
            t = 'Monthly bar and line plot for {0} ({1})'.format(y, categories)
            y = 'Monthly count'
            chart_title = chart["chart_properties"].get('chart_title', t)
            y_label = chart["chart_properties"].get('y_label', y)
            y2 = 'Monthly total'
            ylabel2 = chart["chart_properties"].get('y_label2', y2)
            js_tmpl = string.Template(open(op.join(templates_dir, "bar_line_plot.txt")).read())
            if not column_name in df.columns:
                logger.critical("FATAL: no {0} column found in {1}".format(column_name, table))
                sys.exit(1)
            df_chart = bar_line_plot(df, column_name)
            categories = df_chart.columns
            category_str = ''             
            x = 0
            while x < len(categories)-1:
                category_str = category_str + '"{0}", '.format(categories[x])
                x = x + 1
            if x == len(categories)-1:
                category_str = category_str + ' "{0}"'.format(categories[x])
            df_chart['Data'] = df_chart.values.tolist()
            df_chart = pd.DataFrame(df_chart['Data'])
            logger.info("For {0}: {1} data points will be written to html".format(chart_id, len(df_chart)))
        elif chart['chart_type'] == 'time_series_with_stacked_bar_plot':
            if categories == '':
                logger.critical("FATAL: no categories defined in JSON for time_series_with_stacked_bar_plot")
                sys.exit(1) 
            t = 'Monthly stacked bar plot for {0} ({1})'.format(y, categories)
            y = 'Monthly count'
            chart_title = chart["chart_properties"].get('chart_title', t)
            y_label = chart["chart_properties"].get('y_label', y)
            js_tmpl = string.Template(open(op.join(templates_dir, "stacked_bar_plot.txt")).read())
            if not column_name in df.columns:
                logger.critical("FATAL: no {0} column found in {1}".format(column_name, table))
                sys.exit(1)
            df_chart, df_chart_cumsum = stacked_bar_plot(df, column_name)
            categories = df_chart_cumsum.columns
            category_str = ''             
            x = 0
            while x < len(categories)-1:
                category_str = category_str + '"{0}", '.format(categories[x])
                x = x + 1
            if x == len(categories)-1:
                category_str = category_str + ' "{0}"'.format(categories[x])
            df_chart['Data'] = df_chart.values.tolist()
            df_chart = pd.DataFrame(df_chart['Data'])
            df_chart_cumsum['Data'] = df_chart_cumsum.values.tolist()
            df_chart_cumsum = pd.DataFrame(df_chart_cumsum['Data'])
            logger.info("For {0}: {1} data points will be written to html".format(chart_id, len(df_chart)))            
        else:
            logger.critical("For {0}: No suitable chart_type is defined check JSON".format(chart_id))
            sys.exit(1)
        # keep data in dir
        download_title = process_title(chart_title)
        vals = create_dir(vals, df_chart, chart_id, chart_title, y_label,
                          startdate, enddate, categories=category_str, ylabel2=ylabel2, df_chart_cumsum=df_chart_cumsum, per_sample=per_sample, column_name=download_title)
        # html template
        html_tmpl = string.Template(open(op.join(templates_dir, "html.txt")).read())
        vals[chart_id + '_html'] = html_tmpl.substitute(**vals[chart_id + 'htmltemplates'])
        logger.info("For {0}: Finished creating html template".format(chart_id))
        # calendar template
        #calendar_tmpl = string.Template(open(op.join(templates_dir, "calendar.txt")).read())
        #vals[chart_id + '_calendar'] = calendar_tmpl.substitute(**vals[chart_id + 'htmltemplates'])
        #logger.info("For {0}: Finished creating calendar template".format(chart_id))
        # js template
        vals[chart_id + '_js'] = js_tmpl.substitute(**vals[chart_id + 'htmltemplates'])
        logger.info("For {0}: Finished creating js template".format(chart_id))
        # side bar with header
        sidebar_tmpl = string.Template(open(op.join(templates_dir, "sidebar.txt")).read())
        vals[chart_id + '_sidebar'] = sidebar_tmpl.substitute(**vals[chart_id + 'htmltemplates'])
        utils.print_progress(i+1, len(config)+2, prefix='Running ChronQC', decimals=1, bar_length=50)
    vals['pdfname'] = "%s.pdf" % prefix
    # substitute vals in main template
    tmpl = string.Template(tmpl).substitute(**vals)
    with io.open(out_file, "w", encoding='utf8') as fh:
        fh.write(tmpl)
    logger.info("Finished creating {0} chronqc plots: {1}".format(i-1, out_file))
    print("Finished creating {0} chronqc plots: {1}".format(i-1, out_file))
