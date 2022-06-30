#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Avishek Dutta, avdutta@ucsd.edu
@requires: python3, pandas, numpy

If there are no argument passed, this script will segregate Bins based on Bowers et al., 2017 paper.
If only either one argument (contamination and completeness) is passed then also this script will segregate Bins based on Bowers et al., 2017 paper.
If both argumentas are passed, then it will select only those bins based on the criteria provided. 
"""

import pandas as pd
import numpy as np
import os
import argparse
import warnings
import ast
from Bio import SeqIO
import shutil

## Define function to copy bins in a dataframe to a new directory of given name.

def select_bins(dir_name, select_df):
    try:
        os.mkdir(dir_name)
    except OSError:
        pass
    for ibin in select_df.index:
        shutil.copy2('bins_dir/' + ibin + '.fa',
                     dir_name + '/' + ibin + '.fa')

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()

parser.add_argument('-cs', '--completeness', help = 'Completeness percentage')

parser.add_argument('-cn', '--contamination', help = 'Contamination percentage')

args = parser.parse_args()


# Declaring names form checkm file header

df = pd.DataFrame()

with open('bin_stats_ext.tsv', 'r') as f:
    for line in f.readlines():
        line = line.split('\t')
        d = ast.literal_eval(line[1])
        bin_name = line[0]
        
        for key in ['Completeness', 'Contamination', 'GC', 'Genome size', 'N50 (contigs)']:
            df.loc[bin_name, key] = d[key]
            
for b in os.listdir('bins_dir'):
    base_name = b.split('.fa')[0]
    coverage_values = []
    for record in SeqIO.parse('bins_dir/' + b, 'fasta'):
        coverage = record.id.split('_')[-1]
        coverage_values.append(float(coverage))
    df.loc[base_name, 'mean_coverage'] = pd.Series(coverage_values).mean()

# saving intermediate file for string to integer

df.to_csv('refined_stats.csv')

df5 = pd.read_csv("refined_stats.csv", index_col=0)

a = '{}'.format(args.completeness)
b = '{}'.format(args.contamination)


if a !="None" and b !="None":

    # for annotating bins
    conditions = [
        (df5['Completeness'] >= float(a)) & (df5['Contamination'] <= float(b))
        ]

    values = ['selected']

    df5['Bin_quality'] = np.select(conditions, values)

    df5.to_csv('checkm_bin_quality.csv', index=True)

    # segregating  dataframe based on bin quality

    selected= df5[df5['Bin_quality'] == "selected"]

    # For extracting high quality bins
    
    select_bins('selected_bins', selected)

    print ("The selected Bins/MAGs have completeness higher than", a ,"% and contamination less than", b, "%")

else:
    # for annotating bins
    conditions = [
        (df5['Completeness'] >= 90) & (df5['Contamination'] <= 5),
        (df5['Completeness'] >= 50) & (df5['Contamination'] <= 10),
        (df5['Completeness'] <= 50) & (df5['Contamination'] <= 10),
        (df5['Contamination'] >= 10)
        ]

    values = ['high', 'medium', 'low', 'contamination']

    df5['Bin_quality'] = np.select(conditions, values)

    df5.to_csv('checkm_bin_quality.csv', index=True)

    # segregating  dataframe based on bin quality

    high = df5[df5['Bin_quality'] == "high"]
    medium = df5[df5['Bin_quality'] == "medium"]
    low = df5[df5['Bin_quality'] == "low"]
    #contamination = df5[df5['Bin_quality'] == "contamination"]

    # For extracting high quality bins

    select_bins('high_qual_draft', high)

    # For extracting medium quality bins

    select_bins('medium_qual_draft', medium)

    # For extracting low quality bins

    select_bins('low_qual_draft', low)

    print ("The segregation of Bins/MAGs are done based on criterion mentioned in Bowers et al., 2017")

