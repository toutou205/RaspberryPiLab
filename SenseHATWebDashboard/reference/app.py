from flask import Flask, render_template
from flask_socketio import SocketIO
from sense_hat_controller import SenseHatController

# --- 初始化 ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sense_secret'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

# --- 创建 Sense HAT 控制器实例 ---
# 将 socketio 实例传递给控制器，以便它可以在后台线程中发送数据
sense_controller = SenseHatController(socketio)

# --- Flask 路由 ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Socket.IO 事件 ---
@socketio.on('toggle_recording')
def handle_toggle_recording():
    """处理来自客户端的开始/停止数据记录（日志）请求。"""
    sense_controller.toggle_recording()

# --- 主程序入口 ---
if __name__ == '__main__':
    # 启动 Sense HAT 控制器的后台线程
    sense_controller.start_threads()
    # 启动 Flask-SocketIO 服务器
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)