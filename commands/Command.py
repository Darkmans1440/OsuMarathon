from FileProperties import OsuProperties


def argument_to_int_parameter(arg: str):
    try:
        value = int(arg)

        return 0 if value < 0 else value
    except ValueError:
        return None


def argument_to_osu_properties(arg: str):
    properties = OsuProperties(arg)
    return properties if properties.exists_and_read() else None


class Command:

    def __init__(self, label: str, usage: str):
        self._label = label
        self._usage = usage

    def __str__(self):
        return " - " + self._label + " " + self._usage

    def get_label(self):
        return self._label

    def execute(self, params):
        pass
