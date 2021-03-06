from django import forms
from django.forms.extras.widgets import SelectDateWidget
from exambookings.models import Booking, Period
from django.contrib.auth.models import User, Permission
import userena.forms, re
from exambookings import settings
from profiles.models import prettyNameOfUser
import datetime

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, usr):
         return prettyNameOfUser(usr)

class UpdateBookingForm(forms.ModelForm):
    courseTeacher = UserModelChoiceField(queryset=User.objects.all().order_by('email'), label="Course Teacher")
    testDate = forms.DateField(widget=SelectDateWidget(years=[2012]), label="Test on Date")
    testDuration = forms.IntegerField(min_value=0, max_value=480, initial=90, label="Test Duration (minutes)")
    testBeginTime = forms.TypedChoiceField(choices=Period.CHOICES, coerce=int, label="Test Period")
    class Meta:
        model = Booking
        exclude = ('testEndTime',)

class CreateBookingForm(forms.ModelForm):
    testDate = forms.DateField(widget=SelectDateWidget(years=[2012]), label="Test on Date")
    testDuration = forms.IntegerField(min_value=0, max_value=480, initial=90, label="Test Duration (minutes)")
    testBeginTime = forms.TypedChoiceField(choices=Period.CHOICES, coerce=int, label="Test Period")
    class Meta:
        model = Booking
        exclude = ('courseTeacher', 'testEndTime',)

def email_is_allowed_signup(email):
    """returns True only if email address is from domain
    settings.MAIN_EMAIL_DOMAIN
    determined by settings.MAIN_EMAIL_DOMAIN_RE_PATTERN
    or email is in settings.SIGNUP_EMAIL_WHITELIST
    """
    if (None != re.match(settings.MAIN_EMAIL_DOMAIN_RE_PATTERN, email)) or (email in settings.SIGNUP_EMAIL_WHITELIST):
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

class ExamBookingAuthForm(userena.forms.AuthenticationForm):
    def clean(self):
        email = self.cleaned_data.get('identification')
        if not email_is_allowed_signup(email):
            email = email + '@' + settings.MAIN_EMAIL_DOMAIN
            if email_is_allowed_signup(email):
                self.cleaned_data['identification'] = email
        return super(ExamBookingAuthForm, self).clean()
