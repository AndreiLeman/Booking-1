from django import forms as dforms
from exambookings.models import Booking
import userena.forms, re

class CreateBookingForm(dforms.ModelForm):
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
    def clean_email(self):
        """ Validate that the e-mail address is allowed. """
        if not email_is_allowed_signup(self.cleaned_data['email']):
            raise dforms.ValidationError('This email is not allowed. Please supply an authorized email.')
        return super(ExamBookingSignupForm, self).clean_email()
