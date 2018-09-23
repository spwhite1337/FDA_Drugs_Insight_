from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import View, TemplateView, FormView
# Create your views here.
from demo_app import forms
from demo_app.demo_app_misc.add_5 import adder

# Function-based View
def demo_app_view(request):
    # Initialize a context_dict
    context_dict = {'Message':'Insight 4eva'}

    # get the form
    form = forms.demo_app_form(initial = {'input_demo': 5})
    formset = forms.demo_app_formset()
    # transfer to the context_dict
    context_dict['form'] = form
    context_dict['formset'] = formset
    # if the submit button is pressed
    if request.method == 'POST': # If submit is hit
        form = forms.demo_app_form(request.POST) # get the data
        formset = forms.demo_app_formset(request.POST) # get the additional data
        # Check to see if the form is valid
        if form.is_valid() and formset.is_valid():
            # transfer to the context_dict
            context_dict['input_demo'] = form.cleaned_data['input_demo']
            # generate output
            context_dict['output_demo'] = adder(context_dict['input_demo'])

            data = []
            for asd in formset:
                if 'input_demo' in asd.cleaned_data.keys():
                    data.append(asd.cleaned_data['input_demo'])

            context_dict['data'] = data
            # Respond to the http request
            return render(request, 'demo_app.html', context_dict)
    # Respond to the http request
    return render(request, 'demo_app.html', context_dict)
