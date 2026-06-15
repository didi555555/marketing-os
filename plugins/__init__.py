import importlib
import os
from pathlib import Path

def discover_plugins():
    plugins = {}
    plugins_dir = Path(__file__).parent
    for item in plugins_dir.iterdir():
        if item.is_dir() and not item.name.startswith('_'):
            info_file = item / "info.json"
            if info_file.exists():
                import json
                info = json.loads(info_file.read_text(encoding='utf-8'))
                plugins[item.name] = info
    return plugins

def register_plugins(app):
    plugins_dir = Path(__file__).parent
    for item in plugins_dir.iterdir():
        if item.is_dir() and not item.name.startswith('_'):
            routes_file = item / "routes.py"
            if routes_file.exists():
                module_name = f"plugins.{item.name}.routes"
                try:
                    mod = importlib.import_module(module_name)
                    if hasattr(mod, 'register'):
                        mod.register(app)
                except Exception as e:
                    print(f"[Plugin] Failed to load {item.name}: {e}")
