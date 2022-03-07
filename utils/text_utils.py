import re

PUNCTUATION = ".,:;!?"  # no need to put a space before these marks


def format_message(text: str) -> str:
    text = re.sub(r"\\", "", text)
    text = re.sub(':[*]', '*:', text)
    text = re.sub(':[)]', ': )', text)
    text = re.sub(':[(]', ': (', text)
    text = re.sub('[)]:', ') :', text)
    text = re.sub('[(]:', '( :', text)

    bold_sub_stings = re.findall('.{0,2}[*].*?[*].{0,2}', text)
    for substr in bold_sub_stings:  # type: str

        correct_substr = format_substring(substr, '*')
        if substr != correct_substr:
            text = text.replace(substr, correct_substr, 1)

    underline_sub_strings = re.findall('.{0,2}[_]{2}.*?[_]{2}.{0,2}', text)
    for substr in underline_sub_strings:  # type: str

        correct_substr = format_substring(substr, '__')
        if substr != correct_substr:
            text = text.replace(substr, correct_substr, 1)

    return text


def format_substring(substr: str, format_markdown: str) -> str:

    markdown_split = substr.split(format_markdown)
    if len(markdown_split) <= 2:
        return substr

    # there must not be spaces before format mark,
    # so remove all from begin and end of formatted part of text
    checking = True

    while checking:
        main_part = markdown_split[1]
        if main_part[0] == ' ':
            checking = True
            markdown_split[1] = main_part[1:]
        else:
            checking = False

        if main_part[-1] == ' ':
            checking = True
            markdown_split[1] = main_part[:-1]
        else:
            checking = False if not checking else True

    # before and after format mark must be spaces, add it where needed
    start = markdown_split[0] if markdown_split[0] else ' '
    end = markdown_split[-1] if markdown_split[-1] else ' '

    if start[-1] != ' ' and start[-1] not in PUNCTUATION:
        correct_substr = f' {format_markdown}'.join(markdown_split[:2])
    else:
        correct_substr = f'{format_markdown}'.join(markdown_split[:2])

    if end[0] != ' ' and end[0] not in PUNCTUATION:
        correct_substr += f'{format_markdown} {end}'
    else:
        correct_substr += f'{format_markdown}{end}'

    return correct_substr
