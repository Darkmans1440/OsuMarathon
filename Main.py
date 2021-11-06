import os
import traceback

import Variables
from colorama import Fore, Style
from colorama import init
from commands.impl.LoadBeatmapCommand import LoadBeatmapCommand
from commands.impl.SwapLoadedBeatmapCommand import SwapLoadedBeatmapCommand
from commands.impl.UnloadBeatmapCommand import UnloadBeatmapCommand
from commands.impl.marathon.CreateMarathonCommand import CreateMarathonCommand
from commands.impl.marathon.PropertyCommand import PropertyCommand


def update_message():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{Fore.LIGHTGREEN_EX}<<< Output Marathon Information >>>")
    print(" ")
    print(
        f"{Fore.LIGHTMAGENTA_EX}Estimated Marathon Length {Style.RESET_ALL}= {Fore.LIGHTCYAN_EX}" + Variables.get_properties_length())
    print(Variables.get_default_values_string())
    print(" ")
    print(f"{Fore.LIGHTBLUE_EX}Loaded Beatmaps for Marathon (Format = Index : Beatmap Path)")
    print(Variables.get_loaded_properties_string())
    print(" ")
    print(f"{Fore.YELLOW}Last Command Response {Style.RESET_ALL}: " + Style.BRIGHT + Variables.last_command_message)
    print(" ")
    print(f"{Fore.LIGHTGREEN_EX}<<< Beatmap Commands >>>")
    print(" ")
    print(Variables.handler.get_command_list_string_of(["load", "unload", "swap"]))
    print(" ")
    print(f"{Fore.LIGHTGREEN_EX}<<< Marathon Commands >>>")
    print(" ")
    print(Variables.handler.get_command_list_string_of(["create", "property"]))


def main():
    Variables.handler.register_command(LoadBeatmapCommand())
    Variables.handler.register_command(SwapLoadedBeatmapCommand())
    Variables.handler.register_command(UnloadBeatmapCommand())
    Variables.handler.register_command(CreateMarathonCommand())
    Variables.handler.register_command(PropertyCommand())

    init(autoreset=True)  # colorama init
    os.system('mode con: cols=133 lines=33')

    update_message()

    while True:

        value = str(input())

        if value:

            try:
                Variables.handler.handle_input(value)

                size = len(Variables.loaded_properties)
                os.system(f'mode con: cols=133 lines={str(33 + max(0, size * 2))}')

                update_message()
            except Exception:
                traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
