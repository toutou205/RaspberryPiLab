import os
from datetime import datetime

class DataLogger:
    def __init__(self, log_dir="logs"):
        """
        Initializes the DataLogger.
        :param log_dir: The directory where log files will be stored.
        """
        self.log_dir = log_dir
        self.log_file_path = None
        self.log_file = None
        self.is_running = False

    def start(self):
        """
        Starts the logging session. Creates a new log file with a timestamped name.
        """
        if self.is_running:
            print("Logger is already running.")
            return

        # Create log directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Create a new log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file_path = os.path.join(self.log_dir, f"log_{timestamp}.csv")
        
        try:
            self.log_file = open(self.log_file_path, "w", newline='')
            self.is_running = True
            print(f"Logging started. Data will be saved to {self.log_file_path}")
        except IOError as e:
            print(f"Error opening log file: {e}")

    def stop(self):
        """
        Stops the logging session and closes the log file.
        """
        if not self.is_running:
            print("Logger is not running.")
            return

        if self.log_file:
            self.log_file.close()
            self.log_file = None
        
        self.is_running = False
        print("Logging stopped.")

    def log(self, data):
        """
        Logs the given data to the log file.
        :param data: The data to be logged (e.g., a dictionary or a string).
        """
        if not self.is_running or not self.log_file:
            # Silently ignore if logger is not running
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        
        if isinstance(data, dict):
            if self.log_file.tell() == 0:
                # Write header for dictionaries
                header = "timestamp," + ",".join(data.keys()) + "\n"
                self.log_file.write(header)
            
            row = f"{timestamp}," + ",".join(map(str, data.values())) + "\n"
            self.log_file.write(row)
        else:
            self.log_file.write(f"{timestamp},{data}\n")