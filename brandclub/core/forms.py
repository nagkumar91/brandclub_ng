from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Field
from .models import StoreFeedback
from django.db import models


class FeedbackForm(ModelForm):
    class Meta:
        model = StoreFeedback

    def clean(self):
        print "Inside clean function"
        if self.cleaned_data.get('name', '') is None:
            raise ValidationError('Name is null')
        if self.cleaned_data.get('phone_number', '') is None:
            raise ValidationError('Phone number is null')
        if self.cleaned_data.get('email_id', '') is None:
            raise ValidationError('Email id is null')