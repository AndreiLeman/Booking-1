from django import forms
from exambookings.models import Booking
from django.contrib.auth.models import Permission
import userena.forms, re

class CreateBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ('courseTeacher',)

RE_PATTERN_example_com = '[^@]+@example\.com'
RE_PATTERN_cbe_ab_ca = '[^@]+@cbe\.ab\.ca'
SIGNUP_EMAIL_WHITELIST = ['homer@example.com']

def email_is_allowed_signup(email):
    """returns True only if email address is from domain example.com
    or email is in SIGNUP_EMAIL_WHITELIST
    """
    if (None != re.match(RE_PATTERN_example_com, email)) or (email in SIGNUP_EMAIL_WHITELIST):
        return True
    return False


class ExamBookingSignupForm(userena.forms.SignupFormOnlyEmail):
    firstname = forms.CharField(max_length=30, label="First Name (Initial)")
    lastname = forms.CharField(max_length=30, label="Last Name")

    def __init__(self, *args, **kwargs):
        super(ExamBookingSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = self.fields['password1'].label + " (Use one you've never used before!)"
        self.fields.keyOrder = ['firstname', 'lastname', 'email', 'password1', 'password2']
    
    def clean_email(self):
        """ Validate that the e-mail address is allowed. """
        if not email_is_allowed_signup(self.cleaned_data['email']):
            raise forms.ValidationError('This email is not allowed. Please supply an authorized email.')
        return super(ExamBookingSignupForm, self).clean_email()

    def save(self):
        user = super(ExamBookingSignupForm, self).save()
        user.user_permissions.add(Permission.objects.get(codename='teacher_view'))
        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        user.save()
        return user

