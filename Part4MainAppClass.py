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


            
