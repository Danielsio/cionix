import customtkinter as ctk
from tkinter import messagebox
from auth import FirebaseAuth
from screens.login import LoginScreen
from util.logger import logger


class RegisterScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        logger.info("Initializing RegisterScreen")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Top space
        self.grid_rowconfigure(1, weight=0)  # Content area
        self.grid_rowconfigure(2, weight=1)  # Bottom space

        # Wrapper frame
        self.wrapper_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.wrapper_frame.grid(row=1, column=0, sticky="nsew")
        self.wrapper_frame.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.wrapper_frame, text="צור חשבון חדש", font=("Arial", 36, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(0, 30))

        # Full Name Entry
        self.full_name_entry = self._create_entry("שם מלא", 1)

        # Email Entry
        self.email_entry = self._create_entry("אימייל", 2)

        # Password Entry
        self.password_entry = self._create_entry("סיסמה", 3, show="*")

        # Confirm Password Entry
        self.confirm_password_entry = self._create_entry("אישור סיסמה", 4, show="*")

        # Register Button
        self.register_button = ctk.CTkButton(
            self.wrapper_frame,
            text="הרשמה",
            command=self.handle_register,
            width=400,
            height=40,
        )
        self.register_button.grid(row=5, column=0, pady=(20, 10))

        # Back to Login Link
        self.back_to_login_link = ctk.CTkLabel(
            self.wrapper_frame,
            text="!כבר יש לך חשבון? התחבר כאן",
            cursor="hand2",
            font=("Arial", 14, "underline"),
            text_color="lightblue",
        )
        self.back_to_login_link.grid(row=6, column=0, pady=(10, 0))
        self.back_to_login_link.bind("<Button-1>", self.go_to_login)

        # Start restrictions on RegisterScreen
        master.restriction_manager.start_restrictions()

    def _create_entry(self, placeholder, row, show=None):
        """Create a simple entry field."""
        entry = ctk.CTkEntry(
            self.wrapper_frame,
            placeholder_text=placeholder,
            width=400,
            height=40,
            show=show,
            justify="right",  # RTL alignment for Hebrew
        )
        entry.grid(row=row, column=0, pady=10)
        return entry

    def handle_register(self):
        """Handle user registration."""
        full_name = self.full_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        logger.info(f"Attempting to register user: {email}")

        if not full_name.strip():
            messagebox.showerror("שגיאה", "שם מלא לא יכול להיות ריק!")
            logger.warning("Registration failed: Full Name is empty")
            return

        if password != confirm_password:
            messagebox.showerror("שגיאה", "הסיסמאות אינן תואמות!")
            logger.warning("Registration failed: Passwords do not match")
            return

        try:
            response = FirebaseAuth.register(email, password, full_name)
            if "error" in response:
                messagebox.showerror("שגיאה", response["error"])
                logger.error(f"Registration failed: {response['error']}")
            else:
                messagebox.showinfo("הצלחה", "!ההרשמה הצליחה")
                logger.info(f"User {email} registered successfully")
                self.master.switch_frame(LoginScreen)
        except Exception as e:
            logger.error(f"Exception during registration: {e}")
            messagebox.showerror("שגיאה", "אירעה שגיאה לא צפויה במהלך ההרשמה.")

    def go_to_login(self, event=None):
        """Switch to the login screen."""
        logger.info("Navigating to LoginScreen from RegisterScreen")
        self.master.switch_frame(LoginScreen)
