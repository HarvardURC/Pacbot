
from .syncclient import SyncClient

class UnavailableClient:
    def __init__(self, *args, **kwargs):
        raise ImportError("Could not import asynchronous client.")

try:
    from .asyncclient import AsyncClient
except ImportError:
    AsyncClient = UnavailableClient

__all__ = ["SyncClient", "AsyncClient"]
