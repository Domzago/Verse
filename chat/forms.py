from django import forms

from chat.models import Item, Chatext, Profile


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'description', 'image']


class ChatextForm(forms.ModelForm):
    class Meta:
        model = Chatext
        fields = ['body']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user']

class ProfileIForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']