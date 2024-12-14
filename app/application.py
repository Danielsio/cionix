import customtkinter as ctk
from screens.login import LoginScreen
from util.task_manager import disable_task_manager, enable_task_manager
from util.restrict import RestrictionManager
import atexit
from util.logger import logger


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        logger.info("Initializing App")

        # Set window title
        self.title("PC Usage Manager")

        # Full-screen mode
        self.attributes("-fullscreen", True)
        self.overrideredirect(True)  # Hide window decorations
        logger.info("Full-screen mode enabled")

        # Disable Task Manager for the app lifecycle
        try:
            disable_task_manager()
            logger.info("Task Manager disabled successfully")
        except Exception as e:
            logger.error(f"Failed to disable Task Manager: {e}")

        # Initialize Restriction Manager
        self.restriction_manager = RestrictionManager(self)

        # Ensure Task Manager is re-enabled and restrictions are cleared on app exit
        atexit.register(self.cleanup_and_exit)

        # Disable the close button and Alt + F4
        self.protocol("WM_DELETE_WINDOW", self.disable_close_action)

        # Bind secret sequence (Ctrl+Shift+Q)
        self.bind_all("<Control-Shift-Key-Q>", self.secret_exit)

        self.current_frame = None
        self.switch_frame(LoginScreen)

    def disable_close_action(self):
        """Disable all close actions (close button, Alt + F4, etc.)."""
        logger.warning("Close action attempted but blocked")

    def secret_exit(self, event=None):
        """Triggered by the secret key sequence to exit the app."""
        self.cleanup_and_exit()

    def cleanup_and_exit(self, *args):
        """Re-enable Task Manager, stop restrictions, and exit the application."""
        try:
            enable_task_manager()  # Always re-enable Task Manager
            logger.info("Task Manager re-enabled successfully")
        except Exception as e:
            logger.error(f"Failed to re-enable Task Manager: {e}")

        # Stop all active restrictions
        self.restriction_manager.stop_restrictions()
        logger.info("All restrictions stopped")

        self.destroy()  # Safely close the app

    def switch_frame(self, frame_class, *args):
        """Switches to a new frame."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)

        # The frame itself decides whether to start or stop restrictions
        logger.info(f"Switched to {frame_class.__name__}")
