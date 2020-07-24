"""The Button Module."""

import tkinter as tk
from typing import Tuple

import BaseModule
import const

import random
import time


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
        self._solution = tuple()  # [0] is HOLD/PRESS, [1] is number for hold or None

        self.init_button()
        self.calc_solution()

    def init_button(self) -> None:
        self._button_colour = random.choice(BUTTON_COLOURS)
        self._button_text = random.choice(LABELS)
        self._strip_colour = random.choice(STRIP_COLOURS)

    def get_button_data(self) -> Tuple[str, str, str]:
        """Returns button colour, button text and strip colour."""
        return self._button_colour, self._button_text, self._strip_colour

    def calc_solution(self) -> None:
        """Sets the calc_solution in the format of (HOLD/PRESS, hold_number/None)"""
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
            self._solution = (PRESS, None)
        elif self._button_colour == const.COL_WHITE and has_car:
            self._solution = (HOLD, hold_number)
        elif battery_count >= 3 and has_frk:
            self._solution = (PRESS, None)
        elif self._button_colour == const.COL_RED and self._button_text == HOLD:
            self._solution = (PRESS, None)
        else:
            self._solution = (HOLD, hold_number)

    def check_solution(self, solution: tuple) -> None:
        """Parameter `solution` has [0] as PRESS/HOLD and [1] as current f_time."""
        if solution[0] == self._solution[0] == PRESS or str(self._solution[1]) in solution[1]:
            self.controller.make_solved()
        else:
            self.controller.add_strike()


class TheButtonView(BaseModule.ModuleView):
    BUTTON_FONT = ("Courier", 16)

    BUTTON_TOP_X = 20
    BUTTON_TOP_Y = 60
    BUTTON_DIAMETER = 110
    BUTTON_CENTRE_X = BUTTON_TOP_X + BUTTON_DIAMETER / 2
    BUTTON_CENTRE_Y = BUTTON_TOP_Y + BUTTON_DIAMETER / 2

    STRIP_X_OFFSET = 25
    STRIP_WIDTH = 30
    STRIP_TOP_X = BUTTON_TOP_X + BUTTON_DIAMETER + STRIP_X_OFFSET
    STRIP_BOTTOM_X = STRIP_TOP_X + STRIP_WIDTH

    def __init__(self, bomb_view, controller: "TheButtonController"):
        super().__init__(bomb_view, controller)
        self._button_colour = ""
        self._button_text = ""
        self._strip_colour = ""
        self._strip_id = None  # used to change strip colour when button pressed
        self._pressed_time = 0

    def attach_button_data(self, button_colour: str, button_text: str, strip_colour: str) -> None:
        self._button_colour = button_colour
        self._button_text = button_text
        self._strip_colour = strip_colour
        self.draw_button()

    def draw_button(self) -> None:
        button_id = self.create_oval(
            self.BUTTON_TOP_X,
            self.BUTTON_TOP_Y,
            self.BUTTON_TOP_X + self.BUTTON_DIAMETER,
            self.BUTTON_TOP_Y + self.BUTTON_DIAMETER,
            fill=self._button_colour, outline=const.COL_BLACK
        )
        label_id = self.create_text(
            self.BUTTON_CENTRE_X, self.BUTTON_CENTRE_Y,
            text=self._button_text, font=self.BUTTON_FONT,
            fill=(const.COL_BLACK if self._button_colour not in (const.COL_BLACK, const.COL_BLUE)
                  else const.COL_WHITE)
        )
        self._strip_id = self.create_rectangle(
            self.STRIP_TOP_X,
            self.BUTTON_TOP_Y,
            self.STRIP_BOTTOM_X,
            self.BUTTON_TOP_Y + self.BUTTON_DIAMETER,
            fill=const.COL_BLACK, outline=const.COL_BLACK
        )

        self.tag_bind(button_id, "<ButtonPress-1>", self.on_button_press)
        self.tag_bind(label_id, "<ButtonPress-1>", self.on_button_press)
        self.tag_bind(button_id, "<ButtonRelease-1>", self.on_button_release)
        self.tag_bind(label_id, "<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event) -> None:
        self._pressed_time = time.time()
        self.itemconfigure(self._strip_id, fill=self._strip_colour)

    def on_button_release(self, event) -> None:
        time_held = time.time() - self._pressed_time
        if time_held <= 0.2:
            response = (PRESS, self.controller.get_f_time())
        else:
            response = (HOLD, self.controller.get_f_time())
        self.itemconfigure(self._strip_id, fill=const.COL_BLACK)
        self.controller.check_solution(response)


class TheButtonController(BaseModule.ModuleController):
    model_class = TheButtonModel
    view_class = TheButtonView

    def __init__(self, bomb_reference, parent_reference: tk.Frame):
        super().__init__(bomb_reference, parent_reference)
        self.view.attach_button_data(*self.model.get_button_data())

    def check_solution(self, solution: tuple) -> None:
        self.model.check_solution(solution)
