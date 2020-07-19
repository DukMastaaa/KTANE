import Bomb
import const
import tkinter as tk
# todo: possibly a tk.Menu at the top?


class KTANEApp(object):
    def __init__(self, master: tk.Tk):
        self._master = master
        self.mview = Bomb.BombView(self._master)
        self.model = Bomb.BombModel(60*5)
        self.mview.attach_module_list(self.model.modules)
        self.eview = Bomb.EdgeworkView(self._master)

        self.mview.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20)
        self.eview.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)


root = tk.Tk()
app = KTANEApp(root)
root.mainloop()
