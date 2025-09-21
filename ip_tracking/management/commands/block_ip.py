from ip_tracking.models import BlockedIP
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Add IP addresses to the block list/database for blocked IPS'
    def add_arguments(self, parser):
        # Here we add an arguments to the command line for the addition of blocked IPs
        parser.add_argument('ip_addressses', nargs='+', type=str, help='List of IP addresses to be added to blockedIp database table')
    
    def handle(self, *args, **options):
        # Clean the database for adding blocked IP
        ip_del = BlockedIP.objects.all().delete()
        self.stdout.write(
                    self.style.WARNING(f"IP addresses in database table cleaned out")
                    )
        print(ip_del)
        for ip_address in options["ip_addressses"]:
            # Add the IP address to the block list/database, check if  the IP address already exists before creating
            try:
                blocked_ip = BlockedIP.objects.get(ip_address=ip_address)
                self.stdout.write(
                    self.style.NOTICE(f"IP address {ip_address} already added")
                    )
            except BlockedIP.DoesNotExist:
                # Create the blocked IP address entry
                blocked_ip = BlockedIP.objects.create(ip_address=ip_address)
            
            # Save the blocked IP address to the database
            blocked_ip.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully added IP address {ip_address} to the blcokedIP database table")
            )