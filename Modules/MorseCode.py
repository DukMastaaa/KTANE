"""Morse Code Module."""

import tkinter as tk
from random import random

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
        self._word = random.choice(MORSE_WORDS)
        self._morse = MorseCodeTranslator.encode(self._word)

    def get_morse_code_data(self) -> str:
        return self._morse

    def calc_solution(self) -> None:
        self._solution = MORSE_WORDS[self._word]


class MorseCodeView(BaseModule.ModuleView):
    DIT_DURATION = 200
    DAH_MULTIPLIER = 3
    CHAR_END_MULTIPLIER = 3
    WORD_END_MULTIPLIER = 7

    def __init__(self, bomb_view, controller: "MorseCodeController"):
        super().__init__(bomb_view, controller)
        self._morse = ""
        self._flash_schedule = []

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
        for char in chars:  # todo: timings below are wrong
            if char == ".":
                time_counter += self.DIT_DURATION
                self._flash_schedule.append((True, time_counter))
            elif char == "-":
                time_counter += self.DIT_DURATION * self.DAH_MULTIPLIER
                self._flash_schedule.append((True, time_counter))


    def draw_morse_code(self) -> None:
        pass

    # Define more methods, modify __init__


class MorseCodeController(BaseModule.ModuleController):
    model_class = MorseCodeModel
    view_class = MorseCodeView

    def __init__(self, bomb_reference, parent_reference: tk.Frame):
        super().__init__(bomb_reference, parent_reference)
        self.view.attach_morse_code(self.model.get_morse_code_data())

    # Define more methods, modify __init__
