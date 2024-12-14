from config import auth, db

class Auth:
    @staticmethod
    def login(email, password):
        try:
            # Authenticate the user
            user = auth.sign_in_with_email_and_password(email, password)

            # Fetch additional data from the database
            local_id = user["localId"]  # Extract the user's unique identifier
            user_data = db.child("users").child(local_id).get().val()

            # Ensure user data exists and is valid
            if not user_data or "remaining_time" not in user_data or "full_name" not in user_data:
                return {"error": "User data is incomplete in the database."}

            # Mark user as logged in
            db.child("users").child(local_id).update({"is_logged_in": True})

            # Attach additional data to the user object
            user["remaining_time"] = user_data["remaining_time"]
            user["full_name"] = user_data["full_name"]

            return user
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def register(email, password, full_name):
        try:
            # Create the user
            user = auth.create_user_with_email_and_password(email, password)

            # Store additional user information in the database
            db.child("users").child(user["localId"]).set({
                "full_name": full_name,
                "email": email,
                "remaining_time": 0  # Default remaining time
            })

            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def reset_password(email):
        try:
            auth.send_password_reset_email(email)
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}
