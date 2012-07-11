from django.core.management.base import BaseCommand, CommandError
from sourcessay.models import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for s in Source.objects.all():
            s.process_feed()
