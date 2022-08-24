#!/usr/bin/env python3

import pandas as pd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-n', '--sample_name', help = 'Sample name')
parser.add_argument('-a', '--annotation', help = 'Annotation of emapper')

args = parser.parse_args()
sample_name = '{}'.format(args.sample_name)
annotation = '{}'.format(args.annotation)

df = pd.read_csv("{}".format(annotation), sep='\t')

df[['A','B','C','D','E','F','G']] = df['#query'].str.split('_',expand=True)

df['#ID']=df['A']+'_'+df['B']+'_'+df['C']+'_'+df['D']+'_'+df['E']+'_'+df['F']

df = df.drop(columns=['A','B','C','D','E','F','G'])

# print(df)

contig_fold = pd.read_csv("pileup_result_{}.txt".format(sample_name), sep='\t')

contig_fold = contig_fold[["#ID", "Avg_fold"]]

final = pd.merge(left=df, right=contig_fold, how='left', left_on='#ID', right_on='#ID')

kegg_count = final['KEGG_ko'].value_counts().rename_axis('KEGG_ko').reset_index(name='Count_{}'.format(sample_name))

final_mod = final[["KEGG_ko", "Avg_fold"]]

final_mod = final_mod.groupby(['KEGG_ko'])["Avg_fold"].sum().rename_axis('KEGG_ko').reset_index(name="Avg_fold_{}".format(sample_name))

result = pd.merge(left=final_mod, right=kegg_count, how='left', left_on='KEGG_ko', right_on='KEGG_ko')

result.to_csv("gene_fold_counter_result_{}.csv".format(sample_name), index =False)

