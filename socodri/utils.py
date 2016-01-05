from urlparse import urljoin
import requests
from django.conf import settings


def get_current_user(cookies):
    user = None
    if settings.DEBUG:
        user = settings.MOCK_USER
    else:
        resp = requests.get(urljoin(settings.SOCIALCODE_BASE_URL, settings.CURRENT_USER_API), cookies=cookies)
        user = resp.status_code == 200 and resp.json() or None
    return user
