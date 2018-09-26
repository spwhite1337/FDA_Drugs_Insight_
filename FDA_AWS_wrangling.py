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

# Make dirs
if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists('progress'):
    os.makedirs('progress')

if not os.path.exists('progress/wrangled'):
    os.makedirs('progress/wrangled')

if not os.path.exists('progress/modeling'):
    os.makedirs('progress/modeling')

if not os.path.exists('progress/wrangled/percent_1'):
    os.makedirs('progress/wrangled/percent_1')

### 1. DOWNLOAD THE DATA

# Archive of downloadable links from FDA
# Data are available for download at this site: https://open.fda.gov/tools/downloads/

# For a cursory look at the data, see this link
# https://open.fda.gov/apis/drug/event/explore-the-api-with-an-interactive-chart/

# For information on entries see this link
# https://open.fda.gov/apis/drug/event/searchable-fields

jsonurl = 'https://api.fda.gov/download.json'
with urllib.request.urlopen(jsonurl) as url:
    data = json.loads(url.read().decode())

# Entries of downloadable files
# 760 in total

# Index key:
# 2004 Q1: 4:8
# 2004 Q2: 8:13
# 2004 Q3: 13:18
# 2004 Q4: 18:23
# 2005 Q1: 23:28
# 2005 Q2: 28:33
# 2005 Q3: 33:38
# 2005 Q4: 38:43
# 2006 Q1: 43:49
# 2006 Q2: 49:54
# 2006 Q3: 54:59
# 2006 Q4: 59:64
# 2007 Q1: 64:70
# 2007 Q2: 70:76
# 2007 Q3: 76:83
# 2007 Q4: 83:89
# 2008 Q1: 89:97
# 2008 Q2: 97:104
# 2008 Q3: 104:111
# 2008 Q4: 111:117
# 2009 Q1: 117:124
# 2009 Q2: 124:132
# 2009 Q3: 132:140
# 2009 Q4: 140:147
# 2010 Q1: 147:156
# 2010 Q2: 156:165
# 2010 Q3: 165:175
# 2010 Q4: 175:185
# 2011 Q1: 185:196
# 2011 Q2: 196:208
# 2011 Q3: 208:219
# 2011 Q4: 219:229
# 2012 Q1: 229:238
# 2012 Q2: 238:249
# 2012 Q3: 249:256
# 2012 Q4: 256:271
# 2013 Q1: 271:289
# 2013 Q2: 289:303
# 2013 Q3: 303:319
# 2013 Q4: 319:338
# 2014 Q1: 338:358
# 2014 Q2: 358:374
# 2014 Q3: 374:391
# 2014 Q4: 391:408
# 2015 Q1: 408:433
# 2015 Q2: 433:456
# 2015 Q3: 456:488
# 2015 Q4: 488:513
# 2016 Q1: 513:542
# 2016 Q2: 542:566
# 2016 Q3: 566:590
# 2016 Q4: 590:613
# 2017 Q1: 613:640
# 2017 Q2: 640:666
# 2017 Q3: 666:693
# 2017 Q4: 693:720
# 2018 Q1: 720:753
# 2018 Q2: 753:791

partitions = data['results']['drug']['event']['partitions']
# Display a few partitions

total_records = 0
total_size = 0
urls = []
partitions_slice = partitions
for entry in partitions_slice:
    urls.append(entry['file'])
    total_records = total_records + entry['records']
    total_size = total_size + float(entry['size_mb'])
print('{records:0.2f} million records for a total size of {size:0.2f} GB'.format(records = total_records/10**6, size = total_size/1000))


# Save compressed files in data folder
file_name = []
j = 0
#for i in range(0,len(urls)): # This goes through all the data
print('Progress...')
for i in range(601,602):
    start_time = timeit.default_timer()
    print('File {num} with size = {size} MB downloading...'.format(num = i, size = partitions[i]['size_mb']))
    url = urls[i] # Get the url
    # Define the filename for the data folder
    file_name.append('./data/' + url.split('/')[-2] + '_' + url.split('/')[-1])
    # Download the data and save it to the data folder
    with urllib.request.urlopen(url) as response, open(file_name[j], 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    j += 1
    elapsed = timeit.default_timer() - start_time
    print('Completed in {time:0.2f} seconds'.format(time = elapsed))
print('Done.')



# Unzip the data
data_2 = []
data_inter = None
j = 0
# Run through sample
print('Progress...')
for j in range(0,len(file_name)):
    start_time = timeit.default_timer()
    with zipfile.ZipFile((file_name[j]), "r") as z: # get the .zip file
        for filename in z.namelist():
            with z.open(filename) as f:  # Open the file
                print('File {iterable} of {total} loading...'.format(iterable = j+1, total = len(file_name)))  # print a progress check
                data_inter = f.read()   # read the file
                data_2.append(json.loads(data_inter.decode("utf-8"))) # decode and save
                elapsed = timeit.default_timer() - start_time
                print('{num_records} records loaded in {time:0.2f} seconds.'.format(num_records = len(data_2[j]['results']), time= elapsed))
print('Done.')


# File information
type_file = type(data_2)
type_entry = type(data_2[0]['results'][0])

size = 0
for i in range(0, len(data_2)):
    for j in range(0, len(data_2[i]['results'])):
        size = size + sys.getsizeof(data_2[i]['results'][j])
print('data_2 is a {} where entries of data_2[0][\'results\'][0] are {}'.format(type_file, type_entry))
print('Approximate Size of packed file is {size:.2f} MB'.format(size = size/10**6))

# File information
type_file = type(data_2)
type_entry = type(data_2[0]['results'][0])

size = 0
for i in range(0, len(data_2)):
    for j in range(0, len(data_2[i]['results'])):
        size = size + sys.getsizeof(data_2[i]['results'][j])
print('Number of files = {}'.format(len(file_name)))
print('data_2 is a {} where entries of data_2[0][\'results\'][0] are {}'.format(type_file, type_entry))
print('Approximate Size of packed file is {size:.2f} MB'.format(size = size/10**6))

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


### 3. CUSTOMIZE DATAFRAME

# Drop unnecessary columns
df = df[['patient_onset_age', 'patient_weight', 'patient_sex', 'generic_name', 'drug_char',
         'drug_indication', 'admin_route', 'reaction_medDRA_pt', 'serious', 'seriousness_congential_anomali',
         'seriousness_death', 'seriousness_disabling', 'seriousness_hospitalization',
         'seriousness_lifethreatening', 'seriousness_other']]

# Check percent of missing values
df.replace('NA', np.nan).isna().sum()/len(df)

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

print('\n')
print("Congratulations! You made it through the code!")
