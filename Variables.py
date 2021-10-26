import re

import unicodedata

from commands.CommandHandler import CommandHandler

default_values = {
    "Title": "Custom Marathon",
    "Artist": "Various Artists",
    "Creator": "Various Mappers",
    "Version": "Marathon",
    "Source": "",
    "Tags": "",
    "HP": "8",
    "OD": "8",
    "Background": ""
}

last_command_message = "Hi"
loaded_properties = []
handler = CommandHandler()


def get_properties_length():
    if len(loaded_properties) <= 0:
        return "N/A"

    total = 0

    for value in loaded_properties:
        total += value.get_length()

    comp = []

    seconds = int((total / 1000) % 60)
    minutes = int((total / (1000 * 60)) % 60)
    hours = int((total / (1000 * 60 * 60)) % 24)

    if hours > 0:
        comp.append(str(hours) + " hour" + ("s" if hours > 1 else ""))
    if minutes > 0:
        comp.append(str(minutes) + " minute" + ("s" if minutes > 1 else ""))
    if seconds > 0:
        comp.append(str(seconds) + " second" + ("s" if seconds > 1 else ""))

    return ", ".join(comp)


def get_default_values_string():
    string = ""

    for key, value in default_values.items():
        string += key + " = " + ("N/A" if value == "" else value) + "\n"

    return string


def get_loaded_properties_string():
    size = len(loaded_properties)

    string = ""

    if size == 0:
        string = " - none"
    else:
        for i in range(size):
            loaded = loaded_properties[i]
            string += " - " + str(i) + " : " + loaded.get_filename() + "\n"

    return string


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
