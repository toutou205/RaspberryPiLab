from flask import render_template

def configure_routes(app):
    """
    配置Flask的路由。

    Args:
        app (Flask): Flask应用实例。
    """
    @app.route('/')
    def index():
        """渲染主页面"""
        return render_template('index.html')
