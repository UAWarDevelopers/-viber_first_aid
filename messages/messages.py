from messages.keyboard_content import KeyBoardContent
from utils import text_utils
from utils import image_utils

from bot.bot import viber

from viberbot.api.messages import TextMessage, KeyboardMessage, PictureMessage

from medical_data.read_medical_data import ReadMedicalData

medical_data = ReadMedicalData().get_medical_data()


def send_next_block(user_id, current_option_id):
    """
    Send next message and keyboard to user
    :param user_id: viber receiver id
    :param current_option_id: id of current option
    :return: True if there is next options for user. False otherwise
    """
    if not medical_data.is_valid_hierarchy(current_option_id):
        send_text_message(user_id, "Оберіть коректну опцію")
        current_option_id = "0"

    medical_data.set_medical_data(current_option_id)

    options_by_hierarchy = medical_data.get_options()
    answer = medical_data.get_answer()
    google_img_url = medical_data.get_link()
    img_url = image_utils.get_jpg_url(
        google_img_url) if google_img_url is not None else None

    if current_option_id != "0":
        options_by_hierarchy[current_option_id[:-2] if len(
            current_option_id) > 1 else 0] = "Повернутися до попереднього"
        options_by_hierarchy["0"] = "Повернутися до меню"

    send_messages_block(user_id, answer,
                        options_by_hierarchy, img_url)


def send_messages_block(user_id: str, text: str, options_by_hierarchy: dict = None,
                        img_url: str = None):
    """
    Send text and keyboard to user
    :param user_id: viber id of receiver
    :param text: message text
    :param options_by_hierarchy: optional. if passed will also send keyboard
    with specified options
    :param img_url: optional. if passed will also send image
    """

    print(f"user_id: {user_id}, text: {text[:10] if text is not None else None}, "
          f"options: "
          f"{list(options_by_hierarchy.items())[:min(3, len(options_by_hierarchy))] if options_by_hierarchy is not None else None}")

    send_text_message(user_id, text)

    if img_url:
        send_image_message(user_id, img_url, "")

    if options_by_hierarchy:
        send_keyboard_message(user_id, options_by_hierarchy)


def send_text_message(user_id: str, text: str):
    text = text_utils.format_message(text)
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


def send_image_message(user_id, url, text):
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
