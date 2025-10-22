from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from agency.models import Newspaper


class RedactorCreationForm(UserCreationForm):
    newspapers = forms.ModelMultipleChoiceField(
        queryset=Newspaper.objects.all(), required=False
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "years_of_experience", "email", "newspapers",)


class RedactorUpdateNewspapersForm(forms.ModelForm):
    newspapers = forms.ModelMultipleChoiceField(
        queryset=Newspaper.objects.all(), required=False
    )

    class Meta:
        model = get_user_model()
        fields = ("newspapers",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["newspapers"].initial = Newspaper.objects.filter(publishers=self.instance)


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search",
            },
        ),
    )
