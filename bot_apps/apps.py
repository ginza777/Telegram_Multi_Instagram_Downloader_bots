import django.core.exceptions
import requests.exceptions
import telegram
from django.apps import AppConfig
from django.conf import settings

import environ

env = environ.Env()
env.read_env(".env")


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot_apps'

    # def ready(self):
    #     # Move the import statement inside the method
    #     from central.models import Bot_token
    #     tokens = []
    #     if not Bot_token.objects.filter(token="6567332198:AAF7rO8Gq0MuZgj_XMuOzikW33IM6PwJOLA").exists():
    #         Bot_token.objects.create(
    #             token="6567332198:AAF7rO8Gq0MuZgj_XMuOzikW33IM6PwJOLA",
    #             bot_username="@user_checker_member_bot"
    #         ).save()
    #     else:
    #         tokens = Bot_token.objects.all().values_list("token", flat=True)
    #
    #     try:
    #         bot = {}
    #         i = 0
    #         for bot_token in tokens:
    #             webhook_url = env.str("WEBHOOK_URL")
    #             bot[i] = telegram.Bot(token=bot_token)
    #             bot[i].set_webhook(f"{webhook_url}/bot/handle_telegram_webhook/{bot_token}")
    #             print("Webhook set successfully for bot: {}".format(bot[i].get_me().username))
    #             i += 1
    #     except telegram.error.RetryAfter:
    #         pass
    #     except requests.exceptions.ConnectionError:
    #         print("Connection error. Please check your internet connection")
    #     except django.core.exceptions.ImproperlyConfigured:
    #         print("Improperly configured. Please check your settings")
    #     except telegram.error.Unauthorized:
    #         print("Unauthorized. Please check your group_controller_bot token")
