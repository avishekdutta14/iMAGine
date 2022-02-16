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
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()

parser.add_argument('-cs', '--completeness', help = 'Completeness percentage')

parser.add_argument('-cn', '--contamination', help = 'Contamination percentage')

args = parser.parse_args()


# Declaring names form checkm file header

header_list = ["Bin_Name", "Stats"]

df = pd.read_csv("bin_stats_ext.tsv", sep='\t', names=header_list)

# splitting and adding based on comma as deliminator

df1 = pd.concat([df["Bin_Name"], df["Stats"].str.split(', ', expand=True)], axis=1)

#df["Stats"] = df["Stats"].str.split(',',expand=True)

#df1.to_csv('checkm_stats.csv', index=False)

# Selecting certain columns

df2 = df1.iloc[:,[0,11,12]]

# replacing certain strings in the columns

df2[10] = df2[10].str.replace("'", "")

df2[11] = df2[11].str.replace("'", "")

df2[10] = df2[10].str.replace("Completeness:", "")

df2[11] = df2[11].str.replace("Contamination:", "")

# renaming the columns

df3 = df2.rename(columns={10: "Completeness", 11: "Contamination"})

# sorting the columns

df4 = df3.sort_values(by='Completeness',  ascending=False)

# saving intermediate file for string to integer

df4.to_csv('refined_stats.csv', index=False)

df5 = pd.read_csv("refined_stats.csv")

a = '{}'.format(args.completeness)
b = '{}'.format(args.contamination)


if a !="None" and b !="None":

    # for annotating bins
    conditions = [
        (df5['Completeness'] >= float(a)) & (df5['Contamination'] <= float(b))
        ]

    values = ['selected']

    df5['Bin_quality'] = np.select(conditions, values)

    df5.to_csv('checkm_bin_quality.csv', index=False)

    # segregating  dataframe based on bin quality

    selected= df5[df5['Bin_quality'] == "selected"]

    # For extracting high quality bins

    selected_name =  selected[["Bin_Name"]]

    selected_name['Bin_Name'] =  selected_name['Bin_Name'].astype(str) + ".fa"

    selected_name.to_csv('selected_bins.txt', header=False, index=False)

    os.system ('mkdir selected_bins')
    os.system ('rsync --files-from=selected_bins.txt bins_dir/ selected_bins/')
    os.remove ('selected_bins.txt')

    os.remove ('refined_stats.csv')

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

    df5.to_csv('checkm_bin_quality.csv', index=False)

    # segregating  dataframe based on bin quality

    high = df5[df5['Bin_quality'] == "high"]
    medium = df5[df5['Bin_quality'] == "medium"]
    low = df5[df5['Bin_quality'] == "low"]
    #contamination = df5[df5['Bin_quality'] == "contamination"]

    # For extracting high quality bins

    high_name =  high[["Bin_Name"]]

    high_name['Bin_Name'] =  high_name['Bin_Name'].astype(str) + ".fa"

    high_name.to_csv('high_name.txt', header=False, index=False)

    os.system ("mkdir high_qual_draft")
    os.system ("rsync --files-from=high_name.txt bins_dir/ high_qual_draft/")
    os.remove ('high_name.txt')

    # For extracting medium quality bins

    medium_name =  medium[["Bin_Name"]]

    medium_name['Bin_Name'] =  medium_name['Bin_Name'].astype(str) + ".fa"

    medium_name.to_csv('medium_name.txt', header=False, index=False)

    os.system ("mkdir medium_qual_draft")
    os.system ("rsync --files-from=medium_name.txt bins_dir/ medium_qual_draft/")
    os.remove ('medium_name.txt')

    # For extracting low quality bins

    low_name =  low[["Bin_Name"]]

    low_name['Bin_Name'] =  low_name['Bin_Name'].astype(str) + ".fa"

    low_name.to_csv('low_name.txt', header=False, index=False)

    os.system ("mkdir low_qual_draft")
    os.system ("rsync --files-from=low_name.txt bins_dir/ low_qual_draft/")
    os.remove ('low_name.txt')
    os.remove ('refined_stats.csv')

    print ("The segregation of Bins/MAGs are done based on criterion mentioned in Bowers et al., 2017")

