# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 10:36:16 2017

@author: tawarinr
"""
import pandas as pd
import chronqc_plot
import sqlite3
'''
df = chronqc_plot.fetch_stats_data('../examples/custom_db_example/chronqc_custom_db.sqlite', 'VCS_Stats_Summary', 'Somatic', categories="KRAS, KIT, BRAF, PDGFRA, NRAS", ColumnName='Gene')
df_chart = chronqc_plot.get_samples_data(df, include_samples='all', per_sample='False')
df_copy = df_chart.copy()
df_dup_all = df_copy.groupby(['First_Date', 'Gene'],  as_index=False)["Sample"].count()
df_dup_all = df_dup_all.pivot(index='First_Date', columns='Gene', values='Sample')
df_dup_all_1 = df_dup_all.cumsum(axis="columns", skipna=True)
df_dup_all["Total"] = df_dup_all.sum(axis=1)

#df_dup_all = df_dup_all.T
#df_dup_all.sort_values(by=[], axis="columns", ascending=False, inplace=True)
#df_dup_all.fillna(0, inplace=True)
#df_dup_all = df_dup_all.rolling(10, min_periods=1, axis="columns").sum()

#df_dup_all.reset_index(inplace=True)

#df_dup_all['Data'] = df_dup_all.values.tolist()
#df_dup_all = pd.DataFrame(df_dup_all['Data'])

genes="KRAS, KIT, BRAF, PDGFRA, NRAS"
genes = list(set([s.strip() for s in genes.split(',')]))
gene_que = 'Gene LIKE'
gene_str = ' "{0}" OR Gene LIKE '
i = 0
while i < len(genes)-1:
    gene_que = gene_que + gene_str.format(genes[i])
    i = i + 1
if i == len(genes)-1:
    gene_que = gene_que + ' "{0}" '.format(genes[i])
'''
# boolean conversion
multiqc_stats = r'../examples/multiqc_example_2/year_2017/multiqc_data/multiqc_general_stats.txt'
df = pd.read_csv(multiqc_stats, sep='\t', comment='#', chunksize=1000,
                     low_memory=False, iterator=True)
df = pd.concat(list(df), ignore_index=True)

#cnx = sqlite3.connect(r'../examples/multiqc_example_2/year_2017/multiqc_data/test.db')
#df.to_sql('test', cnx, index=False, if_exists='replace', chunksize = 1000)
#cnx.close()