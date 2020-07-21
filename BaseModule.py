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

    def get_indicators(self) -> List[Tuple[str, bool]]:
        return self.controller.get_indicators()

    def get_batteries(self) -> List[str]:
        return self.controller.get_batteries()

    def get_ports(self) -> List[str]:
        return self.controller.get_ports()

    def get_serial(self) -> str:
        return self.controller.get_serial()


class ModuleView(tk.Canvas):
    def __init__(self, parent, controller: "ModuleController", *args):
        super().__init__(parent)
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

    def flash_wrong(self, previous_fill: str = None) -> None:
        """Flashes red on the led."""
        if previous_fill is not None:
            self.itemconfigure(self.led_id, fill=previous_fill)
        else:
            current_fill = self.itemcget(self.led_id, "fill")
            self.itemconfigure(self.led_id, fill=const.MODULE_LED_WRONG)
            self.after(500, self.flash_wrong, current_fill)


class ModuleController(object):
    model_class = ModuleModel
    view_class = ModuleView

    def __init__(self, bomb_reference: Bomb.BombModel, parent_reference: tk.Frame, *args):
        # todo: am i even using *args here? not that useful tbh but i'll keep it for now
        self._bomb = bomb_reference
        self.model = self.model_class(self)
        self.view = self.view_class(parent_reference, *args)

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

    def make_solved(self) -> None:
        self.view.make_solved()
