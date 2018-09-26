import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import View, TemplateView, FormView
from FDA import forms

from FDA.FDA_misc.FDA_entry_gen import query_match, query_match_rxn # connect input to the features
from FDA.FDA_misc.FDA_entry_gen import feature_vec # generate a feature vector
from FDA.FDA_misc.FDA_entry_gen import recomm_match # generate a feature vector
from FDA.FDA_misc.ML_preds import LR_pred, cluster_pred # run the model
from FDA.FDA_misc.FDA_entry_gen import entries
from FDA.FDA_misc.FDA_entry_gen import listed_features


import pandas as pd
# http://flaviusim.com/blog/AJAX-Autocomplete-Search-with-Django-and-jQuery/
# http://jqueryui.com/autocomplete/#default
# http://flaviusim.com/blog/AJAX-Autocomplete-Search-with-Django-and-jQuery/
# http://www.lalicode.com/post/5/
import json
from django.core.serializers.json import DjangoJSONEncoder

def FDA(request):
    # Initialize the context_dict
    context_dict = {'Message1': 'Prescription Drugs:'}
    context_dict['Message2'] = 'What\'s the Worst that Could Happen?'

    # Send entries for auto-complete
    # capitalize the admin-routes
    listed_features[1] = [item.upper() for item in listed_features[1]]
    context_dict['gn_entries_JSON'] = json.dumps(listed_features[0], cls = DjangoJSONEncoder)
    context_dict['ar_entries_JSON'] = json.dumps(listed_features[1], cls = DjangoJSONEncoder)
    context_dict['di_entries_JSON'] = json.dumps(listed_features[2], cls = DjangoJSONEncoder)
    context_dict['rxn_entries_JSON'] = json.dumps(listed_features[4], cls = DjangoJSONEncoder) # preferred term

    # get the form
    form = forms.FDA_Form(initial = {'drug_char':'0'})
    context_dict['form'] = form
    formset = forms.FDA_formset()
    context_dict['formset'] = formset
    form_rxn = forms.FDA_Form_2()
    context_dict['form_rxn'] = form_rxn
    # if the submit button is pressed
    if request.method == 'POST': # If submit is hit
        form = forms.FDA_Form(request.POST) # get the data
        formset = forms.FDA_formset(request.POST) # get the data
        form_rxn = forms.FDA_Form_2(request.POST) # get the data
        # Check to see if the form is valid
        if form.is_valid() and formset.is_valid() and form_rxn.is_valid():
            # initialize lists for inputs
            context_dict['results'] = True
            gn = []
            ar = []
            di = []
            dc = []
            rxn = []
            # get the data from initial form
            gn.append(form.cleaned_data['generic_drug'])
            ar.append(form.cleaned_data['admin_route'])
            di.append(form.cleaned_data['drug_indication'])
            dc.append(form.cleaned_data['drug_char'])
            # get the data from the formset
            data = []
            for form in formset:
                gn.append(form.cleaned_data['generic_drug'])
                ar.append(form.cleaned_data['admin_route'])
                di.append(form.cleaned_data['drug_indication'])
                dc.append(form.cleaned_data['drug_char'])
            # get the data from the rxn form (required)
            rxn.append(form_rxn.cleaned_data['reaction'])
            # create list of mapped features
            feature_list = []

            # generic_name
            gn = [x for x in gn if x] # drop blanks
            if len(gn) > 0:
                gn_map = query_match(gn, 'generic_name')
                feature_list.extend(gn_map)
                context_dict['input_gn'] = [item.upper() for item in gn_map]
            # admin_route
            ar = [x for x in ar if x] # drop blanks
            if len(ar) > 0:
                ar_map = query_match(ar, 'admin_route')
                feature_list.extend(ar_map)
                context_dict['input_ar'] = [item.upper() for item in ar_map]
            # drug_indication
            di = [x for x in di if x] # drop blanks
            if len(di) > 0:
                di_map = query_match(di, 'drug_indication')
                feature_list.extend(di_map)
                context_dict['input_di'] = [item.upper() for item in di_map]
            # drug_char
            dc_map = []
            for dc_i in dc:
                if dc_i == "1":
                    dc_map.append("Suspect")
                if dc_i == "2":
                    dc_map.append('Concominant')

            feature_list.extend(dc_map)
            # reaction_medDRA
            rxn = [x for x in rxn if x] # drop blanks
            rxn_map = query_match_rxn(rxn, lvl_in = "PT", lvl_out = "HLT", modeling = True) #### CHANGE lvl_out with varied features
            feature_list.extend(rxn_map)
            context_dict['input_rxn'] = [item.upper() for item in rxn_map]

            # create feature vector for input to model
            vec_input = feature_vec(feature_list)
            # get the prediction probabilities
            prob_output = LR_pred(vec_input)

            # set up outputs for progress bars
            # Serious
            if prob_output[0] < 33:
                context_dict['serious_good'] = prob_output[0]
            if prob_output[0] > 32 and prob_output[0] < 67:
                context_dict['serious_ok'] = prob_output[0]
            if prob_output[0] > 66:
                context_dict['serious_bad'] = prob_output[0]
            # Death
            if prob_output[1] < 33:
                context_dict['death_good'] = prob_output[1]
            if prob_output[1] > 32 and prob_output[1] < 67:
                context_dict['death_ok'] = prob_output[1]
            if prob_output[1] > 66:
                context_dict['death_bad'] = prob_output[1]
            # Disabling
            if prob_output[2] < 33:
                context_dict['disabling_good'] = prob_output[2]
            if prob_output[2] > 32 and prob_output[2] < 67:
                context_dict['disabling_ok'] = prob_output[2]
            if prob_output[2] > 66:
                context_dict['disabling_bad'] = prob_output[2]
            # Hospitalization
            if prob_output[3] < 33:
                context_dict['hospital_good'] = prob_output[3]
            if prob_output[3] > 32 and prob_output[3] < 67:
                context_dict['hospital_ok'] = prob_output[3]
            if prob_output[3] > 66:
                context_dict['hospital_bad'] = prob_output[3]
            # Life Threatening
            if prob_output[4] < 33:
                context_dict['lifethreatening_good'] = prob_output[4]
            if prob_output[4] > 32 and prob_output[4] < 67:
                context_dict['lifethreatening_ok'] = prob_output[4]
            if prob_output[4] > 66:
                context_dict['lifethreatening_bad'] = prob_output[4]

            # get the nearest user and top recomm features
            recom_serious = cluster_pred(vec_input, outcome = "serious")
            recom_death = cluster_pred(vec_input, outcome = "death")
            recom_disabling = cluster_pred(vec_input, outcome = "disabling")
            recom_hospital = cluster_pred(vec_input, outcome = "hospital")
            recom_serious = cluster_pred(vec_input, outcome = "lifethreatening")
            # put the recom_features into categories
            ##### EDIT recomm_match if you change feature sets!!! #
            gn_recomm, di_recomm, ar_recomm, rxn_recomm = recomm_match(recom_list)
            # sent them to context_dict
            if len(rxn_recomm) > 0:
                context_dict['gn_recomm'] = gn_recomm
            if len(rxn_recomm) > 0:
                context_dict['di_recomm'] = di_recomm
            if len(rxn_recomm) > 0:
                context_dict['ar_recomm'] = ar_recomm
            if len(rxn_recomm) > 0:
                context_dict['rxn_recomm'] = rxn_recomm

    # respond to the request
    return render(request,'FDA.html',context_dict)
