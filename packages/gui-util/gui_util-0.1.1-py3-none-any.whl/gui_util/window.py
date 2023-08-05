from Xlib.xobject.drawable import Window
from dataclasses import dataclass


@dataclass
class Window:

    xlib_win: Window

    def __repr__(self):
        return f'Window(name={self.name})'

    @property
    def name(self):
        return self.xlib_win.get_wm_name()

    @classmethod
    def from_xlib_window(cls, xlib_win):
        window = Window(xlib_win=xlib_win)
        return window


