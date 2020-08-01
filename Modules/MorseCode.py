"""Morse Code Module."""

import tkinter as tk
import random

import BaseModule
import const


MORSE_WORDS = {'shell': 3.505,  'halls': 3.515,
               'slick': 3.522,  'trick': 3.532,
               'boxes': 3.535,  'leaks': 3.542,
               'strobe': 3.545, 'bistro': 3.552,
               'flick': 3.555,  'bombs': 3.565,
               'break': 3.572,  'brick': 3.575,
               'steak': 3.582,  'sting': 3.592,
               'vector': 3.595, 'beats': 3.6}


class MorseCodeTranslator(object):
    ALPHA_TO_MORSE = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--.."
    }

    @staticmethod
    def encode(plaintext: str) -> str:
        """Encodes plaintext into morse.

        In the ciphertext, there is one space between each character and two spaces
        between each word of the plaintext.

        Use str.strip(" ") to obtain each plaintext character. Spaces between each
        plaintext word will show as an empty string literal.
        """
        plaintext = plaintext.strip()
        ciphertext_list = []
        for char in plaintext:
            if char.isalpha():
                ciphertext_list.append(MorseCodeTranslator.ALPHA_TO_MORSE[char.upper()])
            elif char == " ":
                ciphertext_list.append("")
        return " ".join(ciphertext_list)


class MorseCodeModel(BaseModule.ModuleModel):
    def __init__(self, controller: "MorseCodeController"):
        super().__init__(controller)
        self._word = ""
        self._solution = 0
        self._morse = ""

        self.init_morse_code()
        self.calc_solution()

    def init_morse_code(self) -> None:
        self._word = random.choice(list(MORSE_WORDS))
        self._morse = MorseCodeTranslator.encode(self._word)

    def get_morse_code_data(self) -> str:
        return self._morse

    def calc_solution(self) -> None:
        self._solution = MORSE_WORDS[self._word]

    def check_solution(self, index: int) -> None:
        """Checks whether the index of the word in `MORSE_WORDS` is correct."""
        if MORSE_WORDS[list(MORSE_WORDS)[index]] == self._solution:
            self.controller.make_solved()
        else:
            self.controller.add_strike()


