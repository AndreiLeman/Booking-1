from django.contrib import messages

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

#from django.contrib.auth import authenticate, login, logout
#import django.contrib.auth
#import django.contrib.auth.forms
from django.contrib.auth.decorators import login_required

from pollApp.models import *


@login_required
def vote(request, poll_id):
    if True:
        p = get_object_or_404(Poll, pk=poll_id)
        try:
            selected_choice = p.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            messages.get_messages(request).used = True # clear messages from last request
            messages.error(request, "You didn't select a choice.")

            return HttpResponseRedirect(reverse('pollDetail', args=(p.id, )))
            
            # return render_to_response('pollApp/detail.html', {
            #         'poll': p,
            #         'error_message': "You didn't select a choice.",
            #         'form_action': ''
            #         }, context_instance=RequestContext(request))
        else:
            selected_choice.votes += 1
            selected_choice.save()

        return HttpResponseRedirect(reverse('poll_results', args=(p.id, )))
    
# def login(request):
#     username = ''
#     password = ''

#     if request.POST:
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)

#         if user is not None:
#             if user.is_active:
#                 django.contrib.auth.login(request, user) 

#         return render_to_response('pollApp/login.html',
#                                   {'error_message': "success"},
#                                   context_instance=RequestContext(request))

#     else:
#         return render_to_response('pollApp/login.html', {}, context_instance=RequestContext(request))

# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('pollAppHome'))
    

