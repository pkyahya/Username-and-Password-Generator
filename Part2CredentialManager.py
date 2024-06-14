class CredentialManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE)

    def generate_password(self, length):
        try:
            charset = string.ascii_letters + string.digits + string.punctuation
            return ''.join(random.choice(charset) for _ in range(length))
        except Exception as e:
            logging.error(f"Error generating password: {e}")

    def generate_username(self, length):
        try:
            charset = string.ascii_lowercase + string.digit
            return ''.join(random.choices(charset, k=length))
        except Exception as e:
            logging.error(f"Error generating username: {e}")

    def evaluate_password_strength(self, password):
        if len(password) < 6:
            return 0, "Too short"
        strength = sum([any(c in group for c in password) for group in (string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation)])
        strength_names = {1: "Weak", 2: "Moderate", 3: "Strong", 4: "Very Strong"}
        return strength, strength_names.get(strength, "Unknown")

    def save_credentials(self, username, password):
        try:
            if not self.config.has_section('Users'):
                self.config.add_section('Users')
            self.config.set('Users', username, password)
            with open(CONFIG_FILE, 'w') as configfile:
                self.config.write(configfile)
            self.show_message("Saved", "Username and password saved successfully.")
        except Exception as e:
            logging.error(f"Error saving credentials: {e}")

    def validate_login(self, username, password):
        try:
            return self.config.has_option('Users', username) and self.config.get('Users', username) == password
        except Exception as e:
            logging.error(f"Error during login: {e}")
            return False

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec()
