"""Template for making modules."""

import tkinter as tk

import BaseModule
import const


class ExampleModel(BaseModule.ModuleModel):
    def __init__(self, controller: "ExampleController"):
        super().__init__(controller)

    # Define more methods, modify __init__


class ExampleView(BaseModule.ModuleView):

    def __init__(self, bomb_view, controller: "ExampleController"):
        super().__init__(bomb_view, controller)

    # Define more methods, modify __init__


class ExampleController(BaseModule.ModuleController):
    model_class = ExampleModel
    view_class = ExampleView

    def __init__(self, bomb_reference, parent_reference: tk.Frame):
        super().__init__(bomb_reference, parent_reference)

    # Define more methods, modify __init__
