import requests
from functools import wraps
from urlparse import urljoin
from django.conf import settings
from django.http import HttpResponseRedirect


def get_current_user_or_none(cookies):
    user = None
    if settings.DEBUG:
        user = settings.MOCK_USER
    else:
        resp = requests.get(urljoin(settings.SOCIALCODE_BASE_URL, settings.CURRENT_USER_API), cookies=cookies)
        user = resp.status_code == 200 and resp.json() or None
    return user


def is_request_authorized(request):
    user = get_current_user_or_none(request.COOKIES)
    return is_user_authorized(user)


def is_user_authorized(user):
    return user and user.get('is_staff', False)


def staff_login_required(f):
    @wraps(f)
    def fn(request, *args, **kwargs):
        user = get_current_user_or_none(request.COOKIES)
        if is_user_authorized(user):
            request.user = user
        else:
            return HttpResponseRedirect(urljoin(settings.SOCIALCODE_LOGIN_PATH, "?next=%s" % request.path))
        return f(request, *args, **kwargs)
    return fn
