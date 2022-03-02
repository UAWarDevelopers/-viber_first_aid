from viberbot import Api
from viberbot.api.messages import TextMessage
from viberbot.api.viber_requests import ViberMessageRequest


def handle_message(viber: Api, viber_request: ViberMessageRequest):
    """
    Process message from user
    """

    # TODO: опрацьовувати тут кожне повідомлення. Для подальших цепочок можна перепосилатись на інші ф-ції
    viber.send_messages(viber_request.sender.id, [TextMessage(text="Опрацювання цього пв ще не готове :C")])
