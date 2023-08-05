# Module: autosentiment
# Author: Sazin Reshed Samin <sazinsamin50@gmail.com>
# License: MIT


from autosentiment.code import pie,analysis_ternary,percentage,number


import pandas as pd
df=pd.read_csv("/home/samin/anaconda3/dataset_2.csv")
percen=percentage(df['text'])
print(percen)