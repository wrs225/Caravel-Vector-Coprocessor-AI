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
    elif f != 0 and abs(f) < MIN_VALUE:  # We don't want to turn exactly 0 into 0
        f = 0.0  # Setting the value to zero

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
# print(float_to_hex(1e-40))  # Output: 0
# print(float_to_hex(-3.5e38))  # Output: 4286578688
# print(float_to_hex(-1e-40))  # Output: 0

def ieee_754_to_float(int_val):
    # Construct the binary format string
    binary_format = ''.join(bin(int_val)[2:].zfill(32))

    # Extract sign, exponent, and mantissa from binary string
    sign = int(binary_format[0], 2)
    exponent = int(binary_format[1:9], 2)
    mantissa = int(binary_format[9:], 2)

    # If exponent is all 1's, it's either an infinity or a NaN
    if exponent == 255:
        if mantissa == 0:
            return float('inf') if sign == 0 else float('-inf')
        else:
            return float('nan')

    # If exponent and mantissa are all 0's, it's zero
    elif exponent == 0 and mantissa == 0:
        return 0.0

    # Compute the actual exponent value
    exponent = exponent - 127

    # Compute the actual mantissa value
    mantissa = 1 + mantissa / 2**23

    # Compute the final floating point value
    float_val = (-1)**sign * 2**exponent * mantissa

    return float_val

# Example: converting a 32-bit single precision IEEE 754 floating point number to a float
# int_val = 1065353216  # binary: 0b00111111100000000000000000000000, represents 1.0 in floating point
# float_val = ieee_754_to_float(int_val)
# print(float_val)  # Output: 1.0
# print(ieee_754_to_float(0x3d1a52aa))