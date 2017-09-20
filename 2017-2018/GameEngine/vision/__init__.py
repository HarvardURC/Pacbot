
try:
    # If the prerequisites for the cv module are missing it will use the
    # keyboard shim
    from .cv import MovementProcessor
except ImportError:
    from .shim import MovementProcessor

__all__ = ["MovementProcessor"]

