# -*- coding: utf-8 -*-
"""Defines the web routes for the Flask application."""

from flask import Flask, render_template


def configure_routes(app: Flask) -> None:
    """Configures the application's web routes.

    This function registers the handlers for different URL endpoints. For this
    application, it only serves the main dashboard page.

    Args:
        app: The Flask application instance.
    """

    @app.route("/")
    def index() -> str:
        """Renders the main dashboard page.

        Returns:
            The rendered 'index.html' template.
        """
        return render_template("index.html")