# -*- coding: utf-8 -*-
"""Application configuration file.

This file centralizes all the configuration variables for the application.
By convention, configuration variables are in uppercase.
"""

import os

# --- Flask & SocketIO Configuration ---
SECRET_KEY: str = 'your_default_secret_key'  # Change this in a production environment
# Reason for change: Centralizes the secret key into a configuration file,
# making it easier to manage and change without altering the application logic.

# --- Application Behavior ---
# Defines the delay (in seconds) between sensor readings in the background thread.
# A smaller value leads to more frequent updates but higher CPU usage.
SENSOR_READ_INTERVAL: float = 0.1
# Reason for change: Makes the sensor reading interval a configurable parameter.
# This is better than a magic number in the code.

# --- Data Logger Configuration ---
# Defines the directory where data logs are stored.
LOG_DIRECTORY: str = "logs"
# Reason for change: Hardcoded "logs" directory is now a configurable setting.

# --- Sense HAT Default/Mock Values ---
# These values are used when the Sense HAT hardware is not detected.
DEFAULT_TEMPERATURE: float = 25.0
DEFAULT_PRESSURE: float = 1013.25
DEFAULT_HUMIDITY: float = 45.0
DEFAULT_ORIENTATION: dict[str, float] = {'pitch': 0, 'roll': 0, 'yaw': 0}

# --- Physics Constants ---
# Standard sea level atmospheric pressure in hPa. Used for altitude calculation.
SEA_LEVEL_PRESSURE: float = 1013.25
# Reason for change: Moves the physical constant for sea level pressure to the config file
# to make altitude calculations more transparent and potentially adjustable.

# Reason for change: Consolidates all mock data values in one place for clarity and ease of modification.

# --- Network Configuration ---
# The host and port on which the web server will listen.
# '0.0.0.0' makes the server accessible from any IP address on the network.
SERVER_HOST: str = '0.0.0.0'
SERVER_PORT: int = 5000
# Reason for change: Network settings are now configurable.

# --- Environment Configuration ---
# Set to True to enable debug mode for Flask.
# WARNING: Do not use debug mode in a production environment.
DEBUG_MODE: bool = True
# Reason for change: Allows enabling/disabling Flask's debug mode via configuration.

# --- LED Display Modes ---
# Defines the different visualization modes for the 8x8 LED matrix.
# Each mode is a dictionary with an id, name, and description.
LED_MODES: list[dict[str, int | str]] = [
    {"id": 0, "name": "Monitor Mode", "desc": "显示静态状态指示灯"},
    {"id": 1, "name": "Spirit Level", "desc": "水平仪 (姿态可视化)"},
    {"id": 2, "name": "Rainbow Wave", "desc": "动态彩虹波浪"},
    {"id": 3, "name": "Fire Effect", "desc": "随机火焰粒子"}
]
# Reason for change: Moves the LED mode definitions to a central configuration file.
# This makes it easy to add, remove, or change modes without code modification.


# --- Joystick Configuration ---
# Defines the string identifiers for joystick events.
JOYSTICK_DIRECTIONS: dict[str, str] = {
    "LEFT": "left",
    "RIGHT": "right",
    "UP": "up",
    "DOWN": "down",
    "MIDDLE": "middle",
}
# Reason for change: Replaces magic strings in the joystick handler with named constants
# to prevent typos and improve code clarity.

# --- LED Display Configuration ---
# The RGB color used to briefly show the current mode number on the LED matrix.
MODE_DISPLAY_COLOR: list[int] = [0, 0, 255]  # Blue
# The duration (in seconds) to display the mode number.
MODE_DISPLAY_DURATION: float = 0.5
# Reason for change: Extracts hardcoded values for LED display feedback into
# configuration variables, making them easy to adjust.

