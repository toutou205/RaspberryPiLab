# -*- coding: utf-8 -*-
"""Handles data logging to CSV files."""

import csv
import os
from datetime import datetime
from typing import IO, Any, Dict, List, Optional


class DataLogger:
    """A class to handle logging of sensor data to timestamped CSV files.

    This implementation uses the standard `csv` module for robust CSV writing.
    """

    def __init__(self, log_dir: str = "logs") -> None:
        """Initializes the DataLogger.

        Args:
            log_dir (str): The directory where log files will be stored.
                           It will be created if it doesn't exist.
        """
        self.log_dir: str = log_dir
        self.is_recording: bool = False
        self.log_file_path: Optional[str] = None
        self._file: Optional[IO[str]] = None
        self._csv_writer: Optional[Any] = None
        self._header: List[str] = [
            'timestamp', 'temp', 'humidity', 'pressure', 'altitude',
            'pitch', 'roll', 'yaw', 'mode_id', 'mode_name',
            'joystick_direction', 'joystick_action'
        ]

    def start(self) -> None:
        """Starts a new logging session.

        Creates the log directory if it doesn't exist, and opens a new
        timestamped CSV file, writing the header immediately.
        """
        if self.is_recording:
            print("Logger is already recording.")
            return

        os.makedirs(self.log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file_path = os.path.join(self.log_dir, f"sensordata_{timestamp}.csv")

        try:
            self._file = open(self.log_file_path, 'w', newline='', encoding='utf-8')
            self._csv_writer = csv.writer(self._file)
            self._csv_writer.writerow(self._header)
            self.is_recording = True
            print(f"Logging started. Data will be saved to {self.log_file_path}")
        except IOError as e:
            print(f"Error opening log file: {e}")
            self.stop()

    def stop(self) -> None:
        """Stops the current logging session and closes the file."""
        if not self.is_recording and self._file is None:
            return

        if self._file:
            self._file.close()

        self.is_recording = False
        self._file = None
        self._csv_writer = None
        print(f"Logging stopped. Log file saved at: {self.log_file_path}")

    def record_data(self, data_packet: Dict[str, Dict[str, Any]]) -> None:
        """Writes a single data packet to the CSV file.

        Args:
            data_packet (Dict[str, Dict[str, Any]]): The structured sensor
                data packet containing 'env' and 'imu' dictionaries.
        """
        if not self.is_recording or not self._csv_writer:
            return

        env = data_packet.get('env', {})
        imu = data_packet.get('imu', {})
        sys = data_packet.get('sys', {})
        joystick = data_packet.get('joystick', {})
        timestamp = datetime.now().isoformat()

        try:
            self._csv_writer.writerow([
                timestamp,
                env.get('temp', ''),
                env.get('humidity', ''),
                env.get('pressure', ''),
                env.get('altitude', ''),
                imu.get('pitch', ''),
                imu.get('roll', ''),
                imu.get('yaw', ''),
                sys.get('mode_id', ''),
                sys.get('mode_name', ''),
                joystick.get('direction', ''),
                joystick.get('action', '')
            ])
        except (IOError, csv.Error) as e:
            print(f"Error writing to log file: {e}")
            self.stop()