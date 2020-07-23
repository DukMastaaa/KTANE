from typing import Optional, Callable, List
from threading import Timer
from datetime import timedelta

import const
import random
import tkinter as tk
from tkinter import messagebox


class CountdownTimer(object):
    def __init__(self, initial_time: float, countdown_speed: float, finished_callback: Callable):
        self._current_time = initial_time
        self._countdown_speed = countdown_speed
        self._finished_callback = finished_callback
        self._is_timing = False

    @staticmethod
    def format_time(seconds: float) -> str:
        """(str) Returns a string with the time in seconds formatted."""
        # return str(timedelta(seconds=seconds))[2:10] if seconds != 0.0 else "00:00.00"
        if seconds == 0.0:
            return "00.00"
        elif seconds < 60.0:
            return str(timedelta(seconds=seconds))[5:10]  # SS:DD, d decimal
        else:
            return str(timedelta(seconds=seconds))[2:7]   # MM:SS

    def is_timing(self) -> bool:
        return self._is_timing

    def start_timing(self) -> None:
        self._is_timing = True
        self.while_timing()

    def stop_timing(self) -> None:
        self._is_timing = False
        self._finished_callback(self._current_time)

    def stop_timing_no_callback(self) -> None:
        """Used for window close events."""
        self._is_timing = False

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
    def __init__(self, initial_time: float, window_close_callback: Callable):
        self._window_close_callback = window_close_callback
        self._strikes = 0
        self.timer = CountdownTimer(initial_time, const.STRIKE_TO_COUNTDOWN_SPEED[0],
                                    self.game_end)
        self.indicators = []
        self.batteries = []
        self.ports = []
        self.serial = ""
        self.init_edgework()

        self._edgework_view = None

        self.modules = []

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
        # todo: surely optimise. this looks really cramped and repetitive

    def attach_modules(self, modules: list) -> None:
        self.modules = modules
        assert len(modules) <= const.VIEW_MODULES_WIDTH * const.VIEW_MODULES_HEIGHT

    def attach_edgework_view(self, view: "EdgeworkView") -> None:
        """Saves a reference to the program's `EdgeworkView` object."""
        self._edgework_view = view

    def game_end(self, seconds_left: float) -> None:
        if self._strikes >= const.STRIKE_LIMIT or seconds_left <= 0:
            self._game_lose()
        else:
            self._game_win()

    def _game_lose(self) -> None:
        messagebox.showinfo(title="You lost!", message="You lost!")
        # self._window_close_callback()  # todo: this doesn't work for some threading reason

    def _game_win(self) -> None:
        messagebox.showinfo(title="You won!", message="You won!")
        # self._window_close_callback()

    def add_strike(self) -> None:
        if self._strikes < const.STRIKE_LIMIT:
            self._strikes += 1
            self._edgework_view.update_strikes(self._strikes)
            if self._strikes >= const.STRIKE_LIMIT:
                self.timer.stop_timing()
            else:
                self.timer.set_countdown_speed(const.STRIKE_TO_COUNTDOWN_SPEED[self._strikes])

    def get_time(self) -> float:
        return self.timer.get_time()

    def get_f_time(self) -> str:
        """Gets the current time formatted as MM:SS.dd (d decimal)"""
        return self.timer.format_time(self.timer.get_time())

    def start_game(self) -> None:
        """Starts the game and timer."""
        self.check_edgework_view_attached()
        self.timer.start_timing()
        self._edgework_view.start_timing()

    def check_edgework_view_attached(self) -> None:
        """Checks whether an edgework view has been attached. Quits otherwise."""
        if not isinstance(self._edgework_view, EdgeworkView):
            raise TypeError("Edgework view not attached to bomb model.")


