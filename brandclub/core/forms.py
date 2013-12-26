from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Field
from .models import StoreFeedback
from django.db import models


class FeedbackForm(ModelForm):
    # name = models.CharField(max_length=100, null=False)
    # phone_number = models.CharField(max_length=15, null=False)
    # email_id = models.EmailField(max_length=100, null=False)
    # message = models.TextField(max_length=1000)

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