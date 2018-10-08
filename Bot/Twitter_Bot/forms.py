from django import forms
from django.forms import DateTimeInput
from requests import request
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django .contrib.auth import authenticate
from django.contrib import messages
# from .models import tweets_twitter,tweets_numbering,using_time,Data_tweet


class Fav_keyword(forms.ModelForm):
    Fav_keywords = forms.CharField(label='Please enter your favourite keywords')
    num_limits = forms.IntegerField(label='Please enter number limit ')
    class Meta:
        model = FavouriteKeywords
        fields = ["Fav_keywords",
                  "num_limits",
                 ]


class Restricted_words(forms.ModelForm):
    Restrited_keywords = forms.CharField(label='Enter restricted words you dont want to like  :::',widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '}))
    # numlimits = forms.IntegerField(label= 'Enter limit of number :::', required=False)

    class Meta:
        model = RestrictedKeywords
        fields = [

            "Restrited_keywords",
            # "numlimits",
        ]


class between_time(forms.ModelForm):
    initial_time = forms.DateTimeField(
        label="Initial time",
        required=False,
        input_formats=["%m/%d/%Y %H:%M %p"],
        widget=DateTimeInput(format="%m/%d/%Y %H:%M %p",
                             attrs = {'placeholder': 'YYYY-mm-dd HH:mm:ss'})
    )

    final_time = forms.DateTimeField(
        label="Final time",
        required=False,
        input_formats=["%m/%d/%Y %H:%M %p"],
        widget=DateTimeInput(format="%m/%d/%Y %H:%M %p",
                             attrs={'placeholder': 'YYYY-mm-dd HH:mm:ss'}
                               ))

    class Meta:
        model = Jobs
        fields = [
            "initial_time",
            "final_time",
        ]


class BlockUser(forms.ModelForm):
    block_users = forms.CharField(label='Enter Screen Name of user to Block him:::')

    class Meta:
        model = Black_List_Names
        fields = [
            "block_users"
        ]



class Days_calc(forms.ModelForm):
    days_back = forms.IntegerField(label='Enter Number of Days')

    class Meta:
        model = days
        fields = [
            "days_back"
        ]


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, help_text='Enter user name ', widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.',widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(help_text='Your password must contain atleast 8 characters',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(help_text='Your password must match with above password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class SimpleForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)

        return super(SimpleForm, self).clean(*args, **kwargs)