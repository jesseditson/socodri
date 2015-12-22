from django.shortcuts import render
from django.http import HttpResponse


def ping(request):
    "Health check for determining if the server is available"
    response_content = '<html><body>OK</body></html>'
    return HttpResponse(response_content, content_type='text/html')

def show_app(request):
    return render(request, "app.html")
