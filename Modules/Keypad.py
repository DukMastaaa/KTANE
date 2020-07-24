"""Keypad module."""

import tkinter as tk

import BaseModule
import const


class KeypadModel(BaseModule.ModuleModel):
    def __init__(self, controller: "KeypadController"):
        super().__init__(controller)
    # todo: resume here - add symbol constants
    # Define more methods, modify __init__


class KeypadView(BaseModule.ModuleView):

    def __init__(self, bomb_view, controller: "KeypadController"):
        super().__init__(bomb_view, controller)
        self.create_text(10, 10, anchor=tk.NW, text=u"ϘѦӬѼ", font=("TkDefaultFont", 20))

    # Define more methods, modify __init__


class KeypadController(BaseModule.ModuleController):
    model_class = KeypadModel
    view_class = KeypadView

    def __init__(self, bomb_reference, parent_reference: tk.Frame):
        super().__init__(bomb_reference, parent_reference)

    # Define more methods, modify __init__
