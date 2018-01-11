import re


def format_short_name(short_name):
    short_name = re.sub('(&)', r' \1 ', short_name)
    return short_name
