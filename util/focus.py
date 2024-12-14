import tkinter as tk

class FocusEnforcer:
    def __init__(self, app):
        """
        Initialize FocusEnforcer.
        :param app: The root application instance (Tk instance).
        """
        self.app = app
        self.focus_enforced = False

    def enforce_focus(self):
        """Enforce the app window to remain focused and on top."""
        if not self.focus_enforced:
            self.app.lift()  # Bring the app to the front
            self.app.focus_force()  # Force focus to the app
            self.app.attributes('-topmost', True)  # Temporarily set to topmost
            self.app.after(100, lambda: self.app.attributes('-topmost', False))  # Restore normal behavior
            self.focus_enforced = True

    def reverse_focus(self):
        """Reverse focus enforcement and restore normal window behavior."""
        if self.focus_enforced:
            self.app.attributes('-topmost', False)  # Remove the 'topmost' attribute
            self.focus_enforced = False
