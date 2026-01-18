from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = "Add an ip to the blocklist"
    def add_arguments(self, parser):
        parser.add_argument('ip', type=str, help="IP adress to add to Blacklist")
    def handle(self, *args, **options):
        ip = options['ip']
        obj, created = BlockedIP.objects.get_or_create(ip_address=ip)
        if created:
            self.stdout.write(self.style.SUCCESS(f"ip Address Blocked Successfully"))
        else:
            self.stdout.write(self.style.WARNING(f"ip {ip} already exit in Block list"))