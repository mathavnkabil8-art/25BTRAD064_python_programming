"""
OTP (One-Time Password) Generator - Mini Project
--------------------------------------------------
Features:
  1. Numeric / Alphanumeric / Alphanumeric+Special OTP generation
  2. Custom OTP length
  3. Expiry timer (configurable)
  4. Limited verification attempts (lockout after too many tries)
  5. Resend OTP option (generates a fresh one, invalidates old)
  6. OTP history log (with timestamps, saved to a text file)
  7. Multi-user support (each user_id tracked separately)
  8. Simple menu-driven CLI
"""

import random
import string
import time
from datetime import datetime


# ------------------ CORE OTP LOGIC ------------------

def generate_otp(length=6, mode="numeric"):
    """Generate an OTP based on the selected mode."""
    if mode == "numeric":
        characters = string.digits
    elif mode == "alphanumeric":
        characters = string.ascii_uppercase + string.digits
    elif mode == "strong":  # letters + digits + special characters
        characters = string.ascii_letters + string.digits + "!@#$%&*"
    else:
        raise ValueError("Invalid mode. Choose numeric, alphanumeric, or strong.")

    return ''.join(random.choice(characters) for _ in range(length))


class OTPManager:
    """Handles OTP generation, storage, verification, expiry, and attempts."""

    def __init__(self, expiry_seconds=300, max_attempts=3, log_file="otp_log.txt"):
        self.expiry_seconds = expiry_seconds
        self.max_attempts = max_attempts
        self.log_file = log_file
        # user_id -> {otp, generated_time, attempts_left, mode, length}
        self.otp_store = {}

    def _log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def generate_and_store(self, user_id, length=6, mode="numeric"):
        otp = generate_otp(length, mode)
        self.otp_store[user_id] = {
            "otp": otp,
            "generated_time": time.time(),
            "attempts_left": self.max_attempts,
            "mode": mode,
            "length": length,
        }
        self._log(f"OTP generated for '{user_id}' -> {otp} (mode={mode}, length={length})")
        return otp

    def resend_otp(self, user_id):
        """Generate a new OTP using the same settings as before."""
        if user_id not in self.otp_store:
            return None, "No previous OTP found. Generate one first."
        old = self.otp_store[user_id]
        new_otp = self.generate_and_store(user_id, old["length"], old["mode"])
        self._log(f"OTP resent for '{user_id}' -> {new_otp}")
        return new_otp, "New OTP generated successfully."

    def time_remaining(self, user_id):
        if user_id not in self.otp_store:
            return 0
        elapsed = time.time() - self.otp_store[user_id]["generated_time"]
        remaining = self.expiry_seconds - elapsed
        return max(0, round(remaining))

    def verify(self, user_id, otp_input):
        if user_id not in self.otp_store:
            return False, "No OTP generated for this user."

        record = self.otp_store[user_id]

        # Check expiry
        if time.time() - record["generated_time"] > self.expiry_seconds:
            del self.otp_store[user_id]
            self._log(f"OTP expired for '{user_id}'")
            return False, "OTP expired. Please request a new one."

        # Check attempts
        if record["attempts_left"] <= 0:
            del self.otp_store[user_id]
            self._log(f"OTP locked out for '{user_id}' (too many attempts)")
            return False, "Too many incorrect attempts. OTP invalidated."

        # Check correctness
        if otp_input == record["otp"]:
            del self.otp_store[user_id]
            self._log(f"OTP verified successfully for '{user_id}'")
            return True, "OTP verified successfully!"
        else:
            record["attempts_left"] -= 1
            self._log(f"Incorrect OTP attempt for '{user_id}', "
                      f"{record['attempts_left']} attempt(s) left")
            return False, f"Incorrect OTP. {record['attempts_left']} attempt(s) left."


# ------------------ CLI MENU ------------------

def main():
    manager = OTPManager(expiry_seconds=60, max_attempts=3)
    current_user = None

    menu = """
========== OTP GENERATOR ==========
1. Generate OTP for a user
2. Verify OTP
3. Resend OTP
4. Check time remaining
5. View OTP log
6. Exit
====================================
"""

    while True:
        print(menu)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            current_user = input("Enter user ID / email: ").strip()
            length = input("OTP length (default 6): ").strip()
            length = int(length) if length.isdigit() else 6

            print("Select OTP type: [1] Numeric  [2] Alphanumeric  [3] Strong (with symbols)")
            mode_choice = input("Choice (default 1): ").strip()
            mode_map = {"1": "numeric", "2": "alphanumeric", "3": "strong"}
            mode = mode_map.get(mode_choice, "numeric")

            otp = manager.generate_and_store(current_user, length, mode)
            print(f"\n✅ OTP generated for '{current_user}': {otp}")
            print(f"(Valid for {manager.expiry_seconds} seconds)")

        elif choice == "2":
            user_id = input("Enter user ID: ").strip()
            otp_input = input("Enter the OTP to verify: ").strip()
            success, message = manager.verify(user_id, otp_input)
            print(("✅ " if success else "❌ ") + message)

        elif choice == "3":
            user_id = input("Enter user ID: ").strip()
            new_otp, message = manager.resend_otp(user_id)
            print(message)
            if new_otp:
                print(f"New OTP: {new_otp}")

        elif choice == "4":
            user_id = input("Enter user ID: ").strip()
            remaining = manager.time_remaining(user_id)
            if remaining > 0:
                print(f"⏳ {remaining} second(s) remaining before expiry.")
            else:
                print("⚠️ OTP expired or not found.")

        elif choice == "5":
            try:
                with open(manager.log_file, "r") as f:
                    print("\n--- OTP LOG ---")
                    print(f.read())
            except FileNotFoundError:
                print("No log file found yet.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
