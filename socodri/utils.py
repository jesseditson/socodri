from urlparse import urljoin
import requests
import json
import hashlib
from django.conf import settings


def get_current_user(cookies):
    user = None
    if settings.DEBUG:
        user = settings.MOCK_USER
    else:
        resp = requests.get(urljoin(settings.SOCIALCODE_BASE_URL, settings.CURRENT_USER_API), cookies=cookies)
        user = resp.status_code == 200 and resp.json() or None
    return user


def uncamel(camel_str):
    return reduce(lambda a,b: a + ((b.upper() == b and (len(a) and a[-1].upper() != a[-1])) and (' ' + b) or b), camel_str, '')

def hash_params(params):
    tuple_string = json.dumps(params.items(), sort_keys=True)
    return hashlib.sha256(tuple_string).hexdigest()
