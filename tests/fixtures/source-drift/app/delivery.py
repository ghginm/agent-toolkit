import importlib
from .config import DELIVERY_PLUGIN

def publish(summary):
    """Delegate once; transport internals are not bundled here."""
    transport = importlib.import_module(DELIVERY_PLUGIN)
    return transport.send(summary)
