"""The Button Module."""

import tkinter as tk

import BaseModule
import const

import random


# todo: can things like this be replaced with an enum?
ABORT = "ABORT"
DETONATE = "DETONATE"
HOLD = "HOLD"
PRESS = "PRESS"
LABELS = [ABORT, DETONATE, HOLD, PRESS]

BUTTON_COLOURS = [const.COL_BLUE, const.COL_RED, const.COL_WHITE, const.COL_YELLOW, const.COL_BLACK]
STRIP_COLOURS = [const.COL_BLUE, const.COL_RED, const.COL_WHITE, const.COL_YELLOW]


class TheButtonModel(BaseModule.ModuleModel):
    def __init__(self, controller: "TheButtonController"):
        super().__init__(controller)
        self._button_colour = ""
        self._button_text = ""
        self._strip_colour = ""
        self._solution = tuple()  # [0] is HOLD/PRESS, [1] is number for hold

        self.init_button()
        self.calc_solution()

        # todo: resume from here: make function which checks duration, checks ftime etc.

    def init_button(self) -> None:
        self._button_colour = random.choice(BUTTON_COLOURS)
        self._button_text = random.choice(LABELS)
        self._strip_colour = random.choice(STRIP_COLOURS)

    def calc_solution(self) -> None:
        """Sets the calc_solution in the format of (HOLD/PRESS, hold_number)"""
        battery_count = len(self.controller.get_batteries())
        has_car = (const.IND_CAR, const.IND_ON) in self.controller.get_indicators()
        has_frk = (const.IND_FRK, const.IND_ON) in self.controller.get_indicators()
        if self._strip_colour == const.COL_YELLOW:
            hold_number = 5
        elif self._strip_colour == const.COL_BLUE:
            hold_number = 4
        else:
            hold_number = 1

        if self._button_colour == const.COL_BLUE and self._button_text == ABORT:
            self._solution = (HOLD, hold_number)
        elif battery_count >= 2 and self._button_text == DETONATE:
            self._solution = (PRESS,)
        elif self._button_colour == const.COL_WHITE and has_car:
            self._solution = (HOLD, hold_number)
        elif battery_count >= 3 and has_frk:
            self._solution = (PRESS,)
        elif self._button_colour == const.COL_RED and self._button_text == HOLD:
            self._solution = (PRESS,)
        else:
            self._solution = (HOLD, hold_number)



class TheButtonView(BaseModule.ModuleView):

    def __init__(self, bomb_view, controller: "TheButtonController"):
        super().__init__(bomb_view, controller)

    # Define more methods, modify __init__


class TheButtonController(BaseModule.ModuleController):
    model_class = TheButtonModel
    view_class = TheButtonView

    def __init__(self, bomb_reference, parent_reference: tk.Frame):
        super().__init__(bomb_reference, parent_reference)

    # Define more methods, modify __init__
