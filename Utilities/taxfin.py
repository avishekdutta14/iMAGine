#!/usr/bin/env python3

"""
@author: Avishek Dutta, avdutta@ucsd.edu
@requires: python3, pandas
Usage: taxafin.py -t Viruses -s sample_name
"""

import pandas as pd
import argparse
import os

# defining argument for taxa input

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--taxa', help = 'Taxa Name')

parser.add_argument('-s', '--sample', help = 'Sample Name')

args = parser.parse_args()

# searching and reading the output annotation file from emapper

df = pd.read_csv('{}.final.annotations'.format(args.sample), sep='\t')

specific_taxa = df[df['eggNOG_OGs'].str.contains('{}'.format(args.taxa))]

specific_taxa.to_csv('{}.emapper.annotations_{}.csv'.format(args.sample,args.taxa), index=False)

# counting number of different taxa

specific_taxa_counts = specific_taxa['max_annot_lvl'].value_counts()

specific_taxa_counts.to_csv('{}.emapper_{}_counts_temp.csv'.format(args.sample,args.taxa))

specific_taxa_counts_1 = pd.read_csv('{}.emapper_{}_counts_temp.csv'.format(args.sample,args.taxa))

specific_taxa_counts_1.columns = ['{}_taxa'.format(args.taxa), '{}_{}_count'.format(args.sample,args.taxa)]

specific_taxa_counts_1.to_csv('{}.emapper_{}_counts.csv'.format(args.sample,args.taxa), index=False)

os.remove('{}.emapper_{}_counts_temp.csv'.format(args.sample,args.taxa))

