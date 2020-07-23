"""The Button Module."""

import tkinter as tk

import BaseModule
import const


class TheButtonModel(BaseModule.ModuleModel):
    def __init__(self, controller: "TheButtonController"):
        super().__init__(controller)

    # Define more methods, modify __init__


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
