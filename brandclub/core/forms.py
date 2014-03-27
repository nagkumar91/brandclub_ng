from django.forms import ModelForm

from .models import StoreFeedback


class FeedbackForm(ModelForm):
    class Meta:
        model = StoreFeedback
        fields = ['name','phone_number','email_id','message']