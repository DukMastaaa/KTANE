"""Simon Says Module."""

import tkinter as tk

import BaseModule
import const

# Translates which button to press based on vowel / strike count
WITH_VOWEL = {
    0: {
        const.COL_RED:      const.COL_BLUE,
        const.COL_BLUE:     const.COL_RED,
        const.COL_GREEN:    const.COL_YELLOW,
        const.COL_YELLOW:   const.COL_GREEN
    },
    1: {
        const.COL_RED:      const.COL_YELLOW,
        const.COL_BLUE:     const.COL_GREEN,
        const.COL_GREEN:    const.COL_BLUE,
        const.COL_YELLOW:   const.COL_RED
    },
    2: {
        const.COL_RED:      const.COL_GREEN,
        const.COL_BLUE:     const.COL_RED,
        const.COL_GREEN:    const.COL_YELLOW,
        const.COL_YELLOW:   const.COL_BLUE
    }
}
NO_VOWEL = {
    0: {
        const.COL_RED:      const.COL_BLUE,
        const.COL_BLUE:     const.COL_YELLOW,
        const.COL_GREEN:    const.COL_GREEN,
        const.COL_YELLOW:   const.COL_RED
    },
    1: {
        const.COL_RED:      const.COL_RED,
        const.COL_BLUE:     const.COL_BLUE,
        const.COL_GREEN:    const.COL_YELLOW,
        const.COL_YELLOW:   const.COL_GREEN
    },
    2: {
        const.COL_RED:      const.COL_YELLOW,
        const.COL_BLUE:     const.COL_GREEN,
        const.COL_GREEN:    const.COL_BLUE,
        const.COL_YELLOW:   const.COL_RED
    }
}

class SimonSaysModel(BaseModule.ModuleModel):
    def __init__(self, controller: "SimonSaysController"):
        super().__init__(controller)


    # Define more methods, modify __init__


class SimonSaysView(BaseModule.ModuleView):

    def __init__(self, bomb_view, controller: "SimonSaysController"):
        super().__init__(bomb_view, controller)

    # Define more methods, modify __init__


class SimonSaysController(BaseModule.ModuleController):
    model_class = SimonSaysModel
    view_class = SimonSaysView

    def __init__(self, bomb_reference, parent_reference: tk.Frame):
        super().__init__(bomb_reference, parent_reference)

    # Define more methods, modify __init__
