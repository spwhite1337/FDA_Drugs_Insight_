from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import View, TemplateView, FormView
from FDA import forms

from FDA.FDA_misc.FDA_entry_gen import query_match # connect input to the features
from FDA.FDA_misc.FDA_entry_gen import feature_vec # generate a feature vector
from FDA.FDA_misc.ML_preds import RF_pred, cluster_pred # run the model
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
    context_dict = {'Message': 'Insight Fellows'}

    # Send entries for auto-complete
    context_dict['gn_entries_JSON'] = json.dumps(listed_features[0], cls = DjangoJSONEncoder)
    context_dict['ar_entries_JSON'] = json.dumps(listed_features[1], cls = DjangoJSONEncoder)
    context_dict['di_entries_JSON'] = json.dumps(listed_features[2], cls = DjangoJSONEncoder)
    context_dict['rxn_entries_JSON'] = json.dumps(listed_features[3], cls = DjangoJSONEncoder)
    # get the form
    form = forms.FDA_Form(initial = {'drug_char':'1'})
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
            # admin_route
            ar = [x for x in ar if x] # drop blanks
            if len(ar) > 0:
                ar_map = query_match(ar, 'admin_route')
                feature_list.extend(ar_map)
            # drug_indication
            di = [x for x in di if x] # drop blanks
            if len(di) > 0:
                di_map = query_match(di, 'drug_indication')
                feature_list.extend(di_map)
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
            rxn_map = query_match(rxn, 'reaction_medDRA')
            feature_list.extend(rxn_map)
            # All together for the template
            context_dict['inputs'] = feature_list

            # create feature vector for input to model
            vec_input = feature_vec(feature_list)
            # get the prediction probabilities
            prob_output = RF_pred(vec_input)
            context_dict['prob_output'] = prob_output
            # get the nearest user
            recom_list = cluster_pred(vec_input)
            context_dict['Recommendations'] = recom_list
    # respond to the request
    return render(request,'FDA.html',context_dict)
