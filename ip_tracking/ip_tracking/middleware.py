from .models import RequestLog, BlockedIP
from django.http import HttpResponseForbidden

class IpLoggingMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
		if x_forwarded_for:
			ip = x_forwared_for.split(',')[0].strip()
		else:
			ip = request.META.get('REMOTE_ADDR')
		if BlockeIP.objects.filter(ip_address=ip).exist():
			return HttpResponseForbidden("Access Denied: your IP address has been blacklisted")
		cache_key = f"geo_data_{ip}"
		geo_data = cache.get(cache_key)
		if not geo_data:
			# Fetch from API if not in cache
			location = get_ip_controler(ip)
			data = location.get_geolocation_data()
			geo_data = {
				'country': data.get('country_name', 'Unknown'),
				'city': data.get('city', 'Unknown')
            }
			cache.set(cache_key, geo_data, 86400)
		path = request.path
		RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            country=geo_data['country'],
            city=geo_data['city']
        )
		
		response = self.get_response(request)
		return response