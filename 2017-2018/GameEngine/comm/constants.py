import struct

# Message sizes are communicated as a single unsigned short
# encoded using network byte-order (big-endian).
# receiving libraries will need to account for this properly.
# The header also includes a magic number (also a short) for verification
MAGIC_HEADER = 11297
SIZE_HEADER = struct.Struct("!HH")
