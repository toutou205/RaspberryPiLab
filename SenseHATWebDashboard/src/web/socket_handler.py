from flask_socketio import SocketIO
from src.core.logger import DataLogger

def configure_socket_handlers(socketio: SocketIO, logger: DataLogger):
    """
    配置SocketIO事件处理程序。

    Args:
        socketio (SocketIO): Flask-SocketIO实例。
        logger (DataLogger): DataLogger实例。
    """
    @socketio.on('toggle_record')
    def handle_toggle_record(data):
        """
        处理前端发送的toggle_record事件来控制日志记录。
        """
        is_recording = logger.is_recording()
        if not is_recording:
            logger.start_recording()
            print("Started recording.")
        else:
            csv_path = logger.stop_recording()
            print(f"Stopped recording. Log saved to: {csv_path}")

        # 向客户端广播新的录制状态
        socketio.emit('new_data', {
            "recording": logger.is_recording()
        })
