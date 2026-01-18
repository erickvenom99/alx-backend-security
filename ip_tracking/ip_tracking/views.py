from django.shortcuts import render
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from django.conf import settings

# Helper to determine which rate to use
def get_rate(group, request):
    if request.user.is_authenticated:
        return settings.AUTH_RATE
    return settings.ANON_RATE

@ratelimit(key='user_or_ip', rate=get_rate, block=True)
def login_view(request):
    """
    A sensitive view (login) protected by rate limits.
    - Authenticated: 10 req/min
    - Anonymous: 5 req/min
    """
    return HttpResponse("Login page - Try refreshing quickly to trigger the limit!")

def ratelimit_error(request, exception=None):
    """
    This view is called when a user exceeds their rate limit.
    """
    return HttpResponseForbidden("Too many requests. Please try again later.")