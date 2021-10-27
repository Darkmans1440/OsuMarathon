import os
import random
import shutil
from shutil import copyfile
from tkinter import Tk
from tkinter.filedialog import askdirectory
from zipfile import ZipFile

import FileProperties
import Variables
from commands.Command import Command, argument_to_int_parameter
from pydub import AudioSegment


class CreateMarathonCommand(Command):

    def __init__(self):
        super().__init__("create", "(spacing-between-beatmaps-in-seconds) opens a directory picker to choose where to save the output marathon")

    def execute(self, params):

        if len(params) < 1:
            Variables.last_command_message = "Insufficient parameters for Create"
            return

        map_spacing = argument_to_int_parameter(params[0])

        if map_spacing is None or map_spacing < 1:
            Variables.last_command_message = "First argument for Create must be an integer and at least 1"
            return

        map_spacing = map_spacing * 1000

        if len(Variables.loaded_properties) < 2:
            Variables.last_command_message = "Must have at least 2 beatmaps to create a marathon"
            return

        if Variables.default_values["Title"] == "":
            Variables.last_command_message = "Marathon title must be set"
            return

        if Variables.default_values["Version"] == "":
            Variables.last_command_message = "Marathon version must be set"
            return

        Tk().withdraw()
        save_at = askdirectory()

        if not os.path.exists(save_at):
            Variables.last_command_message = "Path doesn't exist for create"
            return

        bpm_map = FileProperties.OsuProperties("")

        bpm_append_at = 0

        for loaded_map in Variables.loaded_properties:

            for obj in loaded_map.get_hitobjects():
                copy = FileProperties.HitObject(str(obj))

                bpm_map.mutate_append_hitobject(bpm_append_at, copy)

            for loaded_timingpoint in loaded_map.get_timingpoints():
                copy = FileProperties.TimingPoint(str(loaded_timingpoint))

                bpm_map.mutate_append_timingpoint(bpm_append_at, copy)

            bpm_append_at += loaded_map.get_length()

        new_average_bpm = bpm_map.get_average_bpm()
        new_map = FileProperties.OsuProperties(Variables.loaded_properties[0].get_filename())
        new_map.exists_and_read()
        new_map.get_hitobjects().clear()
        new_map.get_timingpoints().clear()

        append_at = 0
        audio_segment = AudioSegment.empty()

        loaded_map: FileProperties.OsuProperties
        for loaded_map in Variables.loaded_properties:

            for hitobject in loaded_map.get_hitobjects():
                new_map.mutate_append_hitobject(append_at if append_at > 0 else 0,
                                                FileProperties.HitObject(str(hitobject)))

            for point in loaded_map.get_timingpoints():

                if point.is_inherited():
                    continue

                data = str(point)

                inherited = FileProperties.TimingPoint(data)
                inherited.set_inherited(True)
                inherited.normalize_to(new_average_bpm)

                new_map.mutate_append_timingpoint(append_at if append_at > 0 else 0,
                                                  FileProperties.TimingPoint(data))
                new_map.mutate_append_timingpoint(append_at if append_at > 0 else 0, inherited)

            audio_file_dir = os.path.dirname(loaded_map.get_filename()) + "\\"

            map_length = loaded_map.get_length()

            with open(audio_file_dir + loaded_map.get_properties("[General]")["AudioFilename"], 'rb') as file:

                append_segment = AudioSegment.from_file(file)

                leftover_length = (append_segment.duration_seconds * 1000) - map_length

                if leftover_length >= 500:
                    append_segment = append_segment[:map_length + 500].fade_out(500)
                    append_segment += AudioSegment.silent(map_spacing - 500)
                else:
                    append_segment = append_segment[:map_length]
                    append_segment += AudioSegment.silent(map_spacing)

                audio_segment += append_segment

            append_at += map_length + map_spacing

        directory = os.getcwd() + "\\output\\"
        os.makedirs(directory, exist_ok=True)

        new_map.set_property("[General]", "AudioFilename", "audio-combined.mp3")
        new_map.set_property("[Metadata]", "Title", Variables.default_values["Title"])
        new_map.set_property("[Metadata]", "TitleUnicode", Variables.default_values["Title"])
        new_map.set_property("[Metadata]", "Artist", Variables.default_values["Artist"])
        new_map.set_property("[Metadata]", "ArtistUnicode", Variables.default_values["Artist"])
        new_map.set_property("[Metadata]", "Creator", Variables.default_values["Creator"])
        new_map.set_property("[Metadata]", "Version", Variables.default_values["Version"])
        new_map.set_property("[Metadata]", "Source", Variables.default_values["Source"])
        new_map.set_property("[Metadata]", "Tags", Variables.default_values["Tags"])
        new_map.set_property("[Metadata]", "BeatmapID", str(0))
        new_map.set_property("[Metadata]", "BeatmapSetID", str(-1))
        new_map.set_property("[Difficulty]", "HPDrainRate", Variables.default_values["HP"])
        new_map.set_property("[Difficulty]", "OverallDifficulty", Variables.default_values["OD"])

        background_path = Variables.default_values["Background"]
        new_background_path = ""
        new_background_name = ""

        if background_path != "":
            new_background_name = "background" + background_path[background_path.rindex('.'):]
            new_background_path = directory + new_background_name
            new_map.set_background(new_background_name)
            copyfile(background_path, new_background_path)

        osu_path = directory + "osu-combined.osu"
        audio_path = directory + "audio-combined.mp3"

        new_map.write(osu_path)

        print("Creating audio... this may take some time (message will delete once it's complete)")

        audio_segment.export(audio_path, format="mp3", bitrate="192k")

        osz_path = save_at + "\\" + Variables.slugify(
            Variables.default_values["Artist"] + " - " +
            Variables.default_values["Title"])

        with ZipFile(osz_path + ".osz", 'w') as zipfile:
            if new_background_path != "":
                zipfile.write(new_background_path, arcname=new_background_name)
            zipfile.write(osu_path, arcname=str(random.randint(1, 1000)) + "-osu-combined.osu")
            zipfile.write(audio_path, arcname="audio-combined.mp3")

        shutil.rmtree(directory)

        Variables.last_command_message = "Successfully created marathon '" + Variables.default_values[
            "Title"] + "' check the launch directory"
