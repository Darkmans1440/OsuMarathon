import Variables
from commands.Command import Command, argument_to_int_parameter


class UnloadBeatmapCommand(Command):

    def __init__(self):
        super().__init__("unload",
                         "(index or 'all') unloads the beatmap at the given index or every beatmap if 'all' is specified")

    def execute(self, params):
        if len(params) <= 0:
            Variables.last_command_message = "Incorrect parameters for remove"
            return

        size = len(Variables.loaded_properties)

        if params[0].lower() == "all":
            delete_count = size
            Variables.loaded_properties.clear()
        else:
            value = argument_to_int_parameter(params[0])

            if value is None:
                Variables.last_command_message = "First argument for remove must either be all or an integer"
                return

            if value >= size:
                Variables.last_command_message = "First argument of remove is out of bounds"
                return

            delete_count = 1
            Variables.loaded_properties.pop(value)

        Variables.last_command_message = "Unloaded " + str(delete_count) + " Beatmap(s)"
