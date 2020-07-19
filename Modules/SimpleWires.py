import BaseModule
import Bomb
import const

import random


class SimpleWiresModel(BaseModule.ModuleModel):
    def __init__(self, bomb: Bomb):
        super().__init__(bomb)
        self._wires = []
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


class SimpleWiresView(BaseModule.ModuleView):
    def __init__(self, ):
        super().__init__()


class SimpleWiresController(BaseModule.ModuleController):
    model_class = SimpleWiresModel
    view_class = SimpleWiresView

    def __init__(self, bomb_reference):
        super().__init__()  # todo: uhhh
        # add bindings to rectangles in view class
