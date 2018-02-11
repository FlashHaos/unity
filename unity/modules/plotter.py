#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set()

data = pd.read_csv(r'C:\Парсер\dataset.csv')

datapivot = pd.pivot_table(data,index="Name",columns="Vendor",values="Price")

f, ax = plt.subplots(figsize=(9, 6))
sns_plot = sns.heatmap(datapivot, annot=True, linewidths=.5, ax=ax)
fig = sns_plot.get_figure()
fig.savefig("output.png")