"""Simple Wires Module."""

import tkinter as tk
from typing import List

import BaseModule
import const

import random


class SimpleWiresModel(BaseModule.ModuleModel):
    def __init__(self, controller: "SimpleWiresController"):
        super().__init__(controller)
        self._wires = []
        self.init_wires()
        self._cut_wires = set()  # stores indices of the cut wires
        self._solution = self.solution()

    def init_wires(self) -> None:
        wire_count = random.randint(3, 6)
        for i in range(wire_count):
            self._wires.append(random.choice(
                [const.COL_RED, const.COL_BLACK, const.COL_BLUE, const.COL_YELLOW, const.COL_WHITE])
            )

    def solution(self) -> int:
        """Returns the index of the wire to cut."""
        serial_last_odd = self.get_serial()[-1] in "13579"
        if len(self._wires) == 3:
            if self._wires == [const.COL_BLUE, const.COL_BLUE, const.COL_RED] \
                    or const.COL_RED not in self._wires:
                return 1
            else:
                return 2
        elif len(self._wires) == 4:
            if self._wires.count(const.COL_RED) and serial_last_odd:
                reversed_wires = list(reversed(self._wires))
                return len(self._wires) - reversed_wires.index(const.COL_RED)
            elif self._wires[-1] == const.COL_YELLOW and const.COL_RED not in self._wires:
                return 0
            elif self._wires.count(const.COL_BLUE) == 1:
                return 0
            elif self._wires.count(const.COL_YELLOW) > 1:
                return 3
            else:
                return 1
        elif len(self._wires) == 5:
            if self._wires[-1] == const.COL_BLACK and serial_last_odd:
                return 3
            elif self._wires.count(const.COL_RED) == 1 and self._wires.count(const.COL_YELLOW) > 1:
                return 0
            elif self._wires.count(const.COL_BLACK):
                return 1
            else:
                return 0
        else:
            if self._wires.count(const.COL_YELLOW) == 0 and serial_last_odd:
                return 2
            elif self._wires.count(const.COL_YELLOW) == 1 \
                    and self._wires.count(const.COL_WHITE) > 1:
                return 3
            elif self._wires.count(const.COL_RED) == 0:
                return 5
            else:
                return 3

    def cut_wire(self, index: int) -> None:
        assert index >= 0
        if index in self._cut_wires:
            return None
        self._cut_wires.add(index)
        if index == self._solution:
            self.controller.make_solved()
        else:
            self.controller.add_strike()

    def get_wires(self) -> List[str]:
        return self._wires


class SimpleWiresView(BaseModule.ModuleView):
    TOP_X_OFFSET = 20
    TOP_Y_OFFSET = 10
    WIRE_WIDTH = 90
    WIRE_HEIGHT = 20
    WIRE_GAP = WIRE_HEIGHT + 5

    def __init__(self, bomb_view, controller: "SimpleWiresController"):
        super().__init__(bomb_view, controller)
        self._wires = []
        self._rect_ids = []

    def attach_wire_list(self, wires: List[str]) -> None:
        """Saves a reference to the wires list from `SimpleWiresModel`."""
        self._wires = wires
        self.draw_wires()

    def draw_wires(self) -> None:
        top_x, top_y = self.TOP_X_OFFSET, self.TOP_Y_OFFSET
        for index, wire in enumerate(self._wires):
            top_y += self.WIRE_GAP
            rect_id = self.create_rectangle(
                top_x, top_y, top_x + self.WIRE_WIDTH, top_y + self.WIRE_HEIGHT,
                fill=wire, outline="black"
            )
            self.tag_bind(rect_id, "<ButtonPress-1>",
                          self.on_wire_click)
            self._rect_ids.append(rect_id)

    def on_wire_click(self, event) -> None:
        """Handles clicking a wire."""
        rect_id = self.find_closest(event.x, event.y)[0]
        index = self._rect_ids.index(rect_id)
        self.itemconfigure(rect_id, state=tk.HIDDEN)
        self.controller.cut_wire(index)


class SimpleWiresController(BaseModule.ModuleController):
    model_class = SimpleWiresModel
    view_class = SimpleWiresView

    def __init__(self, bomb_reference, parent_reference: tk.Frame):
        super().__init__(bomb_reference, parent_reference)
        self.view.attach_wire_list(self.model.get_wires())

    def cut_wire(self, wire_index: int) -> None:
        self.model.cut_wire(wire_index)
