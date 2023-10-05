from django import forms
from django.forms import ModelForm
from .models import Vanue,Event

#Create a venue form
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name','event_date','vanue','manager','attendees','description')

        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'vanue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
        }

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
            'event_date': forms.TextInput(attrs={'class':'form-control','placeholder':'Event Date'}),
            'vanue': forms.Select(attrs={'class':'form-select','placeholder':'Vanue Name'}),
            'manager': forms.Select(attrs={'class':'form-select','placeholder':'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Attendees'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}),


        }
class VanueForm(ModelForm):
    class Meta:
        model = Vanue
        fields = ('name','address','zip_code','phone','web','email_address','vanue_image')

        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
            'vanue_image':'',
        }

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'zip_code': forms.TextInput(attrs={'class':'form-control','placeholder':'Zip_Code'}),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
            'web': forms.TextInput(attrs={'class':'form-control','placeholder':'Web Address'}),
            'email_address': forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}),


        }