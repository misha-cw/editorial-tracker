from django import forms
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Redactor


class RedactorCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )
        widgets = {
            "years_of_experience": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100}),
        }

    def clean_years_of_experience(self):
        years = self.cleaned_data.get("years_of_experience")
        if years is not None and (years < 0 or years > 100):
            raise forms.ValidationError("Years of experience must be between 0 and 100.")
        return years


class RedactorUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = [
            "username",
            "first_name",
            "last_name",
            "years_of_experience",
        ]
        widgets = {
            "years_of_experience": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100,}),
        }
    
    def clean_years_of_experience(self):
        years = self.cleaned_data.get("years_of_experience")
        if years is not None and (years < 0 or years > 100):
            raise forms.ValidationError("Years of experience must be between 0 and 100.")
        return years
    
