from django.db import models


class RequestLog(models.Model):
    ip_address = models.CharField(max_length=45)
    path = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp} from {self.city}, {self.country}"


class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blocked IP: {self.ip_address}"

class SuspiciousIP(models.Model):
    ip_address = models.CharField(max_length=45)
    reason = models.TextField()

    def __str__(self):
        return f"Suspicious {self.ip_address}: {self.reason}" 