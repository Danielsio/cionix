import customtkinter as ctk
from tkinter import messagebox
from config import db
from util.logger import logger

class PackagesTab(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user

        # Configure dynamic grid layout for centering content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Top spacer
        self.grid_rowconfigure(1, weight=0)  # Content area
        self.grid_rowconfigure(2, weight=1)  # Bottom spacer

        # Content Wrapper
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text="חבילות זמינות",  # Hebrew for "Available Packages"
            font=("Roboto", 24, "bold"),
            text_color="#FFFFFF"
        )
        self.title_label.grid(row=0, column=0, pady=(0, 20))

        # Fetch and display packages
        self.packages = self.fetch_packages()
        if self.packages:
            self.display_packages()
        else:
            self.display_error_message()

    def fetch_packages(self):
        """Fetch packages from the database."""
        try:
            logger.info("Fetching packages from the database...")
            packages = db.child("packages").get(self.user["idToken"]).val()

            if packages:
                logger.info(f"Fetched packages: {packages}")
                return [package for package in packages.values()]
            else:
                logger.warning("No packages found in the database.")
                return []
        except Exception as e:
            logger.error(f"Error fetching packages: {e}")
            return []

    def display_packages(self):
        """Display available packages in a clean, centralized layout."""
        for row_index, package in enumerate(self.packages):
            frame = ctk.CTkFrame(self.content_frame, fg_color="#2C2F33", corner_radius=10)
            frame.grid(row=row_index + 1, column=0, pady=10, padx=20, sticky="ew")

            # Package details
            label = ctk.CTkLabel(
                frame,
                text=f"{package['name']} - {package['minutes']} דקות - ₪{package['price']}",  # Hebrew
                font=("Roboto", 18),
                text_color="#FFFFFF"
            )
            label.pack(side="left", padx=10)

            # Buy Button
            buy_button = ctk.CTkButton(
                frame,
                text="רכוש",  # Hebrew for "Buy"
                command=lambda p=package: self.handle_purchase(p),
                fg_color="#4CAF50",
                hover_color="#45A049",
                font=("Roboto", 16),
                width=100
            )
            buy_button.pack(side="right", padx=10)

        logger.info("Displayed available packages successfully.")

    def display_error_message(self):
        """Display an error message if no packages are found."""
        error_label = ctk.CTkLabel(
            self.content_frame,
            text="אין חבילות זמינות כרגע. נסה שוב מאוחר יותר.",
            font=("Roboto", 16),
            text_color="red"
        )
        error_label.grid(row=1, column=0, pady=20)

    def handle_purchase(self, package):
        """Handle the purchase logic."""
        try:
            logger.info(f"Processing purchase for package: {package['name']}")

            # Add the purchase to the user's purchase history in the database
            purchase_data = {
                "package_name": package["name"],
                "minutes": package["minutes"],
                "price": package["price"],
                "user_id": self.user["localId"]
            }

            db.child("purchases").child(self.user["localId"]).push(purchase_data, self.user["idToken"])
            logger.info(f"User purchased package: {package['name']}")

            # Update user's remaining time
            self.user["remaining_time"] += package["minutes"]

            # Success message
            messagebox.showinfo(
                "רכישה הצליחה",  # Hebrew for "Purchase Successful"
                f"רכשת את {package['name']}! הזמן שנותר שלך כעת הוא {self.user['remaining_time']} דקות."
            )
        except Exception as e:
            logger.error(f"Error during purchase: {e}")
            messagebox.showerror(
                "רכישה נכשלה",  # Hebrew for "Purchase Failed"
                "אירעה שגיאה במהלך עיבוד הרכישה. אנא נסה שוב מאוחר יותר."
            )
