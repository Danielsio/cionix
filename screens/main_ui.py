import customtkinter as ctk
from screens.tabs.main_tab import MainTab
from screens.tabs.packages import PackagesTab
from screens.tabs.history import HistoryTab
from screens.tabs.help import HelpTab
from util.logger import logger


class MainUI(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)
        logger.info("Initializing MainUI")

        self.master = master  # This is the `App` reference
        self.user = user

        # Create tabview
        self.tabview = ctk.CTkTabview(self, width=800, height=600)
        self.tabview.pack(fill="both", expand=True)
        logger.info("Tabview created")

        # Add tabs to the tabview

        help_frame = self.tabview.add("עזרה")
        logger.info("Help tab added")
        history_frame = self.tabview.add("היסטוריה")
        logger.info("History tab added")
        packages_frame = self.tabview.add("חבילות")
        logger.info("Packages tab added")
        main_frame = self.tabview.add("ראשי")
        logger.info("Main tab added")

        self.tabview.set("ראשי")

        # Populate tabs with their respective frames
        self.main_tab = MainTab(self.master, self.user)  # Pass App reference and user data
        logger.info("MainTab initialized")
        self.packages_tab = PackagesTab(self.master, self.user)  # Pass App reference and user data
        logger.info("PackagesTab initialized")
        self.history_tab = HistoryTab(self.master, self.user)  # Pass App reference and user data
        logger.info("HistoryTab initialized")
        self.help_tab = HelpTab(self.master, self.user)  # Pass App reference and user data
        logger.info("HelpTab initialized")

        # Add the content frames to their respective tabs
        self.main_tab.pack(fill="both", expand=True, in_=main_frame)
        self.packages_tab.pack(fill="both", expand=True, in_=packages_frame)
        self.history_tab.pack(fill="both", expand=True, in_=history_frame)
        self.help_tab.pack(fill="both", expand=True, in_=help_frame)

        logger.info("All tabs populated and ready")
