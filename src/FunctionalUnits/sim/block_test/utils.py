import struct

def float_to_hex(f):
    # Constants for maximum and minimum finite positive values
    MAX_VALUE = 3.4028235e38
    MIN_VALUE = 1.175494e-38

    # Check if the input is greater than the maximum finite positive value or smaller than the minimum positive normal value
    if f > MAX_VALUE:
        f = float('inf')
    elif f < -MAX_VALUE:
        f = float('-inf')
    elif f != 0 and abs(f) < MIN_VALUE:  # using abs here
        f = float('inf')

    # First, use the struct module to pack the float into a four byte sequence.
    # The 'f' format code specifies a single precision float, and the '<' specifies little-endian byte order.
    bytes = struct.pack('<f', f)

    # Next, unpack the bytes as an integer. The 'I' format code specifies a unsigned int, and the '<' specifies little-endian byte order.
    i = struct.unpack('<I', bytes)[0]

    # Return the integer representation
    return i

# Test with some examples
# print(float_to_hex(0.1))  # Output: 1036831949
# print(float_to_hex(-0.1))  # Output: 3217625053
# print(float_to_hex(float('inf')))  # Output: 2139095040
# print(float_to_hex(float('-inf')))  # Output: 4286578688
# print(float_to_hex(float('nan')))  # Output: 2143289344
# print(float_to_hex(3.5e38))  # Output: 2139095040
# print(float_to_hex(1e-40))  # Output: 2139095040
# print(float_to_hex(-3.5e38))  # Output: 4286578688
# print(float_to_hex(-1e-40))  # Output: 2139095040
