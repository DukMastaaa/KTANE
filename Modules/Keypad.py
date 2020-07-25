"""Keypad module."""

import tkinter as tk
from enum import Enum
from typing import List

import BaseModule
import const
import random


class Symbols(Enum):
    # Column 1
    HOOP = "Ϙ"
    A_T = "Ѧ"
    LAMBDA = "ƛ"
    LIGHTNING_BOLT = "Ϟ"
    CAT = "Ѭ"
    SCRIPT_X = "ϗ"
    LEFT_C = "Ͽ"

    # Column 2
    E_DOTS = "Ӭ"
    ROLLERCOASTER_LOOP = "Ҩ"
    WHITE_STAR = "☆"
    QUESTION_MARK = "¿"

    # Column 3
    COPYRIGHT = "©"
    NOSE = "Ѽ"
    X_I = "Җ"
    THREE_WITH_TAIL = "Ԇ"

    # Column 4
    FLAT_SIX = "б"
    PARAGRAPH = "¶"
    B_T = "Ѣ"
    SMILE = "ټ"

    # Column 5
    PSI = "Ψ"
    RIGHT_C = "Ͼ"
    THREE_SNAKE = "Ѯ"
    BLACK_STAR = "★"

    # Column 6
    JIGSAW = "҂"
    ASH = "æ"
    BACKWARDS_N = "Ҋ"
    OMEGA = "Ω"


COLUMN_1 = [Symbols.HOOP, Symbols.A_T, Symbols.LAMBDA, Symbols.LIGHTNING_BOLT,
            Symbols.CAT, Symbols.SCRIPT_X, Symbols.LEFT_C]
COLUMN_2 = [Symbols.E_DOTS, Symbols.HOOP, Symbols.LEFT_C, Symbols.ROLLERCOASTER_LOOP,
            Symbols.WHITE_STAR, Symbols.SCRIPT_X, Symbols.QUESTION_MARK]
COLUMN_3 = [Symbols.COPYRIGHT, Symbols.NOSE, Symbols.ROLLERCOASTER_LOOP, Symbols.X_I,
            Symbols.THREE_WITH_TAIL, Symbols.LAMBDA, Symbols.WHITE_STAR]
COLUMN_4 = [Symbols.FLAT_SIX, Symbols.PARAGRAPH, Symbols.B_T, Symbols.CAT,
            Symbols.X_I, Symbols.QUESTION_MARK, Symbols.SMILE]
COLUMN_5 = [Symbols.PSI, Symbols.SMILE, Symbols.B_T, Symbols.RIGHT_C,
            Symbols.PARAGRAPH, Symbols.THREE_SNAKE, Symbols.BLACK_STAR]
COLUMN_6 = [Symbols.FLAT_SIX, Symbols.E_DOTS, Symbols.JIGSAW, Symbols.ASH,
            Symbols.PSI, Symbols.BACKWARDS_N, Symbols.OMEGA]
COLUMNS = {i: eval(f"COLUMN_{i}") for i in range(1, 7)}


class KeypadModel(BaseModule.ModuleModel):
    def __init__(self, controller: "KeypadController"):
        super().__init__(controller)
        self._column_num = 0
        self._buttons = []
        self._solution = []
        self._buttons_pressed = []  # keeps track of which buttons have been pressed

        self.init_keypad()
        self.calc_solution()

    def init_keypad(self) -> None:
        self._column_num = random.randint(1, 6)
        column_copy = COLUMNS[self._column_num].copy()
        for i in range(4):
            symbol = random.choice(column_copy)
            column_copy.remove(symbol)
            self._buttons.append(symbol)

    def get_keypad_data(self) -> list:
        return self._buttons

    def calc_solution(self) -> None:
        indices = []
        for symbol in self._buttons:
            indices.append(COLUMNS[self._column_num].index(symbol))
        sorted_indices = sorted(indices)
        self._solution = [indices.index(i) for i in sorted_indices]

    def check_solution(self, button_index: int) -> bool:
        """Returns whether the button pressed is next in the correct sequence."""
        # todo: something's wrong here, investigate this first
        #       first click registers but all others trigger a strike
        if button_index in self._buttons_pressed:
            return True
        if button_index == self._solution[0]:
            self._buttons_pressed.append(button_index)
            if len(self._buttons_pressed) == 4:
                self.controller.make_solved()
            return True
        else:
            self.controller.add_strike()
            return False


class KeypadView(BaseModule.ModuleView):
    BUTTON_0_TOP_X = 40
    BUTTON_0_TOP_Y = 60
    BUTTON_SIDE_LENGTH = 40
    BUTTON_GAP = 20
    COL_NEUTRAL = "gray"
    COL_CORRECT = "green"
    SYMBOL_FONT = ("TkDefaultFont", 20)

    def __init__(self, bomb_view, controller: "KeypadController"):
        super().__init__(bomb_view, controller)
        self._buttons = []
        self._is_correct = [None] * 4
        self._button_ids = []
        self._symbol_ids = []  # just in case user clicks symbol instead of button

    def attach_buttons(self, buttons: List[str]) -> None:
        self._buttons = buttons
        self.draw_keypad()

    def draw_keypad(self) -> None:
        starting_y = self.BUTTON_0_TOP_Y
        for col in range(2):
            starting_x = self.BUTTON_0_TOP_X
            for row in range(2):
                button_index = col * 2 + row
                bottom_x = starting_x + self.BUTTON_SIDE_LENGTH
                bottom_y = starting_y + self.BUTTON_SIDE_LENGTH
                button_id = self.create_rectangle(
                    starting_x, starting_y, bottom_x, bottom_y,
                    fill=self.COL_NEUTRAL, outline=const.COL_BLACK
                )
                text_id = self.create_text(
                    (starting_x + bottom_x) / 2,
                    (starting_y + bottom_y) / 2,
                    font=self.SYMBOL_FONT,
                    text=self._buttons[button_index].value
                )
                self._button_ids.append(button_id)
                self._symbol_ids.append(text_id)
                self.tag_bind(button_id, const.BIND_LEFT_PRESS, self.on_button_click)
                self.tag_bind(text_id, const.BIND_LEFT_PRESS, self.on_button_click)

                starting_x += self.BUTTON_SIDE_LENGTH + self.BUTTON_GAP
            starting_y += self.BUTTON_SIDE_LENGTH + self.BUTTON_GAP

    def on_button_click(self, event) -> None:
        closest_id = self.find_closest(event.x, event.y)[0]
        button_index = self._button_ids.index(closest_id) if closest_id in self._button_ids \
            else self._symbol_ids.index(closest_id)
        correct_choice = self.controller.check_solution(button_index)
        if correct_choice:
            self.itemconfigure(self._button_ids[button_index], fill=self.COL_CORRECT)


class KeypadController(BaseModule.ModuleController):
    model_class = KeypadModel
    view_class = KeypadView

    def __init__(self, bomb_reference, parent_reference: tk.Frame):
        super().__init__(bomb_reference, parent_reference)
        self.view.attach_buttons(self.model.get_keypad_data())

    def check_solution(self, button_index: int) -> bool:
        return self.model.check_solution(button_index)
