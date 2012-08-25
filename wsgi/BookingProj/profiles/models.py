from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from userena.models import UserenaBaseProfile

import datetime

class BaseProfile(UserenaBaseProfile):
    """ Default profile """
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name= ('user'),
                                related_name='baseProfile')
    #firstName = models.CharField(max_length=25)
    #lastName = models.CharField(max_length=25)
    #emailAddress = models.EmailField(max_length=254)

    #role = models.CharField(max_length=25) #unneeded

    # django auth User class already has fields:
    # first_name = models.CharField(_('first name'), max_length=30, blank=True)
    # last_name = models.CharField(_('last name'), max_length=30, blank=True)
    # email = models.EmailField(_('e-mail address'), blank=True)

    def __unicode__(self):
        return (self.user.first_name + " " + self.user.last_name + " base profile")
