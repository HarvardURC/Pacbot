
from .syncclient import SyncClient

from .constants import MAGIC_HEADER, SIZE_HEADER

class UnavailableClient:
    def __init__(self, *args, **kwargs):
        raise ImportError("Could not import asynchronous client.")

try:
    from .asyncclient import AsyncClient
except ImportError:
    AsyncClient = UnavailableClient

def pack_msg(msg):
    length = SIZE_HEADER.pack(MAGIC_HEADER, len(msg))
    return length + msg
    
__all__ = ["SyncClient", "AsyncClient"]
