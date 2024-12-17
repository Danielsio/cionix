import tkinter as tk

class AltTabBlocker:
    def __init__(self, app):
        """
        Initialize AltTabBlocker.
        :param app: The root application instance (Tk instance).
        """
        self.app = app
        self.alt_tab_disabled = False  # Tracks if Alt+Tab block is active

    def disable_alt_tab(self):
        """Start enforcing 'always on top' behavior to simulate Alt+Tab block."""
        if not self.alt_tab_disabled:
            print("Disabling Alt+Tab...")
            self.alt_tab_disabled = True
            self._enforce_always_on_top()

    def _enforce_always_on_top(self):
        """Keep the app window always on top without stealing widget focus."""
        if self.alt_tab_disabled:
            self.app.attributes('-topmost', True)  # Set "always on top"
            self.app.after(100, self._enforce_always_on_top)  # Repeat every 100ms

    def enable_alt_tab(self):
        """Stop 'always on top' enforcement."""
        if self.alt_tab_disabled:
            print("Enabling Alt+Tab...")
            self.alt_tab_disabled = False
            self.app.attributes('-topmost', False)  # Remove "always on top"
