import logging
import random
import string
import pyperclip
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpinBox, QMessageBox
)
from PyQt6.QtGui import QFont
import configparser
import sys

# Configure logging
logging.basicConfig(filename='password_generator.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration file
CONFIG_FILE = 'users.ini'

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
            charset = string.ascii_lowercase + string.digits
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

class PasswordStrengthWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.bars = [QLabel(self) for _ in range(4)]
        for bar in self.bars:
            bar.setFixedSize(20, 20)
            bar.setStyleSheet("background-color: lightgray; border-radius: 10px;")
            self.layout.addWidget(bar)
        self.strength_label = QLabel(self)
        self.layout.addWidget(self.strength_label)
        self.setLayout(self.layout)

    def set_strength(self, strength, strength_name):
        colors = ["lightgray", "green", "yellow", "green"]
        for i in range(4):
            if i < strength:
                self.bars[i].setStyleSheet(f"background-color: {colors[strength]}; border-radius: 10px;")
            else:
                self.bars[i].setStyleSheet("background-color: lightgray; border-radius: 10px;")
        self.strength_label.setText(strength_name)

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = CredentialManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Username and Password Generator')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        title = QLabel('Username and Password Generator')
        title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # Username length input
        self.username_length_label = QLabel('Username Length:')
        self.username_length_spinbox = QSpinBox()
        self.username_length_spinbox.setRange(6, 20)

        layout.addWidget(self.username_length_label)
        layout.addWidget(self.username_length_spinbox)

        # Password length input
        self.password_length_label = QLabel('Password Length:')
        self.password_length_spinbox = QSpinBox()
        self.password_length_spinbox.setRange(6, 20)

        layout.addWidget(self.password_length_label)
        layout.addWidget(self.password_length_spinbox)

        # Manual username input
        self.username_input_label = QLabel('Enter Username:')
        self.username_input = QLineEdit()

        layout.addWidget(self.username_input_label)
        layout.addWidget(self.username_input)

        # Generate button
        self.generate_button = QPushButton('Generate')
        self.generate_button.clicked.connect(self.generate)

        layout.addWidget(self.generate_button)

        # Username display
        self.username_label = QLabel('Username:')
        self.username_entry = QLineEdit()

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)

        # Password display
        self.password_label = QLabel('Password:')
        self.password_entry = QLineEdit()

        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)

        # Password strength display
        self.strength_label = QLabel('Password Strength:')
        layout.addWidget(self.strength_label)
        self.strength_widget = PasswordStrengthWidget()
        layout.addWidget(self.strength_widget)

        # Copy button
        self.copy_button = QPushButton('Copy Credentials')
        self.copy_button.clicked.connect(self.copy)

        layout.addWidget(self.copy_button)

        # Save button
        self.save_button = QPushButton('Save Credentials')
        self.save_button.clicked.connect(self.save)

        layout.addWidget(self.save_button)

        # Login section
        login_title = QLabel('User Login')
        login_title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        layout.addWidget(login_title)

        self.login_username_label = QLabel('Username:')
        self.login_username_entry = QLineEdit()

        layout.addWidget(self.login_username_label)
        layout.addWidget(self.login_username_entry)

        self.login_password_label = QLabel('Password:')
        self.login_password_entry = QLineEdit()
        self.login_password_entry.setEchoMode(QLineEdit.EchoMode.Password)  # Set password entry to show as ***

        layout.addWidget(self.login_password_label)
        layout.addWidget(self.login_password_entry)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def generate(self):
        try:
            password_length = self.password_length_spinbox.value()
            username_length = self.username_length_spinbox.value()

            password = self.manager.generate_password(password_length)
            username = self.username_input.text() or self.manager.generate_username(username_length)

            if self.manager.config.has_option('Users', username):
                self.manager.show_message("Error", "Username already exists. Please enter a different username.")
                return

            strength_value, strength_name = self.manager.evaluate_password_strength(password)

            self.username_entry.setText(username)
            self.password_entry.setText(password)
            self.strength_widget.set_strength(strength_value, strength_name)
        except Exception as e:
            logging.error(f"Error generating credentials: {e}")

    def copy(self):
        try:
            username = self.username_entry.text()
            password = self.password_entry.text()
            credentials = f"Username: {username}\nPassword: {password}"
            pyperclip.copy(credentials)
        except Exception as e:
            logging.error(f"Error copying credentials to clipboard: {e}")

    def save(self):
        try:
            username = self.username_entry.text()
            password = self.password_entry.text()
            strength_value, strength_name = self.manager.evaluate_password_strength(password)

            if self.manager.config.has_option('Users', username):
                self.manager.show_message("Error", "Username already exists. Please enter a different username.")
                return

            if strength_value < 3:  # Assume strength 3 or 4 is strong enough
                self.manager.show_message("Weak Password", "The password you entered is not strong enough. Please use a stronger password.")
                return

            self.manager.save_credentials(username, password)
        except Exception as e:
            logging.error(f"Error saving credentials: {e}")

    def login(self):
        try:
            username = self.login_username_entry.text()
            password = self.login_password_entry.text()
            if self.manager.validate_login(username, password):
                self.manager.show_message("Login Successful", "You have successfully logged in.")
            else:
                self.manager.show_message("Login Failed", "Incorrect username or password.")
        except Exception as e:
            logging.error(f"Error during login: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())
