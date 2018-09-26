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

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
import sklearn.cluster
from Levenshtein import distance
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# read in the df
df = pd.read_csv('./progress/modeling/df_extracted.csv', index_col = 0)
# Select the files to save
model_num = ['X_1', 'X_2', 'X_3']
model_num = model_num[0]
save_all = True # save all the relevant files
save_df = False
save_entries = False
save_entries_len = False
save_unique_gn = False
save_unique_di = False

# Drop missing generic names
df['generic_name'] = df['generic_name'].replace('NA', np.nan)
df = df.dropna(axis=0).reset_index()

### 4. FEATURE ENGINEERING

from helper_funcs.wrangling_func import unique_gen, entries_col_to_lists, value_gen, data_wrangling, percent_gen
from helper_funcs.wrangling_func import one_hot_encode_drugs, entry_condenser
from helper_funcs.conversion_dicts import quals, patientsex, admin_route_dict, drug_char_dict, unii_dict
from helper_funcs.conversion_dicts import dict_LLT_PT, dict_PT_HLT, dict_HLT_HLGT, dict_HLGT_SOC


df_ML = pd.DataFrame()

# List for the length of all the entry types
entries_len = []

### generic_name
test_col = 'generic_name'
print('Working on "{}"...'.format(test_col))
start_time = timeit.default_timer()
### One-hot-encode with condensed input
# Generate list of unique drugs
unique_entries = unique_gen(test_col, df)
# Condense this list to a lower dimensional space
cond_dict = entry_condenser(unique_entries, 25)
# Get raw columns as a nested list
col_as_list = entries_col_to_lists(test_col, df)
# Convert raw column to lower-d space
col_list_cond = [[[cond_dict[l1] for l1 in l2 if l1 in cond_dict.keys()] for l2 in l3] for l3 in col_as_list]
# Unnest the lowest list
col_list_cond = [[x for y in entry for x in y] for entry in col_list_cond]

# One hot encoder
# For more information, see the following link:
# https://stackoverflow.com/questions/46864816/convert-data-frame-of-comma-separated-strings-to-one-hot-encoded
print('One Hot Encoding...')
df_tmp = pd.Series(col_list_cond).str.join(',').str.split(',',expand = True).apply(pd.Series.value_counts, 1).iloc[:,:].fillna(0)

# Save unique list of generic_names
unique_entries_generic_name = unique_entries

# clean up
if '5%' in list(df_tmp.columns):
    df_tmp = df_tmp.drop(['5%'], axis=1)
if '' in list(df_tmp.columns):
    df_tmp = df_tmp.drop([''], axis = 1)

# start the final df
entries_len.append(len(df_tmp.columns))
df_ML = df_tmp.copy()
elapsed = timeit.default_timer() - start_time
print('Done with "{a}" in {b:0.2f} minutes.'.format(a = test_col, b = elapsed/60))
print('\n')

### drug_char
# one-hot-encode
test_col = 'drug_char'
print('Working on "{}"...'.format(test_col))
start_time = timeit.default_timer()

df_tmp = one_hot_encode_drugs(test_col, df)

# clean up
df_tmp = df_tmp.drop(['Unknown'], axis = 1)

# join to the rest
entries_len.append(len(df_tmp.columns))
df_ML = pd.concat([df_ML, df_tmp], axis=1, join_axes=[df_ML.index])
elapsed = timeit.default_timer() - start_time
print('Done with "{a}" in {b:0.2f} minutes.'.format(a = test_col, b = elapsed/60))
print('\n')

### drug_indication
test_col = 'drug_indication'
print('Working on "{}"...'.format(test_col))
start_time = timeit.default_timer()
### One-hot-encode with condensed input
# Generate list of unique drugs
unique_entries = unique_gen(test_col, df)
# Condense this list to a lower dimensional space
cond_dict = entry_condenser(unique_entries, 25)
# Get raw columns as a nested list
col_as_list = entries_col_to_lists(test_col, df)
# Convert raw column to lower-d space
col_list_cond = [[[cond_dict[l1] for l1 in l2 if l1 in cond_dict.keys()] for l2 in l3] for l3 in col_as_list]
# Unnest the lowest list
col_list_cond = [[x for y in entry for x in y] for entry in col_list_cond]

# One hot encoder
# For more information, see the following link:
# https://stackoverflow.com/questions/46864816/convert-data-frame-of-comma-separated-strings-to-one-hot-encoded
print('One Hot Encoding...')
df_tmp = pd.Series(col_list_cond).str.join(',').str.split(',',expand = True).apply(pd.Series.value_counts, 1).iloc[:,:].fillna(0)
# Save unique list of drug indication
unique_entries_drug_indication = unique_entries

# clean up
if '' in list(df_tmp.columns):
    df_tmp = df_tmp.drop([''], axis = 1)

