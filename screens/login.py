import customtkinter as ctk
from tkinter import messagebox
from auth.auth import Auth
from screens.main_ui import MainUI
from util.logger import logger


class LoginScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        logger.info("Initializing LoginScreen")

        # Configure grid layout for dynamic vertical and horizontal centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Top space
        self.grid_rowconfigure(1, weight=0)  # Content area
        self.grid_rowconfigure(2, weight=1)  # Bottom space

        # Wrapper frame to hold all content (centered dynamically)
        self.wrapper_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.wrapper_frame.grid(row=1, column=0, sticky="nsew")  # Place content in the middle row
        self.wrapper_frame.grid_columnconfigure(0, weight=1)  # Center horizontally

        # Title
        self.title_label = ctk.CTkLabel(
            self.wrapper_frame, text="Welcome Back!", font=("Arial", 36, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(0, 30))  # Space below title

        # Email Entry
        self.email_entry = ctk.CTkEntry(
            self.wrapper_frame, placeholder_text="Email", width=400, height=40
        )
        self.email_entry.grid(row=1, column=0, pady=10)

        # Password Entry
        self.password_entry = ctk.CTkEntry(
            self.wrapper_frame, placeholder_text="Password", show="*", width=400, height=40
        )
        self.password_entry.grid(row=2, column=0, pady=10)

        # Forgot Password Link
        self.reset_password_link = ctk.CTkLabel(
            self.wrapper_frame,
            text="Forgot your password?",
            cursor="hand2",
            font=("Arial", 14, "underline"),
            text_color="lightblue",
        )
        self.reset_password_link.grid(row=3, column=0, pady=(0, 20))  # Space under password field
        self.reset_password_link.bind("<Button-1>", self.reset_password)

        # Login Button
        self.login_button = ctk.CTkButton(
            self.wrapper_frame, text="Login", command=self.login, width=200, height=40
        )
        self.login_button.grid(row=4, column=0, pady=(10, 20))  # Space above and below button

        # Register Link
        self.register_link = ctk.CTkLabel(
            self.wrapper_frame,
            text="Don't have an account? Register here",
            cursor="hand2",
            font=("Arial", 14, "underline"),
            text_color="lightblue",
        )
        self.register_link.grid(row=5, column=0, pady=(10, 0))  # Space below
        self.register_link.bind("<Button-1>", self.go_to_register)

        # Start restrictions
        master.restriction_manager.start_restrictions()

    def login(self):
        """Handle user login."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        logger.info(f"Attempting login for email: {email}")

        response = Auth.login(email, password)

        if "error" in response:
            logger.error(f"Login failed: {response['error']}")
            messagebox.showerror("Login Failed", response["error"])
        else:
            logger.info("Login successful")
            messagebox.showinfo("Success", "Login successful!")
            logger.info("Navigating to MainUI")
            self.master.switch_frame(MainUI, response)

    def go_to_register(self, event=None):
        """Switch to the register screen."""
        logger.info("Navigating to RegisterScreen")
        from screens.register import RegisterScreen
        self.master.switch_frame(RegisterScreen)

    def reset_password(self, event=None):
        """Handle password reset."""
        email = self.email_entry.get()
        if not email:
            logger.warning("Reset password attempt without email")
            messagebox.showerror("Error", "Please enter your email to reset your password.")
            return

        logger.info(f"Attempting to send password reset link for email: {email}")
        response = Auth.reset_password(email)
        if "error" in response:
            logger.error(f"Password reset failed: {response['error']}")
            messagebox.showerror("Error", response["error"])
        else:
            logger.info("Password reset link sent successfully")
            messagebox.showinfo("Success", "Password reset link sent to your email!")
