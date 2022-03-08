import os

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

from config import LOCAL_BOT_TOKEN, LOCAL_ENDPOINT

# Viber Bot API requires execution of a single command to set endpoint
# for forwarding messages sent to bot


viber = Api(BotConfiguration(
    name='ViktorFAR',
    avatar='http://site.com/avatar.jpg',
    auth_token=(LOCAL_BOT_TOKEN or os.environ["BOT_TOKEN"])
))

viber.set_webhook(LOCAL_ENDPOINT or os.environ["BOT_ENDPOINT"])
