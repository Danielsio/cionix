import customtkinter as ctk
from tkinter import messagebox

class HelpTab(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)

        # Help message
        help_message = "For assistance, please contact: admin@example.com"
        self.help_label = ctk.CTkLabel(self, text=help_message, font=("Arial", 16))
        self.help_label.pack(pady=20)

        # Contact Button
        self.contact_button = ctk.CTkButton(
            self,
            text="Contact Admin",
            command=self.contact_admin
        )
        self.contact_button.pack(pady=10)

    def contact_admin(self):
        # Example: Show a message
        messagebox.showinfo("Contact Admin", "Email sent to admin@example.com.")
