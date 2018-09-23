from django import forms
from django.forms import formset_factory

# class based form
class demo_app_form(forms.Form):
    # Decimal form with a generic widget to look nice
    input_demo = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))

demo_app_formset = formset_factory(demo_app_form, extra = 1)
