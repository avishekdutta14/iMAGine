#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import argparse
import ast
from Bio import SeqIO
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument('-cs', '--completeness', help = 'Completeness percentage')

parser.add_argument('-cn', '--contamination', help = 'Contamination percentage')

args = parser.parse_args()


# reading checkM and creating stats

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

# making plots

df1 = df[df['Contamination'] < 20]

fig, ax = plt.subplots()
  
plot = ax.scatter(df1.Contamination, df1.Completeness, s=df1.mean_coverage, c = df1.GC, cmap='Greens')
plt.xlabel("Contamination")
plt.ylabel("Completeness")

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.8])

legend1 = ax.legend(*plot.legend_elements(),
                    loc="lower left", title="GC percentage", bbox_to_anchor=(1, 0.2))
ax.add_artist(legend1)

handles, labels = plot.legend_elements(prop="sizes", alpha=0.6)
legend2 = ax.legend(handles, labels, loc="upper center", title="mean_coverage", bbox_to_anchor=(0.5, 1.3), ncol=5)


plt.savefig('scatter_plot_binviz.pdf')  

