import shlex

import Variables
from commands.Command import Command


class CommandHandler:

    def __init__(self):
        self._commands = {}

    def get_command_list_string_of(self, command_labels: []):

        built = []

        for label in command_labels:

            command = self._commands.get(label.lower())

            if command is None:
                continue

            built.append(command)

        return self.get_command_list_string(built)

    def get_command_list_string(self, command_list=None):
        if command_list is None:
            command_list = self._commands.values()

        return "\n".join([str(element) for element in command_list])

    def register_command(self, command: Command):
        self._commands[command.get_label().lower()] = command

    def handle_input(self, line: str):
        split = shlex.split(line, posix=True)
        thing = self._commands.get(split[0].lower())

        if thing is None:
            Variables.last_command_message = "Unknown command '" + split[0] + "'"
            return

        thing.execute(split[1:len(split)])
