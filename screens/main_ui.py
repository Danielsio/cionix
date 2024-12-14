import customtkinter as ctk
from util.time_utils import format_time
from config import db
from tkinter import messagebox
from util.file_explorer import enable_explorer, disable_explorer
from util.logger import logger

class MainUI(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user

        logger.info("Initializing MainUI")
        logger.debug(f"User data: {self.user}")

        # Display the user's full name
        self.full_name_label = ctk.CTkLabel(self, text=f"Welcome, {self.user['full_name']}!", font=("Arial", 18))
        self.full_name_label.pack(pady=10)

        # Initialize local remaining time
        self.remaining_time = int(user.get("remaining_time"))
        self.is_timer_running = True
        self.time_limit_alert_shown = False

        # Title
        self.title_label = ctk.CTkLabel(self, text="PC Usage Manager", font=("Arial", 24))
        self.title_label.pack(pady=20)

        # Remaining Time Label
        self.remaining_time_var = ctk.StringVar(value=f"Remaining Time: {format_time(self.remaining_time)}")
        self.remaining_time_label = ctk.CTkLabel(self, textvariable=self.remaining_time_var, font=("Arial", 18))
        self.remaining_time_label.pack(pady=10)

        # Package Frame
        self.package_frame = ctk.CTkFrame(self)
        self.package_frame.pack(pady=20, fill="both", expand=True)

        # Logout Button
        self.logout_button = ctk.CTkButton(self, text="Logout", command=self.logout, width=150)
        self.logout_button.pack(pady=20)

        # Fetch and display packages
        self.display_packages()

        # Start the timers
        self.update_label_timer()
        self.sync_with_backend()

        # Check user time and manage restrictions
        self.check_user_time()

    def display_packages(self):
        """Fetch and display time packages from the database."""
        try:
            packages = db.child("packages").get().val()
            logger.info(f"Fetched packages: {packages}")
            if not packages:
                ctk.CTkLabel(self.package_frame, text="No packages available.", font=("Arial", 14)).pack(pady=10)
                return

            for package_id, package in packages.items():
                self.create_package_card(package)
        except Exception as e:
            logger.error(f"Failed to fetch packages: {e}")
            messagebox.showerror("Error", f"Failed to load packages: {e}")

    def create_package_card(self, package):
        """Create a visually appealing package card."""
        card = ctk.CTkFrame(self.package_frame, corner_radius=10, border_width=2)
        card.pack(pady=10, padx=10, fill="x")

        # Package details
        name_label = ctk.CTkLabel(card, text=package["name"], font=("Arial", 18))
        name_label.pack(anchor="w", padx=10, pady=5)

        description_label = ctk.CTkLabel(card, text=package["description"], font=("Arial", 14))
        description_label.pack(anchor="w", padx=10, pady=5)

        price_label = ctk.CTkLabel(card, text=f"Price: {package['price']} NIS", font=("Arial", 14))
        price_label.pack(anchor="w", padx=10, pady=5)

        # Purchase Button
        purchase_button = ctk.CTkButton(
            card, text=f"Add {package['minutes']} Minutes",
            command=lambda: self.add_time(package["minutes"] * 60)
        )
        purchase_button.pack(padx=10, pady=10, anchor="e")

    def add_time(self, seconds):
        self.remaining_time += seconds
        if not self.is_timer_running:
            self.is_timer_running = True
            self.update_label_timer()
        self.update_label()
        messagebox.showinfo("Time Added", f"{seconds // 60} minutes added!")
        self.check_user_time()

    def update_label_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_label()
        else:
            self.remaining_time = 0
            self.is_timer_running = False
        self.check_user_time()
        if self.is_timer_running:
            self.after(1000, self.update_label_timer)

    def update_label(self):
        self.remaining_time_var.set(f"Remaining Time: {format_time(self.remaining_time)}")

    def sync_with_backend(self):
        if self.is_timer_running:
            try:
                db.child("users").child(self.user["localId"]).update({"remaining_time": self.remaining_time})
            except Exception as e:
                messagebox.showerror("Sync Error", f"Failed to sync with backend: {e}")
            self.after(10000, self.sync_with_backend)

    def logout(self):
        self.is_timer_running = False
        try:
            db.child("users").child(self.user["localId"]).update({
                "remaining_time": self.remaining_time,
                "is_logged_in": False
            })
            messagebox.showinfo("Logout", "Your time has been saved. You have been logged out.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sync remaining time during logout: {e}")
        self.master.restriction_manager.stop_restrictions()  # Ensure restrictions are cleared on logout
        from screens.login import LoginScreen
        self.master.switch_frame(LoginScreen)

    def check_user_time(self):
        if self.remaining_time > 0:
            enable_explorer()
            self.master.restriction_manager.stop_restrictions()
            self.time_limit_alert_shown = False
        else:
            disable_explorer()
            self.master.restriction_manager.start_restrictions()
            if not self.time_limit_alert_shown:
                messagebox.showinfo("Time Limit", "You have insufficient remaining time to continue using the PC.")
                self.time_limit_alert_shown = True
