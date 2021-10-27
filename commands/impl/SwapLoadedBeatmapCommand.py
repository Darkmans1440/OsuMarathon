import Variables
from commands.Command import Command, argument_to_int_parameter


class SwapLoadedBeatmapCommand(Command):

    def __init__(self):
        super().__init__("swap", "(first-index) (second-index) swaps the <first-index> beatmap with the <second-index> beatmap")

    def execute(self, params):

        size = len(Variables.loaded_properties)

        if len(Variables.loaded_properties) <= 0:
            Variables.last_command_message = "No beatmaps loaded to swap."
            return

        if len(params) < 2:
            Variables.last_command_message = "Incorrect parameters for swap."
            return

        index_a = argument_to_int_parameter(params[0])
        index_b = argument_to_int_parameter(params[1])

        if index_a is None or index_b is None:
            Variables.last_command_message = "First and second argument for swap must be integers"
            return

        if index_a >= size:
            Variables.last_command_message = "First argument of swap is out of bounds."
            return

        if index_b >= size:
            Variables.last_command_message = "Second argument of swap is out of bounds."
            return
        if index_a == index_b:
            Variables.last_command_message = "First and second argument for swap cannot match"
            return

        value_a = Variables.loaded_properties[index_a]
        value_b = Variables.loaded_properties[index_b]

        Variables.loaded_properties[index_a] = value_b
        Variables.loaded_properties[index_b] = value_a

        Variables.last_command_message = "Swapped beatmaps " + str(index_a) + " and " + str(index_b)
