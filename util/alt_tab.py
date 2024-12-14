import tkinter as tk

class AltTabBlocker:
    def __init__(self, app):
        """
        Initialize AltTabBlocker.
        :param app: The root application instance (Tk instance).
        """
        self.app = app
        self.alt_tab_disabled = False  # Tracks if the block is active

    def disable_alt_tab(self):
        """Start enforcing focus and topmost behavior to simulate Alt+Tab block."""
        if not self.alt_tab_disabled:
            print("Disabling Alt+Tab...")
            self.alt_tab_disabled = True
            self._enforce_focus_loop()

    def _enforce_focus_loop(self):
        """Continuously enforce focus and 'always on top'."""
        if self.alt_tab_disabled:
            self.app.lift()  # Bring the window to the front
            self.app.focus_force()  # Force focus back to the app
            self.app.attributes('-topmost', True)  # Set always on top
            # Repeat the loop after 100ms
            self.app.after(100, self._enforce_focus_loop)

    def enable_alt_tab(self):
        """Stop enforcing focus and restore normal window behavior."""
        if self.alt_tab_disabled:
            print("Enabling Alt+Tab...")
            self.alt_tab_disabled = False
            self.app.attributes('-topmost', False)  # Remove always on top
