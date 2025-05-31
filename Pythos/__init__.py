# pythosmc/__init__.py

# Project metadata
__version__ = "0.1.0"
__author__ = "Angadpal"
__license__ = "MIT"  # or whatever license you choose

# High-level imports to simplify usage
from .core.server import start_server
from .config.settings import SERVER_NAME, PORT, MOTD, IP

# Expose top-level API
__all__ = ["start_server", "SERVER_NAME", "PORT", "MOTD", "IP"]
