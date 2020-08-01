"""This imports modules and gets them ready to be used by `Bomb.BombModel`."""

import Modules

# todo: will eventually be replaced with text file and parser
MODULES = ["SimpleWires", "TheButton", "Keypad", "SimonSays", "MorseCode"]


def get_module_list(bomb_reference, parent_reference) -> list:
    module_list = []
    for module_name in MODULES:
        # Module.<module_name>.<module_name>Controller
        controller_class = getattr(getattr(Modules, module_name), module_name+"Controller")
        controller = controller_class(bomb_reference, parent_reference)
        module_list.append(controller)
    return module_list
