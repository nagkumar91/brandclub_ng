# from django.forms import ModelForm
from django import forms
from .models import StoreFeedback, CustomStoreFeedback

RECOMMENDATION_OPTION_CHOICES = (
    ('0', 0),
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4)
)

PRODUCT_RANGE_OPTIONS = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not Sure', 'Not Sure'),
)

STAFF_OPTIONS = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not Particularly', 'Not Particularly'),
)

OVERALL_EXPERIENCE_OPTIONS = (
    ('Very Bad', 'Very Bad'),
    ('Bad', 'Bad'),
    ('Neutral', 'Neutral'),
    ('Good', 'Good'),
    ('Excellent', 'Excellent'),
)

SHOPPING_LENGTH_OPTIONS = (
    ('First Time', 'First Time'),
    ('Less Than 3 Months', 'Less Than 3 Months'),
    ('One Year', 'One Year'),
    ('3 Years', '3 Years'),
    ('Five Years', 'Five Years'),
)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = StoreFeedback
        fields = ['name', 'phone_number', 'email_id', 'message']


class CustomFeedbackForm(forms.ModelForm):
    recommendation_options = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'custom-radio'}), choices=RECOMMENDATION_OPTION_CHOICES, initial='4',
                                               label='How likely is it that you would recommend appleofmyi to a friend or colleague?',
                                               help_text='( 0 - Not at all likely & 4 - Extremely likely )')
    product_range_options = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'custom-radio'}), choices=PRODUCT_RANGE_OPTIONS, initial='Yes',
                                              label='Did you find our product range to be useful, fun and exciting?')
    staff_options = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'custom-radio'}), choices=STAFF_OPTIONS, initial='Yes',
                                      label='Do you find our staff to be helpful and courteous?')
    overall_experience = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'custom-radio'}), choices=OVERALL_EXPERIENCE_OPTIONS, initial='Excellent',
                                           label='What has been your overall experience with this visit to appleofmyi?')
    how_long_have_you_been_shopping = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'custom-radio'}), choices=SHOPPING_LENGTH_OPTIONS, initial='First Time',
                                                        label='How long have you been shopping at appleofmyi?')
    any_other_feedback = forms.CharField(required=False)
    name = forms.CharField(required=True)
    phone_number = forms.NumberInput()


    class Meta:
        model = CustomStoreFeedback
        fields = ('recommendation_options', 'product_range_options', 'staff_options', 'overall_experience',
                  'how_long_have_you_been_shopping', 'any_other_feedback', 'name', 'phone_number')
        # widgets = {
        #     'recommendation_options': forms.RadioSelect(choices=RECOMMENDATION_OPTION_CHOICES),
        # }
        labels = {
            'recommendation_options': (
                'How likely is it that you would recommend appleofmyi to a friend or colleague?'),
            'product_range_options': ('Did you find our product range to be useful, fun and exciting?'),
            'staff_options': ('Do you find our staff to be helpful and courteous?'),
            'overall_experience': ('What has been your overall experience with this visit to appleofmyi?'),
            'how_long_have_you_been_shopping': ('How long have you been shopping at appleofmyi? '),
            'any_other_feedback': ('Any other feedback you have for us? ')
        }
