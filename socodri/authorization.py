from functools import wraps
from urlparse import urljoin
from django.conf import settings
from django.http import HttpResponseRedirect
from socodri import utils


def is_request_authorized(request):
    return request.user and is_user_authorized(request.user)


def is_user_authorized(user):
    return user and user.get('is_staff', False)


def staff_login_required(f):
    @wraps(f)
    def fn(request, *args, **kwargs):
        user = utils.get_current_user(request.COOKIES)
        if is_user_authorized(user):
            request.user = user
        else:
            return HttpResponseRedirect(urljoin(settings.SOCIALCODE_LOGIN_PATH, "?next=%s" % request.path))
        return f(request, *args, **kwargs)
    return fn
