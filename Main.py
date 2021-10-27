import os
import traceback

from colorama import Fore, Style
from colorama import init

import Variables
from commands.impl.LoadBeatmapCommand import LoadBeatmapCommand
from commands.impl.SwapLoadedBeatmapCommand import SwapLoadedBeatmapCommand
from commands.impl.UnloadBeatmapCommand import UnloadBeatmapCommand
from commands.impl.marathon.CreateMarathonCommand import CreateMarathonCommand
from commands.impl.marathon.PropertyCommand import PropertyCommand

Variables.handler.register_command(LoadBeatmapCommand())
Variables.handler.register_command(SwapLoadedBeatmapCommand())
Variables.handler.register_command(UnloadBeatmapCommand())
Variables.handler.register_command(CreateMarathonCommand())
Variables.handler.register_command(PropertyCommand())


def update_message():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(">>> Marathon <<<\n")
    print(f"{Fore.GREEN}Last Command Message: " + Variables.last_command_message + f"{Style.RESET_ALL}\n")
    print(Variables.get_default_values_string())
    print("Estimated Marathon Length = \"" + Variables.get_properties_length() + "\"")
    print("\nLoaded Beatmaps (Numbers = beatmap index):\n" + Variables.get_loaded_properties_string())
    print("Beatmap Commands:\n" + Variables.handler.get_command_list_string_of(["load", "unload", "swap"]))
    print("Marathon Commands:\n" + Variables.handler.get_command_list_string_of(["create", "property"]))


def run():
    update_message()

    while True:

        value = str(input())

        if value:

            try:
                Variables.handler.handle_input(value)
                update_message()
            except Exception:
                traceback.print_exc()


init(autoreset=True)  # colorama init
run()
