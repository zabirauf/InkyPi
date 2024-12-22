from flask import Blueprint, request, jsonify, current_app, render_template, send_from_directory
from apps.app_registry import get_app_instance
from utils.app_utils import resolve_path
import os
import logging

logger = logging.getLogger(__name__)
app_bp = Blueprint("app", __name__)

APPS_DIR = resolve_path("apps")

@app_bp.route('/app/<app_id>')
def app_page(app_id):
    device_config = current_app.config['DEVICE_CONFIG']
    # Find the app by name
    app_config = next((app for app in device_config.get_apps() if app['id'] == app_id), None)
    if app_config:
        try:
            app_instance = get_app_instance(app_config)
            template_params = app_instance.generate_settings_template()
        except Exception as e:
            logger.exception("EXCEPTION CAUGHT: " + str(e))
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        return render_template('app.html', app=app_config, **template_params)
    else:
        return "App not found", 404

@app_bp.route('/images/<app_id>/<path:filename>')
def image(app_id, filename):
    return send_from_directory(APPS_DIR, os.path.join(app_id, filename))
