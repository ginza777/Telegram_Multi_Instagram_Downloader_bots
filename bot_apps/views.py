import json
import os
from queue import Queue

from django.conf import settings
from django.http import JsonResponse
from telegram import Bot, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Dispatcher,
    Filters,
    MessageHandler,
    PicklePersistence,
)

from central.models import Bot_token
from .state import state
from .telegrambot import start, check_channels, button_callback, help
import environ

env = environ.Env()
env.read_env(".env")


def setup(token):
    bot = Bot(token=token)
    queue = Queue()
    # create the dispatcher
    if not os.path.exists(os.path.join(settings.BASE_DIR, "media", "state_record")):
        os.makedirs(os.path.join(settings.BASE_DIR, "media", "state_record"))
    dp = Dispatcher(
        bot,
        queue,
        workers=8,
        use_context=True,
        persistence=PicklePersistence(
            filename=os.path.join(settings.BASE_DIR, "media", "state_record", "conversationbot")
        ),
    )

    states = {
        state.MAIN: [
            CommandHandler("start", start),
            CommandHandler("help", help),
            CallbackQueryHandler(check_channels, pattern="^check_channels$"),
            CallbackQueryHandler(button_callback, pattern="^unsubscribe_")
        ]
    }
    entry_points = [CommandHandler("start", start)]
    fallbacks = [CommandHandler("start", start)]

    conversation_handler = ConversationHandler(
        entry_points=entry_points,
        states=states,
        fallbacks=fallbacks,
        persistent=True,
        name="conversationbot",
    )
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CallbackQueryHandler(check_channels, pattern="^check_channels$"))
    dp.add_handler(CallbackQueryHandler(button_callback, pattern="^unsubscribe_"))
    dp.add_handler(conversation_handler)
    return dp


tokens = []

if not Bot_token.objects.filter(token="6567332198:AAF7rO8Gq0MuZgj_XMuOzikW33IM6PwJOLA").exists():
    Bot_token.objects.create(
        token="6567332198:AAF7rO8Gq0MuZgj_XMuOzikW33IM6PwJOLA",
        bot_username="@user_checker_member_bot"
    ).save()
else:
    tokens = Bot_token.objects.all().values_list("token", flat=True)


def handle_telegram_webhook(request, token):
    # Ensure that the provided token is one of the valid tokens
    if token not in tokens:
        return JsonResponse({"status": "error", "message": "Invalid token"})

    # Create the bot instance for the specified token
    bot = Bot(token=token)

    # Process the update for the specific bot
    update = Update.de_json(json.loads(request.body.decode("utf-8")), bot)
    dp = setup(token)
    dp.process_update(update)

    return JsonResponse({"status": "ok"})


def set_telegram_webhook(request, token):
    webhook_url = env.str("WEBHOOK_URL")
    bot = Bot(token=token)
    bot.set_webhook(f"{webhook_url}/bot/handle_telegram_webhook/{token}")
    return JsonResponse({"status": "ok"})
