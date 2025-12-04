"""Main application window."""

import asyncio
import tkinter as tk
from datetime import datetime
from tkinter import Button, Entry
from typing import Optional, Callable

from PIL import ImageTk, Image
import nest_asyncio

from ..utils import ResourceManager
from .components import ResultDisplay, ResultColor

nest_asyncio.apply()


class MainWindow:
    """Main application window for PC specs checking."""

    WINDOW_WIDTH = 480
    WINDOW_HEIGHT = 400
    WINDOW_TITLE = "Проверка ПК на соответствие требованиям"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(self.WINDOW_TITLE)
        self._setup_window()
        self._setup_resources()
        self._setup_header()
        self.result_display = ResultDisplay(self.root, start_row=7)
        self.on_start_callback: Optional[Callable] = None

    def _setup_window(self):
        """Configure window size and position."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - self.WINDOW_WIDTH) // 2
        y = (screen_height - self.WINDOW_HEIGHT) // 2
        
        self.root.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}')
        self.root.resizable(False, False)

    def _setup_resources(self):
        """Load application resources (icon, logo)."""
        # Set icon
        icon_path = ResourceManager.get_icon_path()
        if icon_path:
            self.root.iconbitmap(default=str(icon_path))

        # Load logo
        logo_path = ResourceManager.get_logo_path()
        if logo_path:
            try:
                self.logo_image = ImageTk.PhotoImage(Image.open(logo_path))
            except Exception:
                self.logo_image = None
        else:
            self.logo_image = None

    def _setup_header(self):
        """Setup header with logo and spacing."""
        if self.logo_image:
            logo_label = tk.Label(self.root, image=self.logo_image)
            logo_label.place(x=10, y=0)

        # Spacing labels
        for i in range(5):
            tk.Label(self.root, text="").grid(column=0, row=i)

        # Date/Time
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tk.Label(self.root, text="Дата/Время:").grid(column=1, row=5, sticky="e")
        tk.Label(self.root, text=dt_string).grid(column=2, row=5, sticky="w")

    def setup_name_input(self, on_start: Callable[[str], None]):
        """Setup name input field and start button.
        
        Args:
            on_start: Callback function to call when user starts the test
        """
        self.on_start_callback = on_start

        # Name label and entry
        self.name_label = tk.Label(self.root, text="Введите ФИО:")
        self.name_label.grid(column=1, row=6, sticky="e")

        self.name_entry = Entry(self.root, width=37)
        self.name_entry.grid(column=2, row=6, sticky="w")

        self.start_button = Button(self.root, text='Сохранить', command=self._on_start_clicked)
        self.start_button.grid(column=3, row=6, sticky="e")

    def _on_start_clicked(self):
        """Handle start button click."""
        username = self.name_entry.get().strip()
        if not username:
            return

        # Update UI
        self.name_label.config(text="ФИО:")
        self.name_entry.config(state="readonly")
        self.start_button.destroy()

        # Call callback
        if self.on_start_callback:
            self.on_start_callback(username)

    def add_quit_button(self):
        """Add quit button at the bottom."""
        quit_button = Button(self.root, text="Закрыть", command=self.root.quit)
        quit_button.place(x=200, y=370)

    async def run_async_task(self, coro):
        """Run async task with UI update loop.
        
        Args:
            coro: Async coroutine to run
        """
        task = asyncio.create_task(coro)
        
        while not task.done():
            self.root.update()
            await asyncio.sleep(0.01)
        
        return await task

    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
