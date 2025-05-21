import tkinter as tk
from gui.app_gui import WeatherApp

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()