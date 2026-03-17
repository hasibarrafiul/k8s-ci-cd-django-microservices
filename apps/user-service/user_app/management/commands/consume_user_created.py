from django.core.management.base import BaseCommand
from user_app.consumer import start_consumer


class Command(BaseCommand):
    help = "Consume user_created events from RabbitMQ"

    def handle(self, *args, **options):
        start_consumer()