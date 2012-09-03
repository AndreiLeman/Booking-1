from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from exambookings.models import Booking

from django.core.context_processors import csrf

# reverse_lazy is included in Django 1.4
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
reverse_lazy = lazy(reverse, str)

from django.contrib.auth.decorators import user_passes_test
def any_permission_required(*perms):
    """ decorator """    
    return user_passes_test(lambda u: any(u.has_perm(perm) for perm in perms))

def staff_only_view(function=None):
    """ decorator """
    actual_decorator = any_permission_required('exambookings.teacher_view', 'exambookings.exam_center_view')
    if function:
        return actual_decorator(function)
    return actual_decorator

def authorized_user_of_this_booking_only_view(function=None):
    """ decorator expects decorated view function to have parameters: (request, pk)
    pk is primary key of a Booking object
    """
    def wrapper(request, *args, **kwargs):
        appt = get_object_or_404(Booking, id__iexact=kwargs['pk'])
        if appt.courseTeacher == request.user or request.user.has_perm('exambookings.exam_center_view'):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("<h1>Update Forbidden</h1> Only <b>exam center staff</b> and the <b>course teacher</b> of an appointment may make changes.", content_type="text/html")
    return wrapper

from django.utils.decorators import method_decorator
class StaffOnlyViewMixin(object):
    @method_decorator(any_permission_required('exambookings.teacher_view', 'exambookings.exam_center_view'))
    def dispatch(self, *args, **kwargs):
        return super(StaffOnlyViewMixin, self).dispatch(*args, **kwargs)



def create_standard_context(request):
    ctx = {}
    if request.user.is_authenticated():
        ctx['user_logged_in'] = True
    return ctx

def create_standard_csrf_context(request):
    ctx = create_standard_context(request)
    ctx.update(csrf(request))
    return ctx
