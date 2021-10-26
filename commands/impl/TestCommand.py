import os

import pydub.effects
from pydub import AudioSegment

from commands.Command import Command


class TestCommand(Command):

    def __init__(self):
        super().__init__("test", "")

    def execute(self, params):

        directory = os.getcwd() + "\\output\\"
        os.makedirs(directory, exist_ok=True)

        with open(params[0], 'rb') as file:
            audio_segment = AudioSegment.from_file(file)
            pydub.effects.speedup(seg=audio_segment, playback_speed=1.5).export(directory + "test.mp3", format="mp3", bitrate="192k")
