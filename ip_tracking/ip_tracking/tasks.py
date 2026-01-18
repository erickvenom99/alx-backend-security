from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    """
    Analyzes logs from the last hour to flag suspicious activity.
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # Rule 1: Flag IPs with > 100 requests in the last hour
    high_volume_ips = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(count=Count('id'))
        .filter(count__gt=100)
    )
    
    for entry in high_volume_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            reason=f"High volume: {entry['count']} requests in 1 hour."
        )

    # Rule 2: Flag IPs accessing sensitive paths
    sensitive_paths = ['/admin', '/login']
    suspicious_path_ips = (
        RequestLog.objects.filter(
            timestamp__gte=one_hour_ago,
            path__in=sensitive_paths
        )
        .values_list('ip_address', flat=True)
        .distinct()
    )
    
    for ip in suspicious_path_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            reason=f"Accessed sensitive paths: {sensitive_paths}"
        )