class MorseCodeView(BaseModule.ModuleView):
    DIT_DURATION = 200
    DAH_MULTIPLIER = 3
    SIGNAL_END_MULTIPLIER = 1
    CHAR_END_MULTIPLIER = 3
    WORD_END_MULTIPLIER = 7

    LIGHT_TOP_X = 20
    LIGHT_TOP_Y = 30
    LIGHT_WIDTH = 40
    LIGHT_HEIGHT = 30

    L_ARROW_TOP_X = 20
    L_ARROW_TOP_Y = 90
    L_ARROW_WIDTH = 30
    L_ARROW_HEIGHT = 40

    # geometry yucky
    L_ARROW_BEND_COORD = (L_ARROW_TOP_X, L_ARROW_TOP_Y + L_ARROW_HEIGHT / 2)
    L_ARROW_TOP_COORD = (L_ARROW_TOP_X + L_ARROW_WIDTH, L_ARROW_TOP_Y)
    L_ARROW_BOTTOM_COORD = (L_ARROW_TOP_X + L_ARROW_WIDTH, L_ARROW_TOP_Y + L_ARROW_HEIGHT)
    L_ARROW_COORDS = (*L_ARROW_BEND_COORD, *L_ARROW_TOP_COORD, *L_ARROW_BOTTOM_COORD)

    R_ARROW_BEND_COORD = (const.MODULE_WIDTH - L_ARROW_TOP_X,
                          L_ARROW_TOP_Y + L_ARROW_HEIGHT / 2)
    R_ARROW_TOP_COORD = (const.MODULE_WIDTH - L_ARROW_TOP_X - L_ARROW_WIDTH, L_ARROW_TOP_Y)
    R_ARROW_BOTTOM_COORD = (const.MODULE_WIDTH - L_ARROW_TOP_X - L_ARROW_WIDTH,
                            L_ARROW_TOP_Y + L_ARROW_HEIGHT)
    R_ARROW_COORDS = (*R_ARROW_BEND_COORD, *R_ARROW_TOP_COORD, *R_ARROW_BOTTOM_COORD)

    FREQ_RECT_GAP = 5
    FREQ_RECT_TOP_X = L_ARROW_TOP_X + L_ARROW_WIDTH + FREQ_RECT_GAP
    FREQ_RECT_TOP_Y = L_ARROW_TOP_Y
    FREQ_RECT_BOTTOM_X = R_ARROW_TOP_COORD[0] - FREQ_RECT_GAP
    FREQ_RECT_BOTTOM_Y = L_ARROW_TOP_Y + L_ARROW_HEIGHT
    FREQ_TEXT_X = (FREQ_RECT_TOP_X + FREQ_RECT_BOTTOM_X) / 2
    FREQ_TEXT_Y = (FREQ_RECT_TOP_Y + FREQ_RECT_BOTTOM_Y) / 2
    FREQ_TEXT_FONT = ("Courier", 20)

    TX_WIDTH = 50
    TX_HEIGHT = 30
    TX_TOP_X = const.MODULE_WIDTH / 2 - TX_WIDTH / 2
    TX_TOP_Y = const.MODULE_HEIGHT - TX_HEIGHT - 20
    TX_TEXT_X = TX_TOP_X + TX_WIDTH / 2
    TX_TEXT_Y = TX_TOP_Y + TX_HEIGHT / 2
    TX_TEXT_FONT = ("Courier", 20)

    def __init__(self, bomb_view, controller: "MorseCodeController"):
        super().__init__(bomb_view, controller)
        self._morse = ""
        self._flash_schedule = []
        self._freq_index = 0
        self._light_id = 0
        self._freq_text_id = 0

    def attach_morse_code(self, morse: str):
        self._morse = morse
        self.calculate_flash_schedule()
        self.draw_morse_code()

    def calculate_flash_schedule(self) -> None:
        """Calculates a "schedule" of flashes and the time duration after the initial flash.

        The flash schedule will be a list of tuples where the first element is bool, indicating
        whether the light is on or off. The second element indicates the time in ms after
        the first initial flash.
        """
        chars = self._morse.split()
        time_counter = 0
        for char in chars:
            for signal in char:
                self._flash_schedule.append((True, time_counter))
                if signal == ".":
                    time_counter += self.DIT_DURATION
                elif signal == "-":
                    time_counter += self.DIT_DURATION * self.DAH_MULTIPLIER

                self._flash_schedule.append((False, time_counter))
                time_counter += self.DIT_DURATION * self.SIGNAL_END_MULTIPLIER
            time_counter += self.DIT_DURATION * self.CHAR_END_MULTIPLIER

        time_counter += self.DIT_DURATION * self.WORD_END_MULTIPLIER
        self._flash_schedule.append((False, time_counter))

    def draw_morse_code(self) -> None:
        self._light_id = self.create_rectangle(
            self.LIGHT_TOP_X, self.LIGHT_TOP_Y,
            self.LIGHT_TOP_X + self.LIGHT_WIDTH,
            self.LIGHT_TOP_Y + self.LIGHT_HEIGHT,
            fill=const.COL_BLACK, outline=const.COL_BLACK
        )
        left_id = self.create_polygon(
            *self.L_ARROW_COORDS, fill="light gray", outline=const.COL_BLACK
        )
        right_id = self.create_polygon(
            *self.R_ARROW_COORDS, fill="light gray", outline=const.COL_BLACK
        )
        self.create_rectangle(  # freq rect
            self.FREQ_RECT_TOP_X, self.FREQ_RECT_TOP_Y,
            self.FREQ_RECT_BOTTOM_X, self.FREQ_RECT_BOTTOM_Y,
            fill=const.COL_BLACK
        )
        self._freq_text_id = self.create_text(
            self.FREQ_TEXT_X, self.FREQ_TEXT_Y,
            text=list(MORSE_WORDS.values())[self._freq_index],
            font=self.FREQ_TEXT_FONT, fill=const.COL_WHITE
        )
        tx_rect_id = self.create_rectangle(
            self.TX_TOP_X, self.TX_TOP_Y,
            self.TX_TOP_X + self.TX_WIDTH,
            self.TX_TOP_Y + self.TX_HEIGHT,
            fill="light gray", outline=const.COL_BLACK
        )
        tx_text_id = self.create_text(
            self.TX_TEXT_X, self.TX_TEXT_Y,
            text="TX", font=self.TX_TEXT_FONT
        )

        self.tag_bind(left_id, const.BIND_LEFT_PRESS, lambda event: self.arrow_press(False))
        self.tag_bind(right_id, const.BIND_LEFT_PRESS, lambda event: self.arrow_press(True))
        self.tag_bind(tx_rect_id, const.BIND_LEFT_PRESS, lambda event: self.tx_press())
        self.tag_bind(tx_text_id, const.BIND_LEFT_PRESS, lambda event: self.tx_press())

        self._restart_schedule()

    def arrow_press(self, right_side: bool) -> None:
        if right_side:
            if self._freq_index < len(MORSE_WORDS) - 1:
                self._freq_index += 1
        else:
            if self._freq_index > 0:
                self._freq_index -= 1
        self.itemconfigure(self._freq_text_id, text=list(MORSE_WORDS.values())[self._freq_index])

    def tx_press(self) -> None:
        self.controller.check_solution(self._freq_index)

    def _restart_schedule(self) -> None:
        for light_state, time in self._flash_schedule:
            self.after(time, self._control_light, light_state)
        self.after(self._flash_schedule[-1][1], self._restart_schedule)

    def _control_light(self, state: bool) -> None:
        self.itemconfigure(self._light_id, fill=(const.COL_YELLOW if state else "light gray"))


class MorseCodeController(BaseModule.ModuleController):
    model_class = MorseCodeModel
    view_class = MorseCodeView

    def __init__(self, bomb_reference, parent_reference: tk.Frame):
        super().__init__(bomb_reference, parent_reference)
        self.view.attach_morse_code(self.model.get_morse_code_data())

    def check_solution(self, index: int) -> None:
        self.model.check_solution(index)
