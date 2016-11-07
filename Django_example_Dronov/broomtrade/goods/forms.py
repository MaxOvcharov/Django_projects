from django import forms

from goods.models import Good

class GoodForm(forms.ModelForm):
  class Meta:
    model = Good
