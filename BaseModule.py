from typing import List, Tuple

import tkinter as tk

import Bomb
import const


class ModuleModel(object):
    def __init__(self, controller: "ModuleController"):
        self.controller = controller

    def add_strike(self) -> None:
        self.controller.add_strike()

    def get_time(self) -> float:
        return self.controller.get_time()

    def get_f_time(self) -> str:
        return self.controller.get_f_time()

    def get_indicators(self) -> List[Tuple[str, bool]]:
        return self.controller.get_indicators()

    def get_batteries(self) -> List[str]:
        return self.controller.get_batteries()

    def get_ports(self) -> List[str]:
        return self.controller.get_ports()

    def get_serial(self) -> str:
        return self.controller.get_serial()


class ModuleView(tk.Canvas):
    def __init__(self, parent, controller, *args):
        super().__init__(parent)
        self.config(highlightthickness=const.MODULE_BORDER_WIDTH,
                    highlightbackground=const.MODULE_BORDER_COLOUR,
                    height=const.MODULE_HEIGHT, width=const.MODULE_WIDTH)
        self.controller = controller
        self.led_id = self.create_oval(
            const.MODULE_WIDTH - const.MODULE_LED_DIAMETER - const.MODULE_LED_PAD,
            const.MODULE_LED_PAD,
            const.MODULE_WIDTH - const.MODULE_LED_PAD,
            const.MODULE_LED_DIAMETER + const.MODULE_LED_PAD,
            fill=const.MODULE_LED_NEUTRAL
        )

    def make_solved(self) -> None:
        """Makes the current module solved."""
        self.itemconfigure(self.led_id, fill=const.MODULE_LED_SOLVED)

    def flash_wrong(self) -> None:
        """Flashes red on the led."""
        self.itemconfigure(self.led_id, fill=const.MODULE_LED_WRONG)
        self.after(500, self.restore_flash)

    def restore_flash(self) -> None:
        """Resets the led to the correct colour."""
        self.itemconfigure(self.led_id,
                           fill=const.MODULE_LED_SOLVED if self.controller.is_solved
                           else const.MODULE_LED_NEUTRAL)


class ModuleController(object):
    # todo: there's something not right here - pycharm doesn't know these have been overridden
    model_class = ModuleModel
    view_class = ModuleView

    def __init__(self, bomb_reference: Bomb.BombModel, parent_reference: tk.Frame, *args):
        # todo: am i even using *args here? not that useful tbh but i'll keep it for now
        self._bomb = bomb_reference
        self.model = self.model_class(self)
        self.view = self.view_class(parent_reference, self, *args)
        self.is_solved = False

    def add_strike(self) -> None:
        self._bomb.add_strike()
        self.view.flash_wrong()

    def get_time(self) -> float:
        return self._bomb.get_time()

    def get_indicators(self) -> List[Tuple[str, bool]]:
        return self._bomb.indicators

    def get_batteries(self) -> List[str]:
        return self._bomb.batteries

    def get_ports(self) -> List[str]:
        return self._bomb.ports

    def get_serial(self) -> str:
        return self._bomb.serial

    def get_f_time(self) -> str:
        return self._bomb.get_f_time()

    def make_solved(self) -> None:
        self.is_solved = True
        self.view.make_solved()
