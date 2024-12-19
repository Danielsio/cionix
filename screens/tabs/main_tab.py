import customtkinter as ctk
from tkinter import messagebox
from auth import FirebaseAuth
from util.time_utils import format_time
from util.logger import logger
from config import db


class MainTab(ctk.CTkFrame):
    def __init__(self, app, user):
        super().__init__(app)

        self.app = app  # Reference to the root application
        self.user = user
        self.remaining_time = int(user.get("remaining_time", 0))
        self.is_timer_running = False
        self.overlay = None

        logger.info("Initializing MainTab")
        logger.debug(f"App reference: {self.app}")
        logger.debug(f"User data: {self.user}")
        logger.debug(f"User's remaining time: {self.remaining_time}")

        # Configure dynamic grid layout for centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        # Content Wrapper
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Greeting
        self.greeting_label = ctk.CTkLabel(
            self.content_frame,
            text=f"Hello, {user['displayName']}!",
            font=("Roboto", 30, "bold"),
            text_color="#FFFFFF"
        )
        self.greeting_label.grid(row=0, column=0, pady=(0, 20))

        # Remaining Time Label
        self.remaining_time_var = ctk.StringVar(value=f"Remaining Time: {format_time(self.remaining_time)}")
        self.remaining_time_label = ctk.CTkLabel(
            self.content_frame,
            textvariable=self.remaining_time_var,
            font=("Roboto", 22),
            text_color="#A9A9A9" if self.remaining_time == 0 else "#FFFFFF"
        )
        self.remaining_time_label.grid(row=1, column=0, pady=(0, 10))

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.content_frame, width=400, height=15)
        self.progress_bar.set(self.remaining_time / 60 / 60)  # Assuming 1 hour = 1.0
        self.progress_bar.grid(row=2, column=0, pady=(0, 20))

        # Start Button
        self.start_button = ctk.CTkButton(
            self.content_frame,
            text="במחשב שימוש התחל",
            command=self.start_pc_usage,
            state="normal" if self.remaining_time > 0 else "disabled",
            fg_color="#3498DB",
            hover_color="#2980B9",
            text_color="white",
            font=("Roboto", 18),
            width=200,
            height=40
        )
        self.start_button.grid(row=3, column=0, pady=(0, 20))

        # Logout Button
        self.logout_button = ctk.CTkButton(
            self.content_frame,
            text="Logout",
            command=self.logout,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            font=("Roboto", 18),
            text_color="#FFFFFF",
            width=200,
            height=40
        )
        self.logout_button.grid(row=4, column=0, pady=(10, 0))

        # Initialize timers
        self.sync_with_backend()

    def start_pc_usage(self):
        """Start the PC usage session."""
        if self.remaining_time <= 0:
            messagebox.showinfo("No Time Remaining", "You have no remaining time.")
            logger.warning("User tried to start a session with no remaining time.")
            return

        logger.info("Starting PC usage session.")
        self.is_timer_running = True
        self.update_timer()

        # Create an overlay
        logger.info("Creating overlay for remaining time display.")
        self.overlay = ctk.CTkToplevel()
        self.overlay.geometry("300x150+10+10")
        self.overlay.configure(fg_color="#2C2F33")
        self.overlay.overrideredirect(True)
        self.overlay.wm_attributes("-topmost", True)

        time_label = ctk.CTkLabel(
            self.overlay,
            textvariable=self.remaining_time_var,
            font=("Roboto", 18),
            text_color="#FFFFFF"
        )
        time_label.pack(pady=10)

        return_button = ctk.CTkButton(
            self.overlay,
            text="Return to Main",
            command=self.return_to_main,
            fg_color="#3498DB",
            hover_color="#2980B9",
            font=("Roboto", 16),
            text_color="white"
        )
        return_button.pack(pady=10)
        logger.info("Overlay initialized.")

    def return_to_main(self):
        """Return to the main tab and stop the timer."""
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None
            logger.info("Overlay destroyed.")

        self.is_timer_running = False
        logger.info("Returned to the main tab. Timer stopped.")

    def update_timer(self):
        """Update the remaining time every second."""
        if self.is_timer_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_remaining_time_label()
            self.progress_bar.set(self.remaining_time / 60 / 60)

            logger.debug(f"Timer updated: {self.remaining_time} seconds remaining.")
            self.after(1000, self.update_timer)
        elif self.remaining_time <= 0:
            self.remaining_time = 0
            self.is_timer_running = False
            logger.info("User session ended due to time running out.")
            messagebox.showinfo("Time Up", "Your session has ended. Logging out.")
            self.logout()

    def update_remaining_time_label(self):
        """Update the remaining time label."""
        self.remaining_time_var.set(f"Remaining Time: {format_time(self.remaining_time)}")
        self.remaining_time_label.configure(
            text_color="#A9A9A9" if self.remaining_time == 0 else "#FFFFFF"
        )
        logger.debug(f"Remaining time label updated: {self.remaining_time} seconds.")

    def sync_with_backend(self):
        """Sync the remaining time with the backend every 10 seconds."""
        if self.is_timer_running:
            try:
                db.child("users").child(self.user["localId"]).update(
                    {"remaining_time": self.remaining_time},
                    self.user["idToken"]
                )
                logger.info("Remaining time synced with backend.")
            except Exception as e:
                logger.error(f"Error syncing with backend: {e}")

        self.after(10000, self.sync_with_backend)

    def logout(self):
        """Logout the user."""
        self.is_timer_running = False
        try:
            FirebaseAuth.logout(self.user)
            logger.info("User logged out successfully.")
            messagebox.showinfo("Logout", "Your time has been saved. You have been logged out.")
            from screens.login import LoginScreen
            self.app.switch_frame(LoginScreen)
        except Exception as e:
            logger.error(f"Logout failed: {e}")
            messagebox.showerror("Error", f"Failed to log out: {e}")
