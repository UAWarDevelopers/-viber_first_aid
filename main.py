import logging

from flask import Flask
from flask import request, Response

from viberbot.api.viber_requests import ViberMessageRequest, \
    ViberConversationStartedRequest, ViberSubscribedRequest, \
    ViberFailedRequest

from messages.messages import send_text_message, send_next_block

from bot.bot import viber

from config import LOCAL_PORT

app = Flask(__name__)


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

        send_next_block(user_id, current_option_id=user_message)

    elif isinstance(viber_request, ViberSubscribedRequest):
        subscribe_text = "Дякуємо за підписку!"

        send_text_message(viber_request.user.id, subscribe_text)

    elif isinstance(viber_request, ViberFailedRequest):
        logging.warning(
            "client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=(LOCAL_PORT or 443), debug=True)
