from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()