import pandas as pd
import numpy as np
import pickle
# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestClassifier

# Load the feature sets
with open("FDA/FDA_misc/entries_1_1.txt", "rb") as fp:
    entries_1_1 = pickle.load(fp)

# Load the model for prediction
with open("FDA/FDA_misc/models/RF_1_1_serious.pkl", "rb") as fp:   # Unpickling
    RF_1_1_serious = pickle.load(fp)
with open("FDA/FDA_misc/models/RF_1_1_death.pkl", "rb") as fp:   # Unpickling
    RF_1_1_death = pickle.load(fp)
with open("FDA/FDA_misc/models/RF_1_1_disabling.pkl", "rb") as fp:   # Unpickling
    RF_1_1_disabling = pickle.load(fp)
with open("FDA/FDA_misc/models/RF_1_1_hospital.pkl", "rb") as fp:   # Unpickling
    RF_1_1_hospital = pickle.load(fp)
with open("FDA/FDA_misc/models/RF_1_1_lifethreatening.pkl", "rb") as fp:   # Unpickling
    RF_1_1_lifethreatening = pickle.load(fp)

# load the model for clustering
with open("FDA/FDA_misc/models/cluster_1_1.pkl", "rb") as fp:
    cluster_1_1 = pickle.load(fp)



# Generate RF preds
def RF_pred(vec_input):
    """
    Returns the set of probabilities for the range of outcomes from the RF model
    """
    # Return the probability that the results is not serious
    serious_prob = round(RF_1_1_serious.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
    death_prob = round(RF_1_1_death.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
    disabling_prob = round(RF_1_1_disabling.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
    hospital_prob = round(RF_1_1_hospital.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
    lifethreatening_prob = round(RF_1_1_lifethreatening.predict_proba(vec_input.reshape(1,-1))[0][0],2)*100
    # return the list
    type_probs = ['Serious', 'Death', 'Disabling', 'Hospitalization', 'Life Threatening']
    probs = [serious_prob, death_prob, disabling_prob, hospital_prob, lifethreatening_prob]
    prob_output = zip(type_probs, probs)
    return prob_output

# Generate recommendation based on clusters
def cluster_pred(vec_input):
    """
    Returns the recommended features to avoid from the clustered patients
    """
    # get the centers for Paradigmatic patients
    patient_centers = cluster_1_1.cluster_centers_
    # Paradigmatic patient most similar
    test_label = cluster_1_1.predict(vec_input.reshape(1,-1))
    # get the values where the input vec is zero for the most similar patient
    arr = patient_centers[test_label[0]][np.where(vec_input == 0)]
    # largest features where the input entry is zero, "those to avoid"
    max_feats = arr.argsort()[-10:][::-1]
    recommends = [entries_1_1[i] for i in max_feats]
    # return it
    return recommends
