import logging
import os

from flask import Flask
from flask import request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage, KeyboardMessage, PictureMessage
from viberbot.api.viber_requests import ViberMessageRequest, \
    ViberConversationStartedRequest, ViberSubscribedRequest, \
    ViberFailedRequest

from parse_medical_data.read_medical_data import ReadMedicalData
from utils.keyboard_content import KeyBoardContent

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


def send_messages_block(user_id: str, text: str, options_by_hierarchy: dict = None):
    """
    Send text and keyboard to user
    :param user_id: viber id of receiver
    :param text: message text
    :param options_by_hierarchy: optional. if passed will also send keyboard
    with specified options
    """

    print(f"user_id: {user_id}, text: {text[:10] if text is not None else None}, "
          f"options: "
          f"{list(options_by_hierarchy.items())[:min(3, len(options_by_hierarchy))] if options_by_hierarchy is not None else None}")

    messages_to_send = [TextMessage(text=text)]

    if options_by_hierarchy:
        messages_to_send.append(
            KeyboardMessage(
                tracking_data="tracking_data",
                keyboard=KeyBoardContent(options_by_hierarchy).get_dict_repr()
            )
        )

    viber.send_messages(
        to=user_id,
        messages=messages_to_send
    )


def send_text_message(user_id: str, text: str):
    viber.send_messages(
        to=user_id,
        messages=[TextMessage(text=text)]
    )


def send_keyboard_message(user_id: str, options_by_hierarchy: dict):
    viber.send_messages(
        to=user_id,
        messages=[KeyboardMessage(
            tracking_data="tracking_data",
            keyboard=KeyBoardContent(options_by_hierarchy).get_dict_repr()
        )]
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


def send_next_block(user_id, current_option_id):
    """
    Send next message and keyboard to user
    :param user_id: viber receiver id
    :param current_option_id: id of current option
    :return: True if there is next options for user. False otherwise
    """
    medical_data.set_medical_data(current_option_id)

    options_by_hierarchy = medical_data.get_options()
    answer = medical_data.get_answer()
    link = medical_data.get_link()

    if current_option_id != "0":
        options_by_hierarchy[current_option_id[:-2] if len(
            current_option_id) > 1 else 0] = "Повернутися до попереднього"
        options_by_hierarchy["0"] = "Повернутися до меню"

    send_image(user_id, link, "")
    send_messages_block(user_id, answer,
                        options_by_hierarchy)



@app.route('/', methods=['POST'])
def incoming():
    logging.debug("received request. post data: {0}".format(request.get_data()))

    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(),
                                  request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this utils supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberConversationStartedRequest):
        welcome_text = "Щоб почати спілкування, надішліть \"Старт\""

        send_text_message(viber_request.user.id, welcome_text)

    elif isinstance(viber_request, ViberMessageRequest):
        user_message = viber_request.message.text
        user_id = viber_request.sender.id

        if user_message == "Старт":
            user_message = "0"

        if not medical_data.is_valid_hierarchy(user_message):
            send_text_message(user_id, "Оберіть коректну опцію")

            send_next_block(user_id, current_option_id="0")

            return Response(status=200)

        send_next_block(user_id, user_message)

    elif isinstance(viber_request, ViberSubscribedRequest):
        subscribe_text = "Дякуємо за підписку!"

        send_text_message(viber_request.user.id, subscribe_text)

    elif isinstance(viber_request, ViberFailedRequest):
        logging.warning(
            "client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=(LOCAL_PORT or 443), debug=True)
