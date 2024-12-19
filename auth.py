from config import auth, db
from util.logger import logger
import json

class FirebaseAuth:
    @staticmethod
    def login(email, password):
        try:
            # Authenticate the user
            user = auth.sign_in_with_email_and_password(email, password)

            # Extract localId and displayName
            local_id = user["localId"]  # Extract the user's unique identifier

            # Fetch additional data from the database
            user_data = db.child("users").child(local_id).get(user["idToken"]).val()

            # If user data doesn't exist, initialize it with default values
            if not user_data:
                user_data = {
                    "remaining_time": 0,  # Default remaining time
                    "is_logged_in": True
                }
                db.child("users").child(local_id).set(user_data, user["idToken"])
            else:
                # Ensure user data has the necessary fields
                user_data.setdefault("remaining_time", 0)
                db.child("users").child(local_id).update({"is_logged_in": True}, user["idToken"])

            # Attach additional data to the user object
            user["remaining_time"] = user_data["remaining_time"]

            return user
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return {"error": str(e)}

    @staticmethod
    def register(email, password, full_name):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            auth.update_profile(user['idToken'], full_name)
            return {"success": True, "user_id": user["localId"]}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def reset_password(email):
        try:
            # Send a password reset email
            auth.send_password_reset_email(email)
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def logout(user):
        try:
            db.child("users").child(user["localId"]).update({
                "remaining_time": user.get("remaining_time", 0),
                "is_logged_in": False
            }, user["idToken"])
            logger.info("User logged out successfully.")
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            raise