import Bomb
import ModuleManager
import const
import tkinter as tk
# todo: possibly a tk.Menu at the top?


class KTANEApp(object):
    def __init__(self, master: tk.Tk):
        self._master = master
        self._master.geometry(const.APP_GEOMETRY)
        self.mview = Bomb.BombView(self._master)
        self.model = Bomb.BombModel(const.DEFAULT_TIME_LIMIT, self.on_window_close)
        self.model.attach_modules(ModuleManager.get_module_list(self.model, self.mview))
        self.mview.attach_module_list(self.model.modules)
        self.eview = Bomb.EdgeworkView(self._master, self.model)
        self.model.attach_edgework_view(self.eview)

        self.mview.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20)
        self.eview.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        self.model.start_game()

    def on_window_close(self) -> None:
        """Stops the timer thread when the window is closed so python process can quit."""
        self.model.timer.stop_timing_no_callback()
        self._master.destroy()
        quit()


root = tk.Tk()
app = KTANEApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_window_close)
root.mainloop()
