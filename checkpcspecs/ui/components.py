"""Reusable UI components."""

import tkinter as tk
from enum import Enum
from typing import Optional


class ResultColor(str, Enum):
    """Colors for result display."""
    GOOD = "green"
    WARNING = "DarkOrange3"
    ERROR = "red"
    NEUTRAL = "black"


class StatusLabel(tk.Label):
    """Label for displaying test status with color coding."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def set_good(self, text: str):
        """Set text with good status color."""
        self.config(text=text, fg=ResultColor.GOOD)

    def set_warning(self, text: str):
        """Set text with warning status color."""
        self.config(text=text, fg=ResultColor.WARNING)

    def set_error(self, text: str):
        """Set text with error status color."""
        self.config(text=text, fg=ResultColor.ERROR)

    def set_neutral(self, text: str):
        """Set text with neutral status color."""
        self.config(text=text, fg=ResultColor.NEUTRAL)


class ResultDisplay:
    """Handles displaying test results in a grid layout."""

    def __init__(self, parent: tk.Widget, start_row: int = 7):
        self.parent = parent
        self.current_row = start_row
        self.labels: dict[str, tuple[tk.Label, StatusLabel]] = {}

    def add_result(self, 
                   label_text: str, 
                   result_text: str, 
                   color: ResultColor = ResultColor.NEUTRAL) -> StatusLabel:
        """Add a result row with label and status.
        
        Args:
            label_text: Text for the label
            result_text: Text for the result
            color: Color for the result
            
        Returns:
            StatusLabel that can be updated later
        """
        label = tk.Label(self.parent, text=label_text)
        label.grid(column=1, row=self.current_row, sticky="e")

        result = StatusLabel(self.parent, text=result_text, fg=color)
        result.grid(column=2, row=self.current_row, sticky="w")

        self.labels[label_text] = (label, result)
        self.current_row += 1

        return result

    def update_result(self, label_text: str, result_text: str, color: ResultColor):
        """Update existing result.
        
        Args:
            label_text: Label text to find the result
            result_text: New result text
            color: New color
        """
        if label_text in self.labels:
            _, result_label = self.labels[label_text]
            result_label.config(text=result_text, fg=color)

    def get_current_row(self) -> int:
        """Get current row number for additional elements."""
        return self.current_row
