import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.error import BadRequest
from telegram import Update
from telegram.ext import CallbackContext
from central.models import Subscriber, Bot_token, Channel

logger = logging.getLogger(__name__)


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Siz barcha kanallarga obuna bo'ldingiz! ✅")


def start(update: Update, context: CallbackContext) -> None:
    # my bot name
    bot = Bot_token.objects.get(bot_username=f"@{context.bot.username}")
    # agar user bazada mavjud bo'lsa yangilash kerak aks holda qo'shish kerak
    user_id = update.effective_user.id

    if Subscriber.objects.filter(user_id=user_id).exists():
        Subscriber.objects.filter(user_id=user_id).update(first_name=update.effective_user.first_name,
                                                          last_name=update.effective_user.last_name,
                                                          username=update.effective_user.username,
                                                          language_code=update.effective_user.language_code,
                                                          is_bot=update.effective_user.is_bot,
                                                          bot=bot
                                                          )
    else:
        Subscriber.objects.create(user_id=user_id,
                                  first_name=update.effective_user.first_name,
                                  last_name=update.effective_user.last_name,
                                  username=update.effective_user.username,
                                  language_code=update.effective_user.language_code,
                                  is_bot=update.effective_user.is_bot,
                                  bot=bot
                                  ).save()

    # Kanallar nomlari
    # random 4 ta kanal
    channels = Channel.objects.all().order_by('?')[:4]

    channel_usernames = []
    for channel in channels:
        channel_usernames.append(
            {"username": channel.channel_username, "name": channel.channel_name, "subscribed": False})

    # Inline tugmalar yaratish
    buttons = [InlineKeyboardButton(text=f"{channel['name']}  ❌", url=f"https://t.me/{channel['name']}") for channel in
               channel_usernames]
    check_channels_button = InlineKeyboardButton("Tekshirish", callback_data="check_channels")
    buttons.append(check_channels_button)

    keyboard = [[button] for button in buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Iltimos, biror bir kanalga obuna bo'lgandan so'ng 'Tekshirish' tugmasini bosing.",
                              reply_markup=reply_markup)


def check_channels(update: Update, context: CallbackContext) -> None:
    # my bot name
    query = update.callback_query
    user_id = update.effective_user.id

    # Kanallar nomlari
    channels = Channel.objects.all().order_by('?')[:4]

    channel_usernames = []
    for channel in channels:
        channel_usernames.append(
            {"username": channel.channel_username, "name": channel.channel_name, "subscribed": False})

    subscribed_channels = []
    bot_cheker = Bot(token="6567332198:AAF7rO8Gq0MuZgj_XMuOzikW33IM6PwJOLA")
    for channel in channel_usernames:
        try:
            chat_member = bot_cheker.get_chat_member(channel['username'], user_id)
            if chat_member and chat_member.status == "member" or chat_member.status == "creator" or chat_member.status == "administrator":
                channel['subscribed'] = True
            else:
                channel['subscribed'] = False
        except BadRequest as e:
            # Handle the case where the user is not found in the channel
            if "User not found" not in str(e):
                print(f"Unexpected error getting chat member for {channel['name']}: {e}")

    old_message_text = query.message.text
    old_reply_markup = query.message.reply_markup
    new_buttons = [InlineKeyboardButton(
        text=f"{channel['name']}  ❌", url=f"https://t.me/{channel['name']}") if not channel[
        'subscribed'] else InlineKeyboardButton(
        text=f"{channel['name']}  ✅", callback_data=f"unsubscribe_{channel['username']}") for channel in
                   channel_usernames]
    new_message = "Siz barcha kanallarga obuna bo'ldingiz! ✅" if all(channel['subscribed'] for channel in
                                                                     channel_usernames) else f"Siz {channel_usernames[0]['name']} kanaliga obuna bo'lmagansiz! ❌"
    new_check_channels_button = InlineKeyboardButton("Tekshirish", callback_data="check_channels")
    new_buttons.append(new_check_channels_button)
    new_keyboard = [[button] for button in new_buttons]
    new_reply_markup = InlineKeyboardMarkup(new_keyboard)
    if old_message_text != new_message or old_reply_markup != new_reply_markup:
        # Edit the message only if there's a change
        query.edit_message_text(new_message, reply_markup=new_reply_markup)


def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    channel_username = query.data.split("_")[1]

    # Foydalanuvchi kanalda bo'lsa, obunani bekor qiladi; aks holda, obunani o'rnatadi
    chat_member = context.bot.get_chat_member(channel_username, user_id)
    if chat_member and chat_member.status == "member":
        context.bot.leave_chat(channel_username)
        query.answer("Siz kanal obunasini bekor qildingiz! ✅")
    else:
        context.bot.send_message(user_id, f"Siz {channel_username} kanaliga obuna bo'ldingiz! ✅")
        query.answer("Siz kanalga muvaffaqiyatli obuna bo'ldingiz! ✅")
