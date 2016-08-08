from django import forms

class SignForm(forms.Form):
    content = forms.CharField(required=True, max_length=10, label="Your message", widget=forms.Textarea)
