import os

import json
import logging

from flask import Flask
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

from flask import request, Response
from viberbot.api.messages import TextMessage, KeyboardMessage
from viberbot.api.viber_requests import ViberMessageRequest, \
    ViberConversationStartedRequest, ViberSubscribedRequest, \
    ViberFailedRequest

from handlers.handlers import handle_message
from handlers.keyboard_content import KeyBoardContent

from parse_medical_data.read_medical_data import ReadMedicalData

app = Flask(__name__)

viber = Api(BotConfiguration(
    name='FirstAidRobot',
    avatar='http://site.com/avatar.jpg',
    auth_token=os.environ["BOT_TOKEN"]
))

medical_data = ReadMedicalData().get_medical_data()


@app.route('/', methods=['POST'])
def incoming():
    logging.debug("received request. post data: {0}".format(request.get_data()))

    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(),
                                  request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        reply = viber_request.message
        options = medical_data.get_next_options(reply)
        question = medical_data.get_answer(reply)
        if reply == " < " or len(options) == 0:
            options = medical_data.get_begin_options()
            question = "Що трапилось?"
        viber.send_messages(viber_request.sender.id,
                            messages=[TextMessage(text=question),
                                      KeyboardMessage(
                                          keyboard=KeyBoardContent(
                                              options).get_json())])
    elif isinstance(viber_request, ViberConversationStartedRequest):
        question = "Що трапилось?"
        options = medical_data.get_begin_options()
        viber.send_messages(viber_request.user.id,
                            messages=[TextMessage(text=question),
                                      KeyboardMessage(
                                          keyboard=KeyBoardContent(
                                              options).get_json())])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="Дякуємо за підписку!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logging.warning(
            "client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, debug=True)
