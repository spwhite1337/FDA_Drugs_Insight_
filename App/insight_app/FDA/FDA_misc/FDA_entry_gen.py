import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pandas as pd
import numpy as np
import pickle

from difflib import SequenceMatcher

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

model_num = "X_1"

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

# drug_char_entries
drug_char_entries = (
                (0, "--"),
                (1, "Suspect"),
                (2, "Benign"),
                )

### Features to pass to Forms
# All generic_names
with open('FDA/FDA_misc/unique_generic_name.txt', "rb") as fp:
    generic_name_all = pickle.load(fp)
# All drug_indication
with open('FDA/FDA_misc/unique_drug_indication.txt', "rb") as fp:
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
listed_features = [generic_name_all, admin_route_list, drug_indication_all, reaction_all, list(dict_PT_HLT.keys())]

# Function for mapping user_input to feature set
def query_match(query_in, query_cat):
    """
    This function takes in a list of entries for a given category and returns the most similar in the feature list by text.
    """
    # For reaction_medDRA, make sure it is in units of "SOC" or whatever the model feature list is in
    entry_query = []
    # clean up input
    for query in query_in:
        # clean up input
        if query_cat == 'generic_name':
            query = query.upper()
            entries_list = generic_name_list

        # clean up input
        elif query_cat == 'drug_indication':
            query = query.upper()
            entries_list = drug_indication_list

        # clean up input
        elif query_cat == 'admin_route':
            query = query.title()
            entries_list = admin_route_list
        elif query_cat == "reaction_medDRA":
            query = query.title()
            entries_list = reaction_list
        else:
            print('bug?')
        # get similarities
        num = []
        for entry in entries_list:
            num.append(SequenceMatcher(None, query, entry).ratio())
        # get best matched entry
        entry_index = num.index(max(num))
        entry_query.append(entries_list[entry_index])
    # return matched entry list
    return entry_query

def query_match_rxn(query_in, lvl_in, lvl_out, modeling = True):
    entries_list = reaction_list #
    print("entries_list is {}".format(entries_list))
    PT_list = list(dict_PT_HLT.keys())
    HLT_list = list(dict_HLT_HLGT.keys())
    HLGT_list = list(dict_HLGT_SOC.keys())
    SOC_list = list(set(list(dict_HLGT_SOC.values()))) # get unique SOC values
    # 1. match to lvl_in by spelling
    # 2. If for modeling, match it to the relevant entries list
    # 3. If for recommendation or display, convert it via dictionaries

    entry_query = []
    for query in query_in:
        query = query.upper()
        # get it to the closest lvl_in
        if lvl_in == "SOC":
            # get similarities
            num = []
            for entry in SOC_list:
                num.append(SequenceMatcher(None, query, entry).ratio())
            # get best matched entry
            entry_index = num.index(max(num))
            # now the query is actually in SOC
            query = SOC_list[entry_index]

            if modeling:
                # match to the entries list
                num = []
                for entry in entries_list:
                    num.append(SequenceMatcher(None, query, entry).ratio())
                # get best matched entry
                entry_index = num.index(max(num))
                entry_query.append(entries_list[entry_index])
                # we got the entry in feature list
            else:
                # just return the SOC
                entry_query.append(query)

        if lvl_in == "HLGT":
            # get similarities
            num = []
            for entry in HLGT_list:
                num.append(SequenceMatcher(None, query, entry).ratio())
            # get best matched entry
            entry_index = num.index(max(num))
            # now the query is actually in HLGT
            query = HLGT_list[entry_index]

            if modeling:
                # match to the entries list
                num = []
                for entry in entries_list:
                    num.append(SequenceMatcher(None, query, entry).ratio())
                # get best matched entry
                entry_index = num.index(max(num))
                entry_query.append(entries_list[entry_index])
                # we got the entry in feature list
            else:
                if lvl_out == "SOC":
                    # convert with dicts
                    entry_query.append(dict_HLGT_SOC[query])
                if lvl_out == "HLGT":
                    # just return the HLGT
                    entry_query.append(query)

        if lvl_in == "HLT":
            # get similarities
            num = []
            for entry in HLT_list:
                num.append(SequenceMatcher(None, query, entry).ratio())
            # get best matched entry
            entry_index = num.index(max(num))
            # now the query is actually in HLT
            query = HLT_list[entry_index]

            if modeling:
                # match to the entries list
                num = []
                for entry in entries_list:
                    num.append(SequenceMatcher(None, query, entry).ratio())
                # get best matched entry
                entry_index = num.index(max(num))
                entry_query.append(entries_list[entry_index])
                # we got the entry in feature list
            else:
                if lvl_out == "SOC":
                    # convert with dicts
                    entry_query.append(dict_HLGT_SOC[dict_HLT_HLGT[query]])
                if lvl_out == "HLGT":
                    # convert with dicts
                    entry_query.append(dict_HLT_HLGT[query])
                if lvl_out == "HLT":
                    # just return the HLT
                    entry_query.append(query)

        if lvl_in == "PT":
            # get similarities
            num = []
            for entry in PT_list:
                num.append(SequenceMatcher(None, query, entry).ratio())
            # get best matched entry
            entry_index = num.index(max(num))
            # now the query is actually in PT
            query = PT_list[entry_index]

            if modeling:
                # match to the entries list
                print("query is {}".format(query))
                num = []
                for entry in entries_list:
                    print("entry is {}".format(entry))
                    num.append(SequenceMatcher(None, query, entry).ratio())
                # get best matched entry
                entry_index = num.index(max(num))
                entry_query.append(entries_list[entry_index])
                # we got the entry in feature list

            else:
                if lvl_out == "SOC":
                    # convert with dicts
                    entry_query.append(dict_HLGT_SOC[dict_HLT_HLGT[dict_PT_HLT[query]]])
                if lvl_out == "HLGT":
                    # convert with dicts
                    entry_query.append(dict_HLT_HLGT[dict_PT_HLT[query]])
                if lvl_out == "HLT":
                    # convert with dicts
                    entry_query.append(dict_PT_HLT[query])
                if lvl_out == "PT":
                    # just return the PT
                    entry_query.append(query)

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


def recomm_match(recomm_list):
    # recommendations categorized
    gn_recomm = []
    di_recomm = []
    ar_recomm = []
    rxn_recomm = []
    # put them into their respective lists
    for recomm in recomm_list:
        if recomm in generic_name_list:
            gn_recomm.append(recomm)
        if recomm in drug_indication_list:
            di_recomm.append(recomm)
        if recomm in admin_route_list:
            ar_recomm.append(recomm)
        if recomm in reaction_list:
            rxn_recomm.append(recomm)

    # Match them to more legible entries
    gn_recomm = query_match(gn_recomm, 'generic_name')
    di_recomm = query_match(di_recomm, 'drug_indication')
    ar_recomm = query_match(ar_recomm, 'admin_route')
    rxn_recomm = query_match(rxn_recomm, 'reaction_medDRA')
    gn_recomm = [feat.title() for feat in gn_recomm]
    di_recomm = [feat.title() for feat in di_recomm]
    ar_recomm = [feat.title() for feat in ar_recomm if feat != 'Not Listed']
    rxn_recomm = [feat.title() for feat in rxn_recomm]

    return gn_recomm, di_recomm, ar_recomm, rxn_recomm