class BombView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(width=const.VIEW_MODULES_PX_WIDTH, height=const.VIEW_MODULES_PX_HEIGHT)
        self._master = master
        self.modules = []

    # def attach_module_list(self, modules: List[BaseModule.ModuleController]) -> None:
    # Removing type because of circular import
    def attach_module_list(self, modules) -> None:
        """Stores the reference to the BombModel's module list."""
        self.modules = modules
        self.draw_modules()

    def draw_modules(self) -> None:
        for index, controller in enumerate(self.modules):
            controller.view.grid(row=(index // const.VIEW_MODULES_WIDTH),
                                 column=(index % const.VIEW_MODULES_WIDTH))


class IndicatorLabel(tk.Label):
    def __init__(self, parent, text: str, on: bool):
        label_text = text + (const.LIT_CIRCLE if on else const.UNLIT_CIRCLE)
        super().__init__(parent, text=label_text, bg=const.INDICATOR_BG, fg=const.INDICATOR_FG,
                         font=const.INDICATOR_FONT)


class BatteryLabel(tk.Label):
    def __init__(self, parent, battery_type: str):
        # todo: implement images instead of text
        super().__init__(parent, text=battery_type, bg="dim gray", fg="white",
                         font=const.INDICATOR_FONT)


class PortLabel(tk.Label):
    def __init__(self, parent, port_type: str):
        # todo: implement images instead of text
        super().__init__(parent, text=port_type, bg="dim gray", fg="white",
                         font=const.INDICATOR_FONT)


class EdgeworkView(tk.Frame):
    def __init__(self, master, bomb_model: BombModel):
        super().__init__(master)
        self._master = master
        self._bomb_model = bomb_model

        self._timer_label = tk.Label(self, text="00:00.00", font=const.EVIEW_FONT_TIMER_STRIKES)
        self._timer_label.pack(side=tk.TOP, anchor=tk.CENTER, fill=tk.X)
        self._strike_label = tk.Label(self, text="-", font=const.EVIEW_FONT_TIMER_STRIKES, fg="red")
        self._strike_label.pack(side=tk.TOP, anchor=tk.CENTER, fill=tk.X)

        self._indicator_frame = tk.Frame(self)
        for ind_name, status in self._bomb_model.indicators:
            indicator = IndicatorLabel(self._indicator_frame, ind_name, status)
            indicator.pack(side=tk.TOP, anchor=tk.CENTER)
        self._indicator_frame.pack(side=tk.TOP, anchor=tk.N, fill=tk.X,
                                   pady=10 if self._bomb_model.indicators else 0)

        self._battery_frame = tk.Frame(self)
        for battery_type in self._bomb_model.batteries:
            battery = BatteryLabel(self._battery_frame, battery_type)
            battery.pack(side=tk.TOP, anchor=tk.CENTER)
        self._battery_frame.pack(side=tk.TOP, anchor=tk.N, fill=tk.X,
                                 pady=10 if self._bomb_model.batteries else 0)

        self._port_frame = tk.Frame(self)
        for port_type in self._bomb_model.ports:
            port = PortLabel(self._port_frame, port_type)
            port.pack(side=tk.TOP, anchor=tk.CENTER)
        self._port_frame.pack(side=tk.TOP, anchor=tk.N, fill=tk.X,
                              pady=10 if self._bomb_model.ports else 0)

        self._serial_label = tk.Label(self, text=self._bomb_model.serial,
                                      font=const.SERIAL_FONT, bg=const.SERIAL_BG,
                                      fg=const.SERIAL_FG)
        self._serial_label.pack(side=tk.TOP, anchor=tk.CENTER, fill=tk.X,
                                pady=10)

        # todo: do images and reduce duplication omg ew

    def start_timing(self) -> None:
        # todo: ok what, am i really polling the timer every 0.1s
        # yes i am, this is disgusting. but can't see a better way
        # can't sync with the CountdownTimer since it uses threading.Timer not tk.after
        self._timer_label.config(text=self._bomb_model.get_f_time())
        self.after(int(const.TIME_STEP * 1000), self.start_timing)

    def update_strikes(self, strikes: int) -> None:
        """Updates the amount of strikes shown on EdgeworkView."""
        strike_str = "-" if strikes == 0 else "X" * strikes
        self._strike_label.config(text=strike_str)
