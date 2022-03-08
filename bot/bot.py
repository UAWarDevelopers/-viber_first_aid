import os

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

from config import LOCAL_BOT_TOKEN

viber = Api(BotConfiguration(
    name='FirstAidRobot',
    avatar='http://site.com/avatar.jpg',
    auth_token=(LOCAL_BOT_TOKEN or os.environ["BOT_TOKEN"])
))
