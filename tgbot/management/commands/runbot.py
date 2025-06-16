from django.core.management.base import BaseCommand
from tgbot.bot import run_bot

class Command(BaseCommand):
    help = "Telegram-ботни ишга туширади"

    def handle(self, *args, **kwargs):
        run_bot()
