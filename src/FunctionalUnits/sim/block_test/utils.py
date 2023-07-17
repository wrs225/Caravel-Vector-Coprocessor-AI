import struct

def float_to_hex(f):
    # First, use the struct module to pack the float into a four byte sequence.
    # The 'f' format code specifies a single precision float, and the '<' specifies little-endian byte order.
    bytes = struct.pack('<f', f)

    # Next, unpack the bytes as an integer. The 'I' format code specifies a unsigned int, and the '<' specifies little-endian byte order.
    i = struct.unpack('<I', bytes)[0]

    # Return the integer representation
    return i
