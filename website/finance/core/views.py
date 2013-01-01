from shortcuts import request_to_response

def home(request):
    return request_to_response(request, "login.html", {})