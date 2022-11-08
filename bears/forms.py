from django import forms
from .models import Bear

class BearForm (forms.ModelForm):

    # we don't include created_date as it is non-editable
    class Meta:
        model = Bear
        fields = ('bearID', 'pTT_ID', 'capture_lat', 'capture_long', 'sex','age_class','ear_applied')