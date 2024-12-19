import customtkinter as ctk
from config import db
from util.logger import logger


class HistoryTab(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user

        # Configure grid layout for centering content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Top space
        self.grid_rowconfigure(1, weight=0)  # Content area
        self.grid_rowconfigure(2, weight=1)  # Bottom space

        # Wrapper Frame for Content
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text="Purchase History",
            font=("Roboto", 24, "bold"),
            text_color="#FFFFFF"
        )
        self.title_label.grid(row=0, column=0, pady=(0, 20))

        logger.info(f"Initializing HistoryTab for user: {self.user['displayName']}")

        # Fetch and display purchase history
        self.history = self.fetch_purchase_history()
        if self.history:
            logger.info("Displaying purchase history.")
            self.display_history()
        else:
            self.no_history_label = ctk.CTkLabel(
                self.content_frame,
                text="No purchase history found.",
                font=("Roboto", 16),
                text_color="#A9A9A9"
            )
            self.no_history_label.grid(row=1, column=0, pady=10)

    def fetch_purchase_history(self):
        """Fetch the purchase history from the database."""
        try:
            logger.info("Fetching purchase history from the database.")
            purchases = db.child("purchases").child(self.user["localId"]).get(self.user["idToken"]).val()

            if purchases:
                logger.info(f"Fetched purchase history: {purchases}")
            else:
                logger.warning(f"No purchase history found for user: {self.user['displayName']}")

            return purchases or {}
        except Exception as e:
            logger.error(f"Error fetching purchase history: {e}")
            return {}

    def display_history(self):
        """Display the purchase history in the tab."""
        row_index = 2
        for purchase_id, item in self.history.items():
            frame = ctk.CTkFrame(self.content_frame, fg_color="#2C2F33")
            frame.grid(row=row_index, column=0, pady=10, padx=20, sticky="ew")

            label = ctk.CTkLabel(
                frame,
                text=f"{item['package_name']} - {item['date']} - ${item['price']}",
                font=("Roboto", 16),
                text_color="#FFFFFF"
            )
            label.pack(side="left", padx=10)

            row_index += 1

        logger.info("Purchase history displayed successfully.")
