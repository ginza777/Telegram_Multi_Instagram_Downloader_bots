from django.contrib import admin

# Register your models here.
from central.models import Subscriber, Bot_token, Channel


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("user_id", "first_name", "last_name", "username", "language_code", "is_bot", "date_created")
    list_filter = ("user_id", "first_name", "last_name", "username", "language_code", "is_bot", "date_created")
    search_fields = ("user_id", "first_name", "last_name", "username", "language_code", "is_bot", "date_created")

    ordering = ("-date_created",)


@admin.register(Bot_token)
class Bot_tokenAdmin(admin.ModelAdmin):
    list_display = ("token", "bot_username", "date_created")
    list_filter = ("token", "bot_username", "date_created")
    search_fields = ("token", "bot_username", "date_created")

    ordering = ("-date_created",)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("channel_username", "date_created")
    list_filter = ("channel_username", "date_created")

    ordering = ("-date_created",)
