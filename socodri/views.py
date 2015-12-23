from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from socodri import authorization


def ping(request):
    "Health check for determining if the server is available"
    response_content = '<html><body>OK</body></html>'
    return HttpResponse(response_content, content_type='text/html')

@authorization.staff_login_required
def show_app(request):
    return render(request, "app.html", {'user': request.user, 'logout_url': settings.SOCIALCODE_LOGOUT_PATH})
