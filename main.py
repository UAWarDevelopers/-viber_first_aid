import os

import logging

from flask import Flask
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

from flask import request, Response
from viberbot.api.messages import TextMessage, KeyboardMessage, PictureMessage
from viberbot.api.viber_requests import ViberMessageRequest, \
    ViberConversationStartedRequest, ViberSubscribedRequest, \
    ViberFailedRequest

from handlers.handlers import handle_message
from handlers.keyboard_content import KeyBoardContent

from parse_medical_data.read_medical_data import ReadMedicalData

app = Flask(__name__)

USE_LOCAL = False

LOCAL_BOT_TOKEN = None
LOCAL_PORT = None

if USE_LOCAL:
    LOCAL_BOT_TOKEN = "4ed5219398e7e547-135d020e66f16b38-bd60a24f2643f98b"
    LOCAL_PORT = 5001

viber = Api(BotConfiguration(
    name='FirstAidRobot',
    avatar='http://site.com/avatar.jpg',
    auth_token=(LOCAL_BOT_TOKEN or os.environ["BOT_TOKEN"])
))

medical_data = ReadMedicalData().get_medical_data()


def send_text_message(user_id, text):
    print(f"user_id: {user_id}, text: {text}")
    viber.send_messages(
        user_id,
        messages=[TextMessage(text=text)]
    )


def update_buttons(user_id, buttons):
    viber.send_messages(
        user_id,
        messages=[
            KeyboardMessage(
                tracking_data="tracking_data",
                keyboard=KeyBoardContent(buttons).get_dict_repr()
            )
        ]
    )


def send_image(user_id, url, text):
    if url:
        viber.send_messages(
            user_id,
            messages=[
                PictureMessage(
                    media=url,
                    text=text
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
        send_text_message(viber_request.sender.id, selected_option)

        if selected_option == "":
            medical_data.init_begin_level()
            begin_options = medical_data.get_begin_options()
            answer = medical_data.get_answer()

            send_text_message(viber_request.sender.id, answer)
            update_buttons(viber_request.sender.id, begin_options)

        elif selected_option == " < ":
            medical_data.select_back_option()
            back_options = medical_data.get_back_options()
            answer = medical_data.get_answer()
            link = medical_data.get_link()

            send_text_message(viber_request.sender.id, answer)
            update_buttons(viber_request.sender.id, back_options)

        else:
            medical_data.select_next_option(selected_option)
            next_options = medical_data.get_next_options()
            answer = medical_data.get_answer()
            link = medical_data.get_link()

            send_text_message(viber_request.sender.id, answer)
            update_buttons(viber_request.sender.id, next_options)
            #send_image(link, answer)

    elif isinstance(viber_request, ViberConversationStartedRequest):
        text = "Відправте будь-яке повідомлення, щоб почати спілкування"
        send_text_message(viber_request.user.id, text)

    elif isinstance(viber_request, ViberSubscribedRequest):
        text = "Дякуємо за підписку!"
        send_text_message(viber_request.user.id, text)

    elif isinstance(viber_request, ViberFailedRequest):
        logging.warning(
            "client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=(LOCAL_PORT or 443), debug=True)
