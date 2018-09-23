import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

# modeling functions
def RF_pred(df, test_col):
    """
    This function takes in a df output from 'FDA_wrangling' and a test_outcome (serious, etc.)
    and returns a RF model and metrics
    """

    # Drop all outcomes except that of interest
    all_cols = ['serious', 'seriousness_congential_anomali', 'seriousness_death',
                  'seriousness_disabling', 'seriousness_hospitalization',
                  'seriousness_lifethreatening', 'seriousness_other']
    # make sure the test_col is legit
    if test_col not in all_cols:
        print('Invalid input')
        return
    # drop all columns except test_col
    drop_cols = [col for col in all_cols if col != test_col]
    df = df.drop(drop_cols, axis = 1)

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(df.drop([test_col], axis = 1),
                                                    df[test_col].astype('category'),
                                                    test_size = 0.33,
                                                    random_state = 189)

    # Create a random forest Classifier. By convention, clf means 'Classifier'
    clf = RandomForestClassifier(n_estimators = 100, random_state=189)
    # Train the Classifier
    clf.fit(X_train, y_train)
    # Apply the Classifier we trained to the train and test data
    y_preds_train = clf.predict(X_train)
    y_preds_test = clf.predict(X_test)

    # List of feature importances
    # View a list of the features and their importance scores
    rf_list = list(zip(X_train, clf.feature_importances_))

    # get the results
    results, cm_train, cm_test, prfs_train, prfs_test = results_out(y_train, y_test, y_preds_train, y_preds_test)

    return clf, results, rf_list, cm_train, cm_test, prfs_train, prfs_test



def LR_pred(df, test_col):
    """
    This function takes in a df output from 'FDA_wrangling' and a test_outcome (serious, etc.)
    and returns a LR model and metrics
    """
    # Drop all outcomes except that of interest
    all_cols = ['serious', 'seriousness_congential_anomali', 'seriousness_death',
                  'seriousness_disabling', 'seriousness_hospitalization',
                  'seriousness_lifethreatening', 'seriousness_other']
    # make sure the test_col is legit
    if test_col not in all_cols:
        print('Invalid input')
        return
    # drop all columns except test_col
    drop_cols = [col for col in all_cols if col != test_col]
    df = df.drop(drop_cols, axis = 1)

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(df.drop([test_col], axis = 1),
                                                    df[test_col].astype('category'),
                                                    test_size = 0.33,
                                                    random_state = 189)

    # Create a model
    LR = LogisticRegression('l2', random_state=189)
    # Train the Classifier
    LR.fit(X_train, y_train)
    # Apply the Classifier we trained to the train and test data
    y_preds_train = LR.predict(X_train)
    y_preds_test = LR.predict(X_test)

    # get the results
    results, cm_train, cm_test, prfs_train, prfs_test = results_out(y_train, y_test, y_preds_train, y_preds_test)

    return LR, results, cm_train, cm_test, prfs_train, prfs_test


def NB_pred(df, test_col):
    """
    This function takes in a df output from 'FDA_wrangling' and a test_outcome (serious, etc.)
    and returns a NB model and metrics
    """
    # Drop all outcomes except that of interest
    all_cols = ['serious', 'seriousness_congential_anomali', 'seriousness_death',
                  'seriousness_disabling', 'seriousness_hospitalization',
                  'seriousness_lifethreatening', 'seriousness_other']
    # make sure the test_col is legit
    if test_col not in all_cols:
        print('Invalid input')
        return
    # drop all columns except test_col
    drop_cols = [col for col in all_cols if col != test_col]
    df = df.drop(drop_cols, axis = 1)

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(df.drop([test_col], axis = 1),
                                                    df[test_col].astype('category'),
                                                    test_size = 0.33,
                                                    random_state = 189)

    # Create a Classifier. By convention, clf means 'Classifier'
    NB = GaussianNB(priors = None)
    # Train the Classifier
    NB.fit(X_train, y_train)
    # Apply the Classifier we trained to the train and test data
    y_preds_train = NB.predict(X_train)
    y_preds_test = NB.predict(X_test)

    # get the results
    results, cm_train, cm_test, prfs_train, prfs_test = results_out(y_train, y_test, y_preds_train, y_preds_test)

    return NB, results, cm_train, cm_test, prfs_train, prfs_test

    ##################


def results_out(y_train, y_test, y_preds_train, y_preds_test):
    """
    This function generates the relevant metrics for test, train and prediction sets
    """
    # Confusion matrix for training set
    cm_train = confusion_matrix(y_train, y_preds_train)
    cm_train = pd.DataFrame(cm_train)
    cm_train.columns = ['Negative', 'Positive']
    cm_train.index = cm_train.columns
    # Confusion matrix for test set
    cm_test = confusion_matrix(y_test, y_preds_test)
    cm_test = pd.DataFrame(cm_test)
    cm_test.columns = ['Negative', 'Positive']
    cm_test.index = cm_test.columns
    # Model accuracy
    acc_train = np.trace(np.asarray(cm_train))/len(y_train)
    acc_test = np.trace(np.asarray(cm_test))/len(y_test)
    fraction_pos = sum(y_train)/len(y_train)
    # Output metrics for train set
    prfs_train = precision_recall_fscore_support(y_train, y_preds_train)
    prfs_train = np.array([prfs_train[0], prfs_train[1], prfs_train[2], prfs_train[3]])
    prfs_train = pd.DataFrame(prfs_train)
    prfs_train.columns = ['Negative', 'Positive']
    prfs_train.index = ['Precision','Recall','F-score','Support']
    # Output metrics for train set
    prfs_test = precision_recall_fscore_support(y_test, y_preds_test)
    prfs_test = np.array([prfs_test[0], prfs_test[1], prfs_test[2], prfs_test[3]])
    prfs_test = pd.DataFrame(prfs_test)
    prfs_test.columns = ['Negative', 'Positive']
    prfs_test.index = ['Precision','Recall','F-score','Support']

    # Consolidate results
    results = [
        acc_train*100,
        prfs_train['Negative'][1], prfs_train['Positive'][1],
        prfs_train['Negative'][0], prfs_train['Positive'][0],
        prfs_train['Negative'][2], prfs_train['Positive'][2],
        acc_test*100,
        prfs_test['Negative'][1], prfs_test['Positive'][1],
        prfs_test['Negative'][0], prfs_test['Positive'][0],
        prfs_test['Negative'][2], prfs_test['Positive'][2],
        fraction_pos*100
    ]

    return results, cm_train, cm_test, prfs_train, prfs_test


def cluster_models(df, test_col, num_clusters = 10):
    """
    Returns the clusters of a positive cases of the designated outcome
    """
    # Only consider the positive cases of the test_col
    df = df[df[test_col] >= 1]
    # drop all outcome cols
    drop_cols = ['serious', 'seriousness_congential_anomali', 'seriousness_death',
              'seriousness_disabling', 'seriousness_hospitalization',
              'seriousness_lifethreatening', 'seriousness_other']
    df = df.drop(drop_cols, axis = 1)

    # Set up a KMeans model with num_clusters paradigmatic patients
    clus = KMeans(n_clusters = num_clusters, random_state = 189)
    # fit the model
    clus.fit(df)
    # return the model
    return clus


##########
