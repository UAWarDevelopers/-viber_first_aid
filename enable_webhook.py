import os

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

# Viber Bot API requires execution of a single command to set endpoint
# for forwarding messages sent to bot

USE_LOCAL = False

LOCAL_ENDPOINT = None
LOCAL_BOT_TOKEN = None

if USE_LOCAL:
    LOCAL_ENDPOINT = "https://97eb-194-44-50-29.ngrok.io"
    LOCAL_BOT_TOKEN = "4ed5219398e7e547-135d020e66f16b38-bd60a24f2643f98b"

viber = Api(BotConfiguration(
    name='ViktorFAR',
    avatar='http://site.com/avatar.jpg',
    auth_token=(LOCAL_BOT_TOKEN or os.environ["BOT_TOKEN"])
))

viber.set_webhook(LOCAL_ENDPOINT or os.environ["BOT_ENDPOINT"])
