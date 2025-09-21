from celery import shared_task
from .models import RequestLog, SuspiciousIP
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.db.models import Q

@shared_task
def flag_suspcious_ip():
    # Get the current time
    MAX_IP_REQUEST_THRESHOLD=0
    SENSITIVE_PATHS = [
        '/login',
        '/admin'
    ]
    current_time = timezone.now()
    one_hour_ago = current_time - timedelta(hours=22)
    ip_addresses = RequestLog.objects.filter(timestamp__gte=one_hour_ago).values('ip_address').annotate(ip_count=Count('ip_address'), sensitive_count=Count('path', filter=Q(path__in=SENSITIVE_PATHS)))

    flagged_ips = []
    print(list(ip_addresses))
    # Check if the IP address exceeds the threshold
    for ip in ip_addresses:
        if ip['ip_count'] > MAX_IP_REQUEST_THRESHOLD or ip['sensitive_count'] > 0:
            reason = "Too many requests or accessed sensitive paths within the last 24 hours"
            reason = "IP has made too many requests within the hour hence flagged as suspicious"
            # Check if it exists, create if not
            sus_ip, created = SuspiciousIP.objects.get_or_create(
                ip_address=ip['ip_address'],
                defaults={"reason": reason}
            )

            if created:
                flagged_ips.append(ip['ip_address'])
                print(f"Flagged suspicious IP: {ip['ip_address']}")

    return {
        "flagged_count": len(flagged_ips),
        "flagged_ips": flagged_ips
    }
   