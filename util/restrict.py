from util.file_explorer import disable_explorer, enable_explorer
from util.alt_tab import AltTabBlocker
from util.logger import logger
from util.focus import FocusEnforcer

class RestrictionManager:
    def __init__(self, app):
        """
        Initialize the Restriction Manager.
        :param app: The root application instance (Tk instance).
        """
        self.app = app
        self.alt_tab_blocker = AltTabBlocker(app)
        self.focus_enforcer = FocusEnforcer(app)  # Create an instance of FocusEnforcer
        self.restrictions_active = False

    def start_restrictions(self):
        """Start all restrictions: disable File Explorer, lock the mouse, and disable Alt+Tab."""
        if not self.restrictions_active:
            logger.info("Starting restrictions")
            disable_explorer()
            self.alt_tab_blocker.disable_alt_tab()
            # self.focus_enforcer.enforce_focus()
            self.restrictions_active = True
            logger.debug("File Explorer disabled, mouse locked, and Alt+Tab disabled")

    def stop_restrictions(self):
        """Stop all restrictions: enable File Explorer, unlock the mouse, and enable Alt+Tab."""
        if self.restrictions_active:
            logger.info("Stopping restrictions")
            enable_explorer()
            self.alt_tab_blocker.enable_alt_tab()
            # self.focus_enforcer.reverse_focus()
            self.restrictions_active = False
            logger.debug("File Explorer enabled, mouse unlocked, and Alt+Tab enabled")
