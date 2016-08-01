from django import forms

class SignForm(forms.Form):
    message = forms.CharField(label='Your message', max_length=50)
    guestbook_name = forms.CharField(label='Guestbook name', max_length=10)