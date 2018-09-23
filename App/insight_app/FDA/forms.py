from django import forms
from django.forms import formset_factory

from FDA.FDA_misc.FDA_entry_gen import drug_char_entries
# dynamic forms
# https://www.b-list.org/weblog/2008/nov/09/dynamic-forms/
# https://medium.com/@taranjeet/adding-forms-dynamically-to-a-django-formset-375f1090c2b0
# https://stackoverflow.com/questions/501719/dynamically-adding-a-form-to-a-django-formset-with-ajax/669982#669982

class FDA_Form(forms.Form):
    generic_drug = forms.CharField(widget = forms.TextInput(
                                            attrs = {'class':'form-control', 'name':'0-generic_drug',
                                                    'id':'gn_form'}
                                            ), required = False)

    admin_route = forms.CharField(widget = forms.TextInput(
                                            attrs = {'class':'form-control', 'name':'0-admin_route',
                                                    'id':'ar_form'}
                                            ),
                                            required = False)

    drug_indication = forms.CharField(widget = forms.TextInput(
                                            attrs = {'class':'form-control', 'name':'0-drug_indication',
                                                     'id':'di_form'},
                                            ),
                                            required = False)
    drug_char = forms.ChoiceField(widget=forms.Select(
                                                attrs={
                                                    'class':'form-control form-control-sm',
                                                    'id':'dc_form'
                                                }),  choices = drug_char_entries)


FDA_formset = formset_factory(FDA_Form, extra = 0)

class FDA_Form_2(forms.Form):
    reaction = forms.CharField(widget = forms.TextInput(
                                            attrs = {'class':'form-control', 'name':'0-reaction',
                                                            'id':'rxn_form'}
                                            ),
                                            required = False)
