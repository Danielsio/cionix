class FocusEnforcer:
    def __init__(self, app):
        """
        Initialize FocusEnforcer.
        :param app: The root application instance (Tk instance).
        """
        self.app = app
        self.focus_enforced = False

    def enforce_focus(self):
        """Enforce focus by bringing the app to the front."""
        if not self.focus_enforced:
            print("Bringing app to the front...")
            self.focus_enforced = True
            self.app.lift()  # Bring the window to the front
            self.app.attributes('-topmost', True)  # Temporarily set "always on top"
            self.app.after(50, lambda: self.app.attributes('-topmost', False))  # Reset "topmost"

    def reverse_focus(self):
        """Reset focus enforcement (no further action needed for one-time focus)."""
        if self.focus_enforced:
            print("Focus enforcement reversed.")
            self.focus_enforced = False
