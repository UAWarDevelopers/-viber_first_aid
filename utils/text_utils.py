import re


def format_message(text: str) -> str:
    text = re.sub(':[*]', '*:', text)
    return re.sub(r"\\", "", text)
