import pyautogui
import threading
from util.logger import logger

class MouseLocker:
    def __init__(self, app):
        """
        Initialize the MouseLocker.
        :param app: The root application instance.
        """
        self.app = app
        self.is_locked = False
        self.locking_thread = None

    def lock_mouse(self):
        """Enable mouse restriction by continuously monitoring mouse position."""
        if not self.is_locked:
            logger.info("Mouse locking enabled")
            self.is_locked = True
            self._start_locking_thread()

    def unlock_mouse(self):
        """Disable mouse restriction."""
        if self.is_locked:
            logger.info("Mouse locking disabled")
            self.is_locked = False
            if self.locking_thread:
                self.locking_thread.cancel()

    def _start_locking_thread(self):
        """Start a thread that continuously checks and repositions the mouse."""
        if self.is_locked:
            self._reposition_mouse_if_needed()
            self.locking_thread = threading.Timer(0.01, self._start_locking_thread)
            self.locking_thread.start()

    def _reposition_mouse_if_needed(self):
        """Reposition the mouse if it exits the app's bounds during movement."""
        if self._is_mouse_outside_bounds():
            self._reposition_mouse()

    def _is_mouse_outside_bounds(self):
        """
        Check if the mouse is outside the application's bounds.
        :return: True if outside bounds, False otherwise.
        """
        x_min = self.app.winfo_x()
        x_max = x_min + self.app.winfo_width()
        y_min = self.app.winfo_y()
        y_max = y_min + self.app.winfo_height()

        mouse_x, mouse_y = pyautogui.position()
        logger.debug(f"Mouse position: ({mouse_x}, {mouse_y}), App bounds: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}")

        return mouse_x < x_min or mouse_x > x_max or mouse_y < y_min or mouse_y > y_max

    def _reposition_mouse(self):
        """
        Reposition the mouse to the center of the app window.
        """
        center_x = self.app.winfo_x() + self.app.winfo_width() // 2
        center_y = self.app.winfo_y() + self.app.winfo_height() // 2
        pyautogui.moveTo(center_x, center_y)
        logger.debug(f"Mouse repositioned to center: ({center_x}, {center_y})")
