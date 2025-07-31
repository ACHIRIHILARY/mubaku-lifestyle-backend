from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django_countries.fields import CountryField
from django_countries import countries
from django_countries.widgets import CountrySelectWidget
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["email", "username", "first_name", "last_name"]
        error_class = "error"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name"]
        error_class = "error"


class UserProfileForm(forms.ModelForm):
    # Fields from the Profile model
    phone_number = forms.CharField(required=False)
    about_me = forms.CharField(widget=forms.Textarea, required=False)
    profile_photo = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices=[("M", "Male"), ("F", "Female")], required=False)
    country = forms.ChoiceField(
        choices=[("", "(select country)")] + list(countries), required=False
    )
    city = forms.CharField(required=False)
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name"]  # Fields from the User model

    def __init__(self, *args, **kwargs):
        # Pass Profile instance as an argument
        self.profile_instance = kwargs.pop("profile_instance", None)
        super(UserProfileForm, self).__init__(*args, **kwargs)

        # Initialize profile fields if a Profile instance is provided
        if self.profile_instance:
            self.fields["phone_number"].initial = self.profile_instance.phone_number
            self.fields["about_me"].initial = self.profile_instance.about_me
            self.fields["profile_photo"].initial = self.profile_instance.profile_photo
            self.fields["gender"].initial = self.profile_instance.gender
            self.fields["country"].initial = self.profile_instance.country
            self.fields["city"].initial = self.profile_instance.city
            self.fields["address"].initial = self.profile_instance.address

    def save(self, commit=True):
        # Save User fields
        user = super(UserProfileForm, self).save(commit=commit)

        # Save Profile fields
        if self.profile_instance:
            self.profile_instance.phone_number = self.cleaned_data["phone_number"]
            self.profile_instance.about_me = self.cleaned_data["about_me"]
            self.profile_instance.profile_photo = self.cleaned_data["profile_photo"]
            self.profile_instance.gender = self.cleaned_data["gender"]
            self.profile_instance.country = self.cleaned_data["country"]
            self.profile_instance.city = self.cleaned_data["city"]
            self.profile_instance.address = self.cleaned_data["address"]
            if commit:
                self.profile_instance.save()

        return user
