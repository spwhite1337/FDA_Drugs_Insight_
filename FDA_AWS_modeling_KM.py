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


### CLUSTERING

# Run the clustering process
test_cols = ['serious', 'seriousness_death',
              'seriousness_disabling', 'seriousness_hospitalization',
              'seriousness_lifethreatening']

KM_models = []
print('Running the KMeans Clustering')
for col in test_cols:
    start_time = timeit.default_timer()
    print('Predicting "{}".'.format(col))
    KM = cluster_models(df, col)
    KM_models.append(KM)
    elapsed = timeit.default_timer() - start_time
    print('Done with "{a}" in {b:0.2f} minutes.'.format(a = col, b = elapsed/60))
    print('\n')

# Save the models
if save_models_KM or save_all:
    i = 0
    for col in test_cols:
        with open(model_filename_KM + col + '.pkl', "wb") as fp:   #Pickling
            pickle.dump(KM_models[i], fp)
        i = i + 1


print('Congratulations! You made it through the code!!')
