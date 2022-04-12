from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.validators import MinLengthValidator

from cookbook.common.helpers import AddBootstrapFormCLassMixin
from cookbook.accounts.models import Profile
from cookbook.common.validators import name_contains_only_letters_validator


class ProfileCreationForm(AddBootstrapFormCLassMixin, UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(Profile.FIRST_NAME_MIN_LENGTH),
            name_contains_only_letters_validator,
        ]
    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(Profile.LAST_NAME_MIN_LENGTH),
            name_contains_only_letters_validator,
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._init_bootstrap_form_controls()
        for fieldname in ['email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user=user,
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']


class ProfileLoginForm(AddBootstrapFormCLassMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()


class EditProfileForm(AddBootstrapFormCLassMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'description', 'date_of_birth', 'image', 'cover_image']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'mm/dd/yyyy'}),
        }
