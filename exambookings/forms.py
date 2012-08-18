from django import forms
from exambookings.models import Booking

class CreateBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ('courseTeacher',)
    
