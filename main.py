import os

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


def send_text_message(viber_request, text):
    viber.send_messages(
        viber_request.sender.id,
        messages=[TextMessage(text=text)]
    )


def update_buttons(viber_request, buttons):
    viber.send_messages(
        viber_request.sender.id,
        messages=[
            KeyboardMessage(
                tracking_data="tracking_data",
                keyboard=KeyBoardContent(buttons).get_dict_repr()
            )
        ]
    )


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
        selected_option = viber_request.message.text

        # for debug
        send_text_message(viber_request, selected_option)

        if selected_option == " < ":
            options = medical_data.get_back_options()
            bot_answer = medical_data.get_back_answer()

            send_text_message(viber_request, bot_answer)
            update_buttons(viber_request, options)

        else:
            options = medical_data.get_options(selected_option)
            bot_answer = medical_data.get_answer(selected_option)

            send_text_message(viber_request, bot_answer)
            update_buttons(viber_request, options)

        if selected_option == "":
            medical_data.init_begin_level()
            options = medical_data.get_begin_options()
            bot_answer = "Що трапилось?"

            send_text_message(viber_request, bot_answer)
            update_buttons(viber_request, options)

    elif isinstance(viber_request, ViberConversationStartedRequest):
        text = "Відправте будь-яке повідомлення, щоб почати спілкування"
        send_text_message(viber_request, text)

    elif isinstance(viber_request, ViberSubscribedRequest):
        text = "Дякуємо за підписку!"
        send_text_message(viber_request, text)

    elif isinstance(viber_request, ViberFailedRequest):
        logging.warning(
            "client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, debug=True)
