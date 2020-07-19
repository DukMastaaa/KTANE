from typing import Optional, Callable, List
from threading import Timer
from datetime import timedelta

import BaseModule
import const
import random
import tkinter as tk


class CountdownTimer(object):
    def __init__(self, initial_time: float, countdown_speed: float, finished_callback: Callable):
        self._current_time = initial_time
        self._countdown_speed = countdown_speed
        self._finished_callback = finished_callback
        self._is_timing = False

    @staticmethod
    def format_time(seconds: float) -> str:
        """(str) Returns a string with the time in seconds formatted."""
        return str(timedelta(seconds=seconds))[2:10] if seconds != 0.0 else "00:00.00"

    def is_timing(self) -> bool:
        return self._is_timing

    def start_timing(self) -> None:
        self._is_timing = True
        self.while_timing()

    def stop_timing(self) -> None:
        self._is_timing = False
        self._finished_callback(self._current_time)

    def while_timing(self) -> None:
        if self._is_timing:
            self._current_time -= const.TIME_STEP / self._countdown_speed
            if self._current_time <= 0:
                self._current_time = 0
                self.stop_timing()
            else:
                schedule = Timer(const.TIME_STEP, self.while_timing)
                schedule.start()

    def get_time(self) -> float:
        return self._current_time

    def set_time(self, seconds: float) -> None:
        assert seconds >= 0
        self._current_time = seconds

    def set_countdown_speed(self, countdown_speed: float) -> None:
        assert 0.5 < countdown_speed
        self._countdown_speed = countdown_speed


class BombModel(object):
    def __init__(self, initial_time: float = 60*5):
        self._strikes = 0
        self._timer = CountdownTimer(initial_time, const.STRIKE_TO_COUNTDOWN_SPEED[0],
                                     self.game_end)
        self.indicators = []
        self.batteries = []
        self.ports = []
        self.serial = ""
        self.init_edgework()

        self.modules = []
        self.init_modules()

    def init_edgework(self) -> None:
        # Indicators
        ind_count = random.randint(0, 3)
        for i in range(ind_count):
            ind_name = random.choice(const.INDICATORS)
            ind_light = random.choice([const.IND_ON, const.IND_OFF])
            self.indicators.append((ind_name, ind_light))

        # Batteries
        bat_count = random.randint(0, 2)
        for i in range(bat_count):
            self.batteries.append(random.choice(const.BATTERIES))

        # Ports
        port_count = random.randint(0, 2)
        for i in range(port_count):
            self.ports.append(random.choice(const.PORTS))

        # Serial
        for i in range(5):
            self.serial += random.choice(const.ALPHA) if random.randint(0, 1) \
                else random.choice(const.NUMER)
        self.serial += random.choice(const.NUMER)
        # todo: surely optimise. this looks really cramped

    def init_modules(self) -> None:
        # todo: assert len(modules) <= MODULES_WIDTH * MODULES_HEIGHT
        pass  # todo: somehow load modules into self.modules list

    def game_end(self, seconds_left: float) -> None:
        if self._strikes >= const.STRIKE_LIMIT or seconds_left <= 0:
            self._game_lose()
        else:
            self._game_win()

    def _game_lose(self) -> None:
        print("You lost the game")

    def _game_win(self) -> None:
        print("You won the game")

    def add_strike(self) -> None:
        self._strikes += 1
        if self._strikes >= const.STRIKE_LIMIT:
            self._timer.stop_timing()
        else:
            self._timer.set_countdown_speed(const.STRIKE_TO_COUNTDOWN_SPEED[self._strikes])

    def get_time(self) -> float:
        return self._timer.get_time()

    def get_f_time(self) -> str:
        return self._timer.format_time(self._timer.get_time())

    def start_game(self) -> None:
        self._timer.start_timing()


class BombView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._master = master
        self.modules = []

    # def attach_module_list(self, modules: List[BaseModule.ModuleController]) -> None:
    # Removing type because of circular import
    def attach_module_list(self, modules: List[BaseModule.ModuleController]) -> None:
        """Stores the reference to the BombModel's module list."""
        self.modules = modules
        for index, controller in enumerate(self.modules):
            self.grid(row=(index // const.VIEW_MODULES_WIDTH),
                      column=(index % const.VIEW_MODULES_WIDTH))
            # todo: see how this deals with empty spots in the grid.


class EdgeworkView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._master = master
        # todo: countdown timer display (get reference to BombModel CountdownTimer)
        # todo: BombModel updates state => EdgeworkView notified, updates view by querying BombModel
