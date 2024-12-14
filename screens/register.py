import customtkinter as ctk
from tkinter import messagebox
from auth.auth import Auth
from screens.login import LoginScreen
from util.logger import logger  # Import the logger

class RegisterScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        logger.info("Initializing RegisterScreen")

        # Configure grid layout for dynamic vertical and horizontal centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Top space
        self.grid_rowconfigure(1, weight=0)  # Content area
        self.grid_rowconfigure(2, weight=1)  # Bottom space

        # Wrapper frame to hold all content (centered dynamically)
        self.wrapper_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.wrapper_frame.grid(row=1, column=0, sticky="nsew")  # Place in middle row
        self.wrapper_frame.grid_columnconfigure(0, weight=1)  # Center horizontally

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.wrapper_frame, text="Create an Account", font=("Arial", 36, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(0, 30))  # Space under title

        # Full Name Entry
        self.full_name_entry = ctk.CTkEntry(self.wrapper_frame, placeholder_text="Full Name", width=400, height=40)
        self.full_name_entry.grid(row=1, column=0, pady=10)

        # Email Entry
        self.email_entry = ctk.CTkEntry(self.wrapper_frame, placeholder_text="Email", width=400, height=40)
        self.email_entry.grid(row=2, column=0, pady=10)

        # Password Entry
        self.password_entry = ctk.CTkEntry(self.wrapper_frame, placeholder_text="Password", show="*", width=400, height=40)
        self.password_entry.grid(row=3, column=0, pady=10)

        # Confirm Password Entry
        self.confirm_password_entry = ctk.CTkEntry(self.wrapper_frame, placeholder_text="Confirm Password", show="*", width=400, height=40)
        self.confirm_password_entry.grid(row=4, column=0, pady=10)

        # Register Button
        self.register_button = ctk.CTkButton(
            self.wrapper_frame, text="Register", command=self.handle_register, width=400, height=40
        )
        self.register_button.grid(row=5, column=0, pady=(20, 10))

        # Back to Login Link
        self.back_to_login_link = ctk.CTkLabel(
            self.wrapper_frame,
            text="Already have an account? Login here",
            cursor="hand2",
            font=("Arial", 14, "underline"),
            text_color="lightblue"
        )
        self.back_to_login_link.grid(row=6, column=0, pady=(10, 0))
        self.back_to_login_link.bind("<Button-1>", self.go_to_login)

        # Start restrictions on RegisterScreen
        master.restriction_manager.start_restrictions()

    def handle_register(self):
        """Handle user registration."""
        full_name = self.full_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        logger.info(f"Attempting to register user: {email}")

        if not full_name.strip():
            messagebox.showerror("Error", "Full Name cannot be empty!")
            logger.warning("Registration failed: Full Name is empty")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            logger.warning("Registration failed: Passwords do not match")
            return

        try:
            response = Auth.register(email, password, full_name)
            if "error" in response:
                messagebox.showerror("Error", response["error"])
                logger.error(f"Registration failed: {response['error']}")
            else:
                messagebox.showinfo("Success", "Registration successful!")
                logger.info(f"User {email} registered successfully")
                self.master.switch_frame(LoginScreen)
        except Exception as e:
            logger.error(f"Exception during registration: {e}")
            messagebox.showerror("Error", "An unexpected error occurred during registration.")

    def go_to_login(self, event=None):
        """Switch to the login screen."""
        logger.info("Navigating to LoginScreen from RegisterScreen")
        self.master.switch_frame(LoginScreen)
