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