# join to the rest
entries_len.append(len(df_tmp.columns))
df_ML = pd.concat([df_ML, df_tmp], axis=1, join_axes=[df_ML.index])

elapsed = timeit.default_timer() - start_time
print('Done with "{a}" in {b:0.2f} minutes.'.format(a = test_col, b = elapsed/60))
print('\n')

### Admin_route
test_col = 'admin_route'
print('Working on "{}"...'.format(test_col))
start_time = timeit.default_timer()
# one-hot-encode
df_tmp = one_hot_encode_drugs(test_col, df)

# Clean up
if 'Unknown' in list(df_tmp.columns):
    df_tmp = df_tmp.drop(['Unknown'], axis = 1)
if 'Not Listed' in list(df_tmp.columns):
    df_tmp = df_tmp.drop(['Not Listed'], axis = 1)

# join to the rest
entries_len.append(len(df_tmp.columns))
df_ML = pd.concat([df_ML, df_tmp], axis=1, join_axes=[df_ML.index])

elapsed = timeit.default_timer() - start_time
print('Done with "{a}" in {b:0.2f} minutes.'.format(a = test_col, b = elapsed/60))
print('\n')

### reaction_medDRA
test_col = 'reaction_medDRA_pt'
print('Working on "{}"...'.format(test_col))
start_time = timeit.default_timer()

### One-hot-encode with condensed input
# Generate list of unique drugs
unique_entries = unique_gen(test_col, df)
# Condense this list to a lower dimensional space
cond_dict = entry_condenser(unique_entries, 25)
# Get raw columns as a nested list
col_as_list = entries_col_to_lists(test_col, df)
# Convert raw column to lower-d space
col_list_cond = [[[cond_dict[l1] for l1 in l2 if l1 in cond_dict.keys()] for l2 in l3] for l3 in col_as_list]
# Unnest the lowest list
col_list_cond = [[x for y in entry for x in y] for entry in col_list_cond]

# One hot encoder
# For more information, see the following link:
# https://stackoverflow.com/questions/46864816/convert-data-frame-of-comma-separated-strings-to-one-hot-encoded
print('One Hot Encoding...')
if model_num == "X_1":
    df_tmp = pd.Series(col_list_cond).str.join(',').str.split(',',expand = True).apply(pd.Series.value_counts, 1).iloc[:,:].fillna(0)

if model_num == "X_3":
    col_as_list = [[x for y in entry for x in y] for entry in col_as_list]
    df_tmp = pd.Series(col_as_list).str.join(',').str.split(',',expand = True).apply(pd.Series.value_counts, 1).iloc[:,:].fillna(0)

# clean up
if '' in list(df_tmp.columns):
    df_tmp = df_tmp.drop([''], axis = 1)

# joing to the rest
entries_len.append(len(df_tmp.columns))
df_ML = pd.concat([df_ML, df_tmp], axis=1, join_axes=[df_ML.index])
elapsed = timeit.default_timer() - start_time
print('Done with "{a}" in {b:0.2f} minutes.'.format(a = test_col, b = elapsed/60))
print('\n')

# Add in the outcome variables
print('Adding in the outcome variables.')
df_outcomes = df[['serious', 'seriousness_congential_anomali',
         'seriousness_death', 'seriousness_disabling', 'seriousness_hospitalization',
         'seriousness_lifethreatening', 'seriousness_other']]

df_ML = pd.concat([df_ML, df_outcomes], axis = 1, join_axes = [df_ML.index])

# Convert all columns to numeric
df_ML = df_ML.apply(pd.to_numeric)
df_ML['serious'] = df_ML['serious'] - 1
print('Saving the files.')
# Save as a csv
if save_df or save_all:
    df_ML_filename = './progress/modeling/df_ML_model_' + model_num + '.csv'
    df_ML.to_csv(df_ML_filename)

entries = list(df_ML.columns)
# save the entries
if save_entries or save_all:
    entries_filename = './progress/modeling/entries_' + model_num + '.txt'
    with open(entries_filename, "wb") as fp:   #Pickling
        pickle.dump(entries, fp)

# save the length of entries sections
if save_entries_len or save_all:
    entires_len_filename = "./progress/modeling/entries_len_" + model_num + ".txt"
    with open(entires_len_filename, "wb") as fp:   #Pickling
        pickle.dump(entries_len, fp)


# save the unique entries for generic_name
if save_unique_gn or save_all:
    with open("./progress/modeling/unique_generic_name.txt", "wb") as fp:
        pickle.dump(unique_entries_generic_name, fp)

# save the unique entries for drug_indication
if save_unique_di or save_all:
    with open("./progress/modeling/unique_drug_indication.txt", "wb") as fp:
        pickle.dump(unique_entries_drug_indication, fp)

print("Congratulations! You made it through the code!")
