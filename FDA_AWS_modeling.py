import pandas as pd
import numpy as np
import pickle

from helper_funcs.model_preds import RF_pred, LR_pred, NB_pred, cluster_models

# Set up filenames (have to run wrangling function first)
model_num = ['X_1', 'X_2', 'X_3']
model_num = model_num[0]

file_to_read = 'progress/modeling/df_ML_model_' + model_num + '.csv'

save_all = False

save_models_RF = True
model_filename_RF = './progress/modeling/RF_' + model_num + '_' # + [outcome].pkl
save_models_LR = True
model_filename_LR = './progress/modeling/LR_' + model_num + '_' # + [outcome].pkl
save_models_NB = True
model_filename_NB = './progress/modeling/NB_' + model_num + '_' # + [outcome].pkl
save_models_KM = True
model_filename_KM = './progress/modeling/KM_' + model_num + '_' # + [outcome].pkl

save_results_RF = False
file_for_results_RF = 'progress/modeling/RF_' + model_num + '_results.csv'
save_results_LR = False
file_for_results_LR = 'progress/modeling/LR_' + model_num + '_results.csv'
save_results_NB = False
file_for_results_NB = 'progress/modeling/NB_' + model_num + '_results.csv'



save_rf_lists = False
file_for_rf_lists = 'progress/modeling/RF_' + model_num + '_rflist_' # + [outcome].pkl


# Read in the data from Wrangling
df = pd.read_csv(file_to_read, index_col = 0)


### RANDOM FOREST

# Run a Random Forest for all Outcomes in a given df
test_cols = ['serious', 'seriousness_death',
              'seriousness_disabling', 'seriousness_hospitalization',
              'seriousness_lifethreatening']

RF_models = []
RF_results = []
RF_rf_lists = []
RF_cm_train = []
RF_cm_test = []
RF_prfs_train = []
RF_prfs_test = []
for col in test_cols:
    RF, results, rf_list, cm_train, cm_test, prfs_train, prfs_test = RF_pred(df, col)
    RF_models.append(RF)
    RF_results.append(results)
    RF_rf_lists.append(rf_list)
    RF_cm_train.append(cm_train)
    RF_cm_test.append(cm_test)
    RF_prfs_train.append(prfs_train)
    RF_prfs_test.append(prfs_test)


# Save the models
if save_models_RF or save_all:
    i = 0
    for col in test_cols:
        with open(model_filename_RF + col + '.pkl', "wb") as fp:   #Pickling
            pickle.dump(RF_models[i], fp)
        i = i + 1

# Save the rf_lists
if save_rf_lists or save_all:
    i = 0
    for col in test_cols:
        with open(file_for_rf_lists + col + '.pkl', "wb") as fp:   #Pickling
            pickle.dump(RF_rf_lists[i], fp)
        i = i + 1


# Convert results to a nice df
results = pd.DataFrame([RF_results[0], RF_results[1], RF_results[2], RF_results[3], RF_results[4]]).transpose()
results['names'] = pd.DataFrame(['Train_acc',
                                 'Train_Recall_0', 'Train_Recall_1', 'Train_Precision_0',
                                 'Train_Precision_1', 'Train_Fscore_0', 'Train_Fscore_1',
                                 'Test_acc',
                                 'Test_Recall_0', 'Test_Recall_1','Test_Precision_0',
                                 'Test_Precision_1', 'Test_Fscore_0', 'Test_Fscore_1',
                                 'Percent_positive'])
results = results.set_index('names')
results.columns = ['RF_1_1_Serious', 'RF_1_1_Death', 'RF_1_1_Disabling', 'RF_1_1_Hospital', 'RF_1_1_LT']

# Save results for RF
if save_results_RF or save_all:
    results.to_csv(file_for_results_RF)


### LOGISTIC REGRESSION

# Run a Logistic Regression for all Outcomes in a given df
test_cols = ['serious', 'seriousness_death',
              'seriousness_disabling', 'seriousness_hospitalization',
              'seriousness_lifethreatening']

