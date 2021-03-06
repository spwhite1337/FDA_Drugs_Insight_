import pandas as pd
import numpy as np
import pickle
import timeit

from helper_funcs.model_preds import RF_pred, LR_pred, NB_pred, cluster_models

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Set up filenames (have to run wrangling function first)
model_num = ['X_1', 'X_2', 'X_3']
model_num = model_num[0]

file_to_read = 'progress/modeling/df_ML_model_' + model_num + '.csv'

save_all = True

save_models_RF = False
model_filename_RF = './progress/modeling/RF_' + model_num + '_' # + [outcome].pkl
save_models_LR = False
model_filename_LR = './progress/modeling/LR_' + model_num + '_' # + [outcome].pkl
save_models_NB = False
model_filename_NB = './progress/modeling/NB_' + model_num + '_' # + [outcome].pkl
save_models_KM = False
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
print('Reading in the df...')
start_time = timeit.default_timer()
df = pd.read_csv(file_to_read, index_col = 0)
elapsed = timeit.default_timer() - start_time
print('Done in {a:0.2f} seconds.'.format(a = elapsed))

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
print('Running the Naive Bayes Classifier')
for col in test_cols:
    start_time = timeit.default_timer()
    print('Predicting "{}".'.format(col))
    NB, results, cm_train, cm_test, prfs_train, prfs_test = NB_pred(df, col)
    NB_models.append(NB)
    NB_results.append(results)
    NB_cm_train.append(cm_train)
    NB_cm_test.append(cm_test)
    NB_prfs_train.append(prfs_train)
    NB_prfs_test.append(prfs_test)
    elapsed = timeit.default_timer() - start_time
    print('Done with "{a}" in {b:0.2f} minutes.'.format(a = col, b = elapsed/60))
    print('\n')

# Save the models
if save_models_NB or save_all:
    i = 0
    for col in test_cols:
        with open(model_filename_NB + col + '.pkl', "wb") as fp:   #Pickling
            pickle.dump(NB_models[i], fp)
        i = i + 1

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



print('Congratulations! You made it through the code!!')
