import customtkinter as ctk
from tkinter import messagebox
from auth import FirebaseAuth
from util.time_utils import format_time, format_time_dd_hh_mm_ss
from util.logger import logger
from config import db

class MainTab(ctk.CTkFrame):
    def __init__(self, app, user):
        super().__init__(app)

        self.time_label = None
        self.return_button = None
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
            text=f"שלום, {user['displayName']}!",
            font=("Roboto", 30, "bold"),
            text_color="#FFFFFF"
        )
        self.greeting_label.grid(row=0, column=0, pady=(0, 20))

        # Remaining Time Label
        self.remaining_time_var = ctk.StringVar(value=f"{format_time(self.remaining_time)} :שנותר זמן")  # Hebrew
        self.remaining_time_label = ctk.CTkLabel(
            self.content_frame,
            textvariable=self.remaining_time_var,
            font=("Roboto", 22),
            text_color="#A9A9A9" if self.remaining_time == 0 else "#FFFFFF"
        )
        self.remaining_time_label.grid(row=1, column=0, pady=(0, 10))

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
            text="התנתקות",
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
            messagebox.showinfo("הזמן נגמר", "אין לך זמן שימוש במחשב.")
            logger.warning("User tried to start a session with no remaining time.")
            return

        if self.is_timer_running:
            logger.warning("Timer is already running; start button should be disabled.")
            return

        logger.info("Starting PC usage session.")
        self.is_timer_running = True
        self.update_timer()

        # Disable Start Button
        self.start_button.configure(state="disabled")

        # Minimize the application and stop restrictions
        self.app.toggle_pc_access(True)

        # Create a smaller overlay
        logger.info("Creating overlay for remaining time display.")
        self.overlay = ctk.CTkToplevel()
        self.overlay.geometry("150x50+10+10")  # Smaller overlay
        self.overlay.configure(fg_color="#2C2F33")
        self.overlay.overrideredirect(True)
        self.overlay.wm_attributes("-topmost", True)

        # Time label in dd:hh:mm:ss format
        self.time_label = ctk.CTkLabel(
            self.overlay,
            text=format_time_dd_hh_mm_ss(self.remaining_time),
            font=("Roboto", 16),
            text_color="#FFFFFF"
        )
        self.time_label.pack(fill="both", expand=True)

        # Bind hover events to dynamically create/destroy the return button
        self.overlay.bind("<Enter>", self.create_return_button)
        self.overlay.bind("<Leave>", self.destroy_return_button)

        logger.info("Overlay initialized.")

    def create_return_button(self, event=None):
        """Dynamically create the return button."""
        if not hasattr(self, "return_button") or self.return_button is None:
            self.return_button = ctk.CTkButton(
                self.overlay,
                text="חזרה",
                command=self.return_to_main,
                fg_color="#3498DB",
                hover_color="#2980B9",
                font=("Roboto", 12),
                text_color="white",
                width=80,
                height=30
            )
            self.return_button.pack(pady=(5, 0))
            self.is_hovering = True  # Set flag to prevent flickering
            logger.info("Return button created.")

    def destroy_return_button(self, event=None):
        """Dynamically destroy the return button."""
        # Check if the pointer is still inside the overlay before destroying
        x, y, width, height = (self.overlay.winfo_rootx(), self.overlay.winfo_rooty(),
                               self.overlay.winfo_width(), self.overlay.winfo_height())
        if not (x <= self.overlay.winfo_pointerx() <= x + width and
                y <= self.overlay.winfo_pointery() <= y + height):
            if hasattr(self, "return_button") and self.return_button:
                self.return_button.destroy()
                self.return_button = None
                logger.info("Return button destroyed.")

    def return_to_main(self):
        """Return to the main tab and stop the timer."""
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None
            logger.info("Overlay destroyed.")

        # Restore the application and enable restrictions
        self.app.toggle_pc_access(False)

        # Stop the timer
        self.is_timer_running = False

        # Re-enable Start Button
        self.start_button.configure(state="normal")

        logger.info("Returned to the main tab. Timer stopped.")

    def update_timer(self):
        """Update the remaining time every second."""
        if self.is_timer_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_remaining_time_label()

            # Update the overlay time label
            if self.overlay and self.time_label:
                self.time_label.configure(text=format_time_dd_hh_mm_ss(self.remaining_time))

            logger.debug(f"Timer updated: {self.remaining_time} seconds remaining.")
            self.after(1000, self.update_timer)
        elif self.remaining_time <= 0:
            self.remaining_time = 0
            self.is_timer_running = False
            logger.info("User session ended due to time running out.")
            messagebox.showinfo("נגמר הזמן", "זמן השימוש במחשב נגמר. מתנתק.")
            self.logout()

    def update_remaining_time_label(self):
        """Update the remaining time label."""
        self.remaining_time_var.set(f"{format_time(self.remaining_time)} :שנותר זמן")
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
            from screens.login import LoginScreen
            self.app.switch_frame(LoginScreen)
        except Exception as e:
            logger.error(f"Logout failed: {e}")
            messagebox.showerror("שגיאה", f"{e} :שגיאה במהלך התנתקות")
