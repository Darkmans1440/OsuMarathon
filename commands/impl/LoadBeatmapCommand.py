from tkinter import Tk
from tkinter.filedialog import askopenfilenames

import Variables
from FileProperties import OsuProperties
from commands.Command import Command


class LoadBeatmapCommand(Command):

    def __init__(self):
        super().__init__("load", "<1 or no arguments (e.x \"path\\to\\song\\test.osu\"), leave empty to open file picker to load beatmap(s)>")

    def execute(self, params):

        if len(params) > 0:

            loaded = OsuProperties(params[0])

            if not loaded.exists_and_read():
                Variables.last_command_message = "File must exist for load"
                return

            Variables.loaded_properties.append(loaded)
            Variables.last_command_message = "Loaded single file: '" + params[0] + "'"

            return

        Tk().withdraw()

        filenames = askopenfilenames(filetypes=[("osu! files", "*.osu")])

        if len(filenames) > 0:
            Variables.last_command_message = "Loaded file(s): " + str(len(filenames))
            for filename in filenames:
                loaded = OsuProperties(filename)
                loaded.exists_and_read()

                Variables.loaded_properties.append(loaded)
        else:
            Variables.last_command_message = "Cancelled or failed to load files"