LR_models = []
LR_results = []
LR_rf_lists = []
LR_cm_train = []
LR_cm_test = []
LR_prfs_train = []
LR_prfs_test = []
for col in test_cols:
    LR, results, cm_train, cm_test, prfs_train, prfs_test = LR_pred(df, col)
    LR_models.append(LR)
    LR_results.append(results)
    LR_rf_lists.append(rf_list)
    LR_cm_train.append(cm_train)
    LR_cm_test.append(cm_test)
    LR_prfs_train.append(prfs_train)
    LR_prfs_test.append(prfs_test)

# Save the models
if save_models_LR or save_all:
    i = 0
    for col in test_cols:
        with open(model_filename_LR + col + '.pkl', "wb") as fp:   #Pickling
            pickle.dump(LR_models[i], fp)
        i = i + 1

# Convert results to a nice df
results = pd.DataFrame([LR_results[0], LR_results[1], LR_results[2], LR_results[3], LR_results[4]]).transpose()
results['names'] = pd.DataFrame(['Train_acc',
                                 'Train_Recall_0', 'Train_Recall_1', 'Train_Precision_0',
                                 'Train_Precision_1', 'Train_Fscore_0', 'Train_Fscore_1',
                                 'Test_acc',
                                 'Test_Recall_0', 'Test_Recall_1','Test_Precision_0',
                                 'Test_Precision_1', 'Test_Fscore_0', 'Test_Fscore_1',
                                 'Percent_positive'])
results = results.set_index('names')
results.columns = ['LR_1_1_Serious', 'LR_1_1_Death', 'LR_1_1_Disabling', 'LR_1_1_Hospital', 'LR_1_1_LT']

# Save results for LR
if save_results_LR or save_all:
    results.to_csv(file_for_results_LR)


### NAIVE BAYES

# Run a Naive Bayes for all Outcomes in a given df
test_cols = ['serious', 'seriousness_death',
              'seriousness_disabling', 'seriousness_hospitalization',
              'seriousness_lifethreatening']

NB_models = []
NB_results = []
NB_rf_lists = []
NB_cm_train = []
NB_cm_test = []
NB_prfs_train = []
NB_prfs_test = []
for col in test_cols:
    NB, results, cm_train, cm_test, prfs_train, prfs_test = NB_pred(df, col)
    NB_models.append(NB)
    NB_results.append(results)
    NB_rf_lists.append(rf_list)
    NB_cm_train.append(cm_train)
    NB_cm_test.append(cm_test)
    NB_prfs_train.append(prfs_train)
    NB_prfs_test.append(prfs_test)

# Convert results to a nice df
results = pd.DataFrame([NB_results[0], NB_results[1], NB_results[2], NB_results[3], NB_results[4]]).transpose()
results['names'] = pd.DataFrame(['Train_acc',
                                 'Train_Recall_0', 'Train_Recall_1', 'Train_Precision_0',
                                 'Train_Precision_1', 'Train_Fscore_0', 'Train_Fscore_1',
                                 'Test_acc',
                                 'Test_Recall_0', 'Test_Recall_1','Test_Precision_0',
                                 'Test_Precision_1', 'Test_Fscore_0', 'Test_Fscore_1',
                                 'Percent_positive'])
results = results.set_index('names')
results.columns = ['NB_1_1_Serious', 'NB_1_1_Death', 'NB_1_1_Disabling', 'NB_1_1_Hospital', 'NB_1_1_LT']

# Save results for NB
if save_results_NB or save_all:
    results.to_csv(file_for_results_NB)

### CLUSTERING

# Run the clustering process
test_cols = ['serious', 'seriousness_death',
              'seriousness_disabling', 'seriousness_hospitalization',
              'seriousness_lifethreatening']

KM_models = []
for col in test_cols:
    KM = cluster_models(df, col)
    KM_models.append(KM)

# Save the models
if save_models_KM or save_all:
    i = 0
    for col in test_cols:
        with open(model_filename_KM + col + '.pkl', "wb") as fp:   #Pickling
            pickle.dump(KM_models[i], fp)
        i = i + 1
