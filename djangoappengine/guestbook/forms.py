from django import forms

from google.appengine.api import users

from guestbook.models import Greeting, Guestbook

class SignForm(forms.Form):
    content = forms.CharField(required=True, max_length=10, label="Your message", widget=forms.Textarea)


class EditGreetingForm(forms.Form):
    guestbook_name = forms.CharField(widget=forms.HiddenInput(), required=False, )
    greeting_id = forms.CharField(widget=forms.HiddenInput(), required=False, )
    greeting_author = forms.CharField(label="Author", required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    greeting_content = forms.CharField(label="", required=True, max_length=10, widget=forms.Textarea)

    # def update_greeting(self):
    #     guestbook_name = self.cleaned_data['guestbook_name']
    #     greeting_id = self.cleaned_data['greeting_id']
    #     author = self.cleaned_data['greeting_author']
    #     greeting_content = self.cleaned_data['greeting_content']
    #     if users.get_current_user():
    #         greeting_updated_by = users.get_current_user().nickname()
    #     else:
    #         greeting_updated_by = None
    #     obj = Guestbook(guestbook_name)
    #     new_greeting = obj.update_greeting_by_id(author, users.get_current_user(), False, greeting_id, greeting_content)
    #     return new_greeting
    #
    #
    # def delete_message_form(self):
    #     guestbook_name = self.cleaned_data['guestbook_name']
    #     greeting_id = self.cleaned_data['greeting_id']
    #     author = self.cleaned_data['greeting_author']
    #     obj = Guestbook(guestbook_name)
    #     obj.delete_message(author, users.get_current_user(), False, greeting_id)