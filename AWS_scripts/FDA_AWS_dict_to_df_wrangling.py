import urllib.request,io
import requests
import urllib
import json
import sys
import zipfile
import shutil
import timeit
import os
import pickle

import pandas as pd
import numpy as np

print('Loading in the data...')
# General
with open("./progress/file_name.txt", "rb") as fp:   # Unpickling
    file_name = pickle.load(fp)
# General
with open("./progress/data_2.txt", "rb") as fp:   # Unpickling
    data_2 = pickle.load(fp)
print('Done.')

# Select the files to save
model_num = ['X_1', 'X_2', 'X_3']
model_num = model_num[0]
save_all = True # save all the relevant files
save_df = False
save_entries = False
save_entries_len = False
save_unique_gn = False
save_unique_di = False



### 2. CONVERT TO A DATAFRAME

from helper_funcs.munging_func import section_1, section_2, section_3, section_4, section_5, section_6, section_7


df_1 = section_1(data_2, file_name)
df_2 = section_2(data_2)
df_3 = section_3(data_2)
df_4 = section_4(data_2)
df_5 = section_5(data_2)
df_6 = section_6(data_2)
df_7 = section_7(data_2)

df = df_1.join(df_2).join(df_3).join(df_4).join(df_5).join(df_6).join(df_7)

print('Saving dfs...')
df.to_csv('./progress/modeling/df_extracted.csv')
print('Saved, congrats!')
