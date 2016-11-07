from django import forms

from guestbook.models import Guestbook

class GuestbookForm(forms.ModelForm):
  class Meta:
    model = Guestbook
  user = forms.CharField(max_length = 20, label = "Пользователь")
  content = forms.CharField(widget = forms.Textarea, label = "Содержание")
  honeypot = forms.CharField(required = False, label = "Ловушка для спамеров")
