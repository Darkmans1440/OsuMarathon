from tkinter import Tk
from tkinter.filedialog import askopenfilename

import Variables
from commands.Command import Command


class PropertyCommand(Command):

    def __init__(self):
        super().__init__("property",
                         "<2 arguments, (e.x title \"my custom title\"), prints possible properties if no arguments. Background requires no arguments)>")

    def execute(self, params):

        size = len(params)

        if size > 0:
            if params[0].capitalize() != "Background" and size < 2:
                Variables.last_command_message = str(list(Variables.default_values.keys()))
                return

        arg = params[0].capitalize()
        prop = Variables.default_values.get(arg)

        if prop is None:
            Variables.last_command_message = "Property '" + arg + "' not found."
            return

        new_value = ""

        if arg == "Background":
            Tk().withdraw()
            filename = askopenfilename(
                filetypes=[("image files", "*.jpg"), ("image files", "*.jpeg"), ("image files", "*.png")])
            new_value = filename
        else:
            new_value = params[1]

        Variables.default_values[arg] = new_value
        Variables.last_command_message = "Set Property '" + arg + "' to '" + new_value + "'"
