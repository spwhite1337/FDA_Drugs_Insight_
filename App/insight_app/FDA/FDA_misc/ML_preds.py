import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pandas as pd
import numpy as np
import pickle
# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

model_num = "X_1"

# Load the feature sets
with open("FDA/FDA_misc/entries_" + model_num + '.txt', "rb") as fp:
    entries_1_1 = pickle.load(fp)
entries = entries_1_1

# Load the model for prediction
with open("FDA/FDA_misc/models/LR_" + model_num + "_serious.pkl", "rb") as fp:   # Unpickling
    LR_serious = pickle.load(fp)
with open("FDA/FDA_misc/models/LR_" + model_num + "_seriousness_death.pkl", "rb") as fp:   # Unpickling
    LR_death = pickle.load(fp)
with open("FDA/FDA_misc/models/LR_" + model_num + "_seriousness_disabling.pkl", "rb") as fp:   # Unpickling
    LR_disabling = pickle.load(fp)
with open("FDA/FDA_misc/models/LR_" + model_num + "_seriousness_hospitalization.pkl", "rb") as fp:   # Unpickling
    LR_hospital = pickle.load(fp)
with open("FDA/FDA_misc/models/LR_" + model_num + "_seriousness_lifethreatening.pkl", "rb") as fp:   # Unpickling
    LR_lifethreatening = pickle.load(fp)

# load the model for clustering
# For serious
with open("FDA/FDA_misc/models/KM_" + model_num + "_serious.pkl", "rb") as fp:
    cluster_serious = pickle.load(fp)
# For death
with open("FDA/FDA_misc/models/KM_" + model_num + "_seriousness_death.pkl", "rb") as fp:
    cluster_death = pickle.load(fp)
# For Disabling
with open("FDA/FDA_misc/models/KM_" + model_num + "_seriousness_disabling.pkl", "rb") as fp:
    cluster_disabling = pickle.load(fp)
# For hospitalization
with open("FDA/FDA_misc/models/KM_" + model_num + "_seriousness_hospitalization.pkl", "rb") as fp:
    cluster_hospital = pickle.load(fp)
# For lifethreatening
with open("FDA/FDA_misc/models/KM_" + model_num + "_seriousness_lifethreatening.pkl", "rb") as fp:
    cluster_lifethreatening = pickle.load(fp)


# Generate RF preds
# def RF_pred(vec_input):
#     """
#     Returns the set of probabilities for the range of outcomes from the RF model
#     """
#     # Return the probability that the results is not serious
#     serious_prob = round(RF_1_1_serious.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
#     death_prob = round(RF_1_1_death.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
#     disabling_prob = round(RF_1_1_disabling.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
#     hospital_prob = round(RF_1_1_hospital.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
#     lifethreatening_prob = round(RF_1_1_lifethreatening.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
#     # return the list
#     type_probs = ['Serious', 'Death', 'Disabling', 'Hospitalization', 'Life Threatening']
#     probs = [serious_prob, death_prob, disabling_prob, hospital_prob, lifethreatening_prob]
#     probs = [100-x for x in probs]
#     prob_output = zip(type_probs, probs)
#     return probs

# Generate LR preds
def LR_pred(vec_input):
    """
    Returns the set of probabilities for the range of outcomes from the RF model
    """
    # Return the probability that the results is not serious
    serious_prob = round(LR_serious.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
    death_prob = round(LR_death.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
    disabling_prob = round(LR_disabling.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
    hospital_prob = round(LR_hospital.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
    lifethreatening_prob = round(LR_lifethreatening.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
    # return the list
    type_probs = ['Serious', 'Death', 'Disabling', 'Hospitalization', 'Life Threatening']
    probs = [serious_prob, death_prob, disabling_prob, hospital_prob, lifethreatening_prob]
    probs = [100-x for x in probs]
    prob_output = zip(type_probs, probs)
    return probs

# Generate recommendation based on clusters
def cluster_pred(vec_input, outcome = "serious"):
    """
    Returns the recommended features to avoid from the clustered patients
    """
    # get the centers for Paradigmatic patients
    if outcome == "serious":
        patient_centers = cluster_serious.cluster_centers_
        test_label = cluster_serious.predict(vec_input.reshape(1,-1))
    if outcome == "death":
        patient_centers = cluster_death.cluster_centers_
        test_label = cluster_death.predict(vec_input.reshape(1,-1))
    if outcome == "disabling":
        patient_centers = cluster_disabling.cluster_centers_
        test_label = cluster_disabling.predict(vec_input.reshape(1,-1))
    if outcome == "hospital":
        patient_centers = cluster_hospital.cluster_centers_
        test_label = cluster_hospital.predict(vec_input.reshape(1,-1))
    if outcome == "lifethreatening":
        patient_centers = cluster_lifethreatening.cluster_centers_
        test_label = cluster_lifethreatening.predict(vec_input.reshape(1,-1))

    # Paradigmatic patient most similar
    # get the values where the input vec is zero for the most similar patient
    arr = patient_centers[test_label[0]][np.where(vec_input == 0)]
    # largest features where the input entry is zero, "those to avoid"
    max_feats = arr.argsort()[-10:][::-1]
    recommends = [entries[i] for i in max_feats] # Change this if you change entries
    # return it
    return recommends
