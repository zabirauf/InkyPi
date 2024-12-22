# app_registry.py

import os
import importlib
import logging
from utils.app_utils import resolve_path
from pathlib import Path

logger = logging.getLogger(__name__)
APPS_DIR = 'apps'
APP_CLASSES = {}

def load_apps(apps_config):
    apps_module_path = Path(resolve_path(APPS_DIR))
    for app in apps_config:
        app_id = app.get('id')
        if app.get("disabled", False):
            logging.info(f"App {app_id} is disabled, skipping.")
            continue
        
        app_dir = apps_module_path / app_id
        if not app_dir.is_dir():
            logging.error(f"Could not find app directory {app_dir} for '{app_id}', skipping.")
            continue

        module_path = app_dir / f"{app_id}.py"
        if not module_path.is_file():
            logging.error(f"Could not find module path {module_path} for '{app_id}', skipping.")
            continue
        
        module_name = f"apps.{app_id}.{app_id}"
        try:
            module = importlib.import_module(module_name)
            app_class = getattr(module, app.get("class"), None)

            if app_class:
                # Create an instance of the app class and add it to the app_classes dictionary
                APP_CLASSES[app_id] = app_class(app)

        except ImportError as e:
            logging.error(f"Failed to import app module {module_name}: {e}")

def get_app_instance(app_config):
    app_id = app_config.get("id")
    # Retrieve the app class factory function
    app_class = APP_CLASSES.get(app_id)
    
    if app_class:
        # Initialize the app with its configuration
        return app_class
    else:
        raise ValueError(f"App '{app_id}' is not registered.")