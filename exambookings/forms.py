from django import forms as dforms
from exambookings.models import Booking

class CreateBookingForm(dforms.ModelForm):
    class Meta:
        model = Booking
        exclude = ('courseTeacher',)
    
