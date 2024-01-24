
from django.contrib.admin.widgets import BaseAdminDateWidget, BaseAdminTimeWidget 
from django.forms import ModelForm
from django import forms

from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class OtherWidget(forms.TextInput):
    
    class Media:
        css = {
            "all": ["other.css"],
        }
        js = ["other.js"]

class CalendarWidget(forms.TextInput):
    
    class Media:
        css = {
            "all": ["pretty.css"],
        }
        js = ["animations.js", 'actions.js']

class CustomTextInput(forms.TextInput):
    icon=''

    def __init__(self, icon=''):
        self.icon = icon
        super().__init__()

    class Media:
        css = {
            "all": ["pretty.css"],
        }
        js = ["animations.js", 'actions.js']

    def render(self, name, value, attrs=None, renderer=None):
        
        if self.icon:
            return f'<div class="group"><img src="{self.icon}"> {super().render(name, value, attrs, renderer)} </div>'
        else:
            return super().render(name, value, attrs, renderer)



class ContactForm(forms.Form):
    other = forms.CharField(widget=OtherWidget, help_text='Help text 1')
    calendar = forms.CharField(widget=BaseAdminTimeWidget, help_text='Help text 4')
    custom = forms.CharField(widget=CustomTextInput(icon='user.png'), help_text='Help text 2')