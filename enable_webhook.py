
import os

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

# Viber Bot API requires execution of a single command to set endpoint for forwarding messages sent to bot

viber = Api(BotConfiguration(
    name='FirstAidRobot',
    avatar='http://site.com/avatar.jpg',
    auth_token=os.environ["BOT_TOKEN"]
))

viber.set_webhook(os.environ["BOT_ENDPOINT"])
