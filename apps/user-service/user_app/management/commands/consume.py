from django.core.management.base import BaseCommand
from user_app.consumer import start_consumer

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        start_consumer()