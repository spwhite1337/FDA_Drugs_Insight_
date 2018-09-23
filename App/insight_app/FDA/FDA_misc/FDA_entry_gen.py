import pandas as pd
import numpy as np
import pickle

from difflib import SequenceMatcher

# Select the model_num based on dataset and feature size
model_num = '1_1'
# get the feature set as a list
file_entries = 'FDA/FDA_misc/entries_' + model_num + '.txt'
with open(file_entries, "rb") as fp:   # Unpickling
    entries = pickle.load(fp)
entries = entries[:-7]
# Get the length of each feature type in the feature set
file_entries_len = 'FDA/FDA_misc/entries_len_' + model_num + '.txt'
with open(file_entries_len, "rb") as fp:   # Unpickling
    entries_len = pickle.load(fp)

### Actual Features used in the model
# generic_name
generic_name_list = entries[sum(entries_len[0:0]): sum(entries_len[0:1])]
# drug_char
drug_char_list = entries[sum(entries_len[0:1]): sum(entries_len[0:2])]
# drug_indication
drug_indication_list = entries[sum(entries_len[0:2]): sum(entries_len[0:3])]
# admin_route
admin_route_list = entries[sum(entries_len[0:3]): sum(entries_len[0:4])]
# reaction_medDRA
reaction_list = entries[sum(entries_len[0:4]): sum(entries_len[0:5])]
print(reaction_list)
# drug_char_entries
drug_char_entries = (
                (0, "--"),
                (1, "Suspect"),
                (2, "Benign"),
                )

### Features to pass to Forms
# All generic_names
with open('FDA/FDA_misc/generic_name_unique.txt', "rb") as fp:
    generic_name_all = pickle.load(fp)
# All drug_indication
with open('FDA/FDA_misc/drug_indication_unique.txt', "rb") as fp:
    drug_indication_all = pickle.load(fp)
# reaction_medDRA dicts
with open('FDA/FDA_misc/dict_LLT_PT.pkl', "rb") as fp:
    dict_LLT_PT = pickle.load(fp)
with open('FDA/FDA_misc/dict_PT_HLT.pkl', "rb") as fp:
    dict_PT_HLT = pickle.load(fp)
with open('FDA/FDA_misc/dict_HLT_HLGT.pkl', "rb") as fp:
    dict_HLT_HLGT = pickle.load(fp)
with open('FDA/FDA_misc/dict_HLGT_SOC.pkl', "rb") as fp:
    dict_HLGT_SOC = pickle.load(fp)
# list of reaction_medDRA as preferred terms
reaction_all = list(dict_PT_HLT.keys())

# Passed to views.py for form autocomplete
listed_features = [generic_name_all, admin_route_list, drug_indication_all, reaction_all]

# Function for mapping user_input to feature set
def query_match(query_in, query_cat):
    """
    This function takes in a list of entries for a given category and returns the most similar in the feature list by text.
    """
    # For reaction_medDRA, make sure it is in units of "SOC" or whatever the model feature list is in
    entry_query = []
    if query_cat == "reaction_medDRA":
        entries_list = reaction_list
        PT_list = list(dict_PT_HLT.keys())
        for query in query_in:
            query = query.upper()
            if query in PT_list: # convert it directly if in the keys
                query = dict_HLGT_SOC[dict_HLT_HLGT[dict_PT_HLT[query]]]
            else: # otherwise match the closest then convert
                num_1= []
                for entry in PT_list:
                    num_1.append(SequenceMatcher(None, query, entry).ratio())
                entry_index = num_conv.index(max(num_1))
                PT_nearest = PT_list[entry_index]
                query = dict_HLGT_SOC[dict_HLT_HLGT[dict_PT_HLT[PT_nearest]]]
            # Now we have query in units of "SOC"
            # Need one final matching by spelling to df features in case of error
            num_2 = []
            for entry in entries_list:
                num_2.append(SequenceMatcher(None, query, entry).ratio())
            # Get best matched entry
            entry_index = num_2.index(max(num_2))
            entry_query.append(entries_list[entry_index])

    else:
        # clean up input
        for query in query_in:
            # clean up input
            if query_cat == 'generic_name':
                query = query.upper()
                entries_list = generic_name_list

            # clean up input
            if query_cat == 'drug_indication':
                query = query.upper()
                entries_list = drug_indication_list

            # clean up input
            if query_cat == 'admin_route':
                query = query.title()
                entries_list = admin_route_list

            # get similarities
            num = []
            for entry in entries_list:
                num.append(SequenceMatcher(None, query, entry).ratio())
            # get best matched entry
            entry_index = num.index(max(num))
            entry_query.append(entries_list[entry_index])
    # return matched entry list
    return entry_query



# Convert to feature input for model
def feature_vec(feature_list):
    """
    Converts a list of features into a sparse vector for model input
    """
    # create list of indeces for each feature
    test_inputs = []
    for item in feature_list:
        if item in entries:
            test_inputs.append(entries.index(item))
        else:
            print('bad')
            print(item)
    # initialize vector of zeros with length = num features
    model_input = np.zeros(len(entries))
    # Set the identified indeces to 1.0
    model_input[test_inputs] = 1
    # return
    return model_input
