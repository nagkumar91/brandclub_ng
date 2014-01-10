from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Field
from .models import StoreFeedback
from django.db import models


class FeedbackForm(ModelForm):
    class Meta:
        model = StoreFeedback
        fields = ['name','phone_number','email_id','message']