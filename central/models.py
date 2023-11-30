from django.db import models


# Create your models here.


class Subscriber(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    language_code = models.CharField(max_length=10, blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    bot = models.ForeignKey("Bot_token", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"
        ordering = ["-date_created"]


class Bot_token(models.Model):
    token = models.CharField(max_length=100, unique=True)
    bot_username = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    start_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.token

    class Meta:
        db_table = 'bot_token'


class Channel(models.Model):
    channel_username = models.CharField(max_length=100, unique=True)
    channel_name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.channel_username

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"
        ordering = ["-date_created"]

    def save(self, *args, **kwargs):
        if not self.channel_username.startswith("@"):
            self.channel_username = "@" + self.channel_username
        if self.channel_name is None:
            self.channel_name = self.channel_username.split("@")[1]

        super().save(*args, **kwargs)


class User_subscribe_channel(models.Model):
    user = models.ForeignKey("Subscriber", on_delete=models.CASCADE, blank=True, null=True)
    channel = models.ForeignKey("Channel", on_delete=models.CASCADE, blank=True, null=True)
    subscribe = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_subscribe_channel'
        unique_together = ('user', 'channel')

    def __str__(self):
        return self.user.user_id


class Channel_bot_settings(models.Model):
    bot = models.ForeignKey("Bot_token", on_delete=models.CASCADE, blank=True, null=True)
    channel = models.ManyToManyField("Channel", blank=True, null=True)
