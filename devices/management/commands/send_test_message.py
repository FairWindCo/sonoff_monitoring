from django.conf import settings
from django.core.management import BaseCommand, CommandError

from telegrams.telegram_message import run_send_message_to_client


class Command(BaseCommand):
    help = 'Send Test Message to Telegram'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user', help='Telergam users list', default='Me')
        parser.add_argument('-m', '--message', help='Message', default='Test Message!')

    def handle(self, *args, **options):
        if settings.TELEGRAM_API_ID and settings.TELEGRAM_HASH:
            run_send_message_to_client(options['user'], options['message'], settings.TELEGRAM_API_ID,
                                       settings.TELEGRAM_HASH)
        else:
            raise CommandError('No TELEGRAM id in config value')
