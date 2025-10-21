from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Redactor, Newspaper, Topic


class RedactorCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
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
            "email",
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
    

class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),  
        widget=forms.CheckboxSelectMultiple,
    )


    class Meta:
        model = Newspaper
        fields = [
            "title",
            "content",
            "topics",
            "publishers",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }


class NewspaperTitleSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control me-2",
                "placeholder": "Search by Title",
            }
        ),
    )


class RedactorUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control me-2",
                "placeholder": "Search by Username"
            }
        ),
    )


class TopicNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control me-2",
                "placeholder": "Search by Name"
            }
        ),
    )
