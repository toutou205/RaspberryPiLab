# -*- coding: utf-8 -*-
"""Defines the background thread for continuously reading and processing sensor data."""

import time
from threading import Event, Thread

from flask_socketio import SocketIO

from .. import config
from .calculator import pressure_to_altitude
from .logger import DataLogger
from ..hardware.display import LEDDisplay
from ..hardware.sense_driver import SenseHatWrapper


class SensorDataThread(Thread):
    """
    A thread that runs the application's main loop.

    It continuously reads sensor data, handles joystick input, updates the LED
    display, and emits data to the web client via SocketIO.
    """

    def __init__(
        self,
        socketio: SocketIO,
        sense_wrapper: SenseHatWrapper,
        led_display: LEDDisplay,
        logger: DataLogger,
    ) -> None:
        """Initializes the thread and the application state.

        Args:
            socketio: An initialized Flask-SocketIO server instance.
            sense_wrapper: An instance of the Sense HAT hardware wrapper.
            led_display: An instance of the LED display controller.
            logger: An instance of the data logger.
        """
        # Reason for change: Added a detailed Google-style docstring for clarity.
        super().__init__()
        self.daemon = True

        # Injected components
        self.socketio = socketio
        self.sense_wrapper = sense_wrapper
        self.led_display = led_display
        self.logger = logger

        # Application state
        self.current_mode: int = 0
        self.is_on: bool = True
        self.stop_event = Event()

        # Start the joystick listener and register the callback
        self.sense_wrapper.start_joystick_listener(self._handle_joystick)

    def _handle_joystick(self, event_direction: str) -> None:
        """Callback function to handle joystick events.

        This method is called from the SenseHatWrapper's joystick thread.
        It modifies the application state based on the joystick input.

        Args:
            event_direction: The direction of the joystick event.
        """
        # Reason for change: Replaced magic strings with constants from the config file
        # to improve maintainability and prevent errors from typos.
        print(f"Joystick event received: {event_direction}")
        if event_direction == config.JOYSTICK_DIRECTIONS["LEFT"]:
            self.current_mode = (self.current_mode - 1) % len(config.LED_MODES)
            self.sense_wrapper.show_letter(
                str(self.current_mode), text_colour=config.MODE_DISPLAY_COLOR
            )
            time.sleep(config.MODE_DISPLAY_DURATION)  # Brief display of the mode number
        elif event_direction == config.JOYSTICK_DIRECTIONS["RIGHT"]:
            self.current_mode = (self.current_mode + 1) % len(config.LED_MODES)
            self.sense_wrapper.show_letter(
                str(self.current_mode), text_colour=config.MODE_DISPLAY_COLOR
            )
            time.sleep(config.MODE_DISPLAY_DURATION)
        elif event_direction == config.JOYSTICK_DIRECTIONS["UP"]:
            self.sense_wrapper.set_low_light(False)
        elif event_direction == config.JOYSTICK_DIRECTIONS["DOWN"]:
            self.sense_wrapper.set_low_light(True)
        elif event_direction == config.JOYSTICK_DIRECTIONS["MIDDLE"]:
            self.is_on = not self.is_on
            print(f"Display toggled: {'ON' if self.is_on else 'OFF'}")

    def run(self) -> None:
        """The main loop of the thread.

        This method constitutes the core logic of the application, running in a
        continuous loop until the stop event is set. It performs the following
        actions on each iteration:
        1. Reads all relevant sensor data from the Sense HAT.
        2. Updates the LED matrix display based on the current mode.
        3. Emits the collected data to the web client via SocketIO.
        4. Logs the data to a file if recording is enabled.
        5. Pauses for a configured interval before the next iteration.
        """
        # Reason for change: Added a detailed Google-style docstring for clarity.
        print("Background data-reading thread started.")
        while not self.stop_event.is_set():
            # 1. Read sensor data
            temp = self.sense_wrapper.get_temperature()
            pressure = self.sense_wrapper.get_pressure()
            humidity = self.sense_wrapper.get_humidity()
            orientation = self.sense_wrapper.get_orientation()
            altitude = pressure_to_altitude(pressure, config.SEA_LEVEL_PRESSURE)
            
            # Retrieve latest joystick state
            joystick_event = self.sense_wrapper.last_joystick_event

            # 2. Update LED display
            # The display logic needs the current state and sensor data
            self.led_display.update_display(
                mode=self.current_mode,
                is_on=self.is_on,
                orientation=orientation,
            )

            # 3. Prepare data packet
            data_packet = {
                'env': {
                    'temp': round(temp, 1),
                    'humidity': round(humidity, 1),
                    'pressure': round(pressure, 1),
                    'altitude': round(altitude, 1),
                },
                'imu': {
                    'pitch': round(orientation['pitch'], 1),
                    'roll': round(orientation['roll'], 1),
                    'yaw': round(orientation['yaw'], 1),
                },
                'sys': {
                    'mode_id': self.current_mode,
                    'mode_name': config.LED_MODES[self.current_mode]['name'],
                    'is_on': self.is_on,
                    'is_recording': self.logger.is_recording,
                },
                'joystick': {
                    'direction': joystick_event['direction'] if joystick_event else '',
                    'action': joystick_event['action'] if joystick_event else '',
                },
            }

            # 4. Emit data to client
            self.socketio.emit('sensor_update', data_packet)

            # 5. Log data if recording
            if self.logger.is_recording:
                self.logger.record_data(data_packet)

            time.sleep(config.SENSOR_READ_INTERVAL)
        print("Background data-reading thread stopped.")

    def stop(self) -> None:
        """Signals the thread to stop gracefully."""
        # Reason for change: Added a detailed Google-style docstring for clarity.
        print("Signaling background thread to stop.")
        self.stop_event.set()