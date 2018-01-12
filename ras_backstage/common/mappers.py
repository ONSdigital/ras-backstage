import re


def format_short_name(short_name):
    return re.sub('(&)', r' \1 ', short_name)
