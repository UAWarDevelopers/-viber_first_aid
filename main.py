import json
import logging

from flask import Flask
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

from flask import request, Response
from viberbot.api.messages import TextMessage
from viberbot.api.viber_requests import ViberMessageRequest, ViberConversationStartedRequest, ViberSubscribedRequest, \
    ViberFailedRequest

from handlers.handlers import handle_message

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='FirstAidDevBot',
    avatar='',
    auth_token=TOKEN
))

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()


@app.route('/', methods=['POST'])
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    with open("viber_bot/keyboard.json") as json_file:
        kb = json.load(json_file)

    if isinstance(viber_request, ViberMessageRequest):
        # viber.send_messages(viber_request.sender.id, [
        #     TextMessage(text="Що трапилось?",
        #                 keyboard=kb["MainKeyboard"])
        # ])
        handle_message(viber, viber_request)
    elif isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="Що трапилось?",
                        keyboard=kb["MainKeyboard"])
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="Дякуємо за підписку!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warning("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


if __name__ == "__main__":
    app.run(port=8087, debug=True)
