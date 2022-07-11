"""Main window."""
import tkinter as tk
from tkinter import ttk


class App(tk.Tk):

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.title("{{ cookiecutter.project_name }}")
        self.initialize()

    def initialize(self) -> None:
        """Initialize the widgets."""
