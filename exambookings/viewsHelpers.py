# reverse_lazy is included in Django 1.4
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
reverse_lazy = lazy(reverse, str)

from django.contrib.auth.decorators import user_passes_test
def any_permission_required(*perms):
    return user_passes_test(lambda u: any(u.has_perm(perm) for perm in perms))

from django.utils.decorators import method_decorator
class StaffOnlyViewMixin(object):
    @method_decorator(any_permission_required('exambookings.teacher_view', 'exambookings.exam_center_view'))
    def dispatch(self, *args, **kwargs):
        return super(StaffOnlyViewMixin, self).dispatch(*args, **kwargs)
