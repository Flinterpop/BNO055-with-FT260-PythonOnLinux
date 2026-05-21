import time
from smbus2 import SMBus

# BNO055 I2C Address (default is 0x28)
BNO055_ADDRESS = 0x28


# I2C Configuration
I2C_BUS = 9
MODE_NDOF = 0x08 # Fusion mode with 9 degrees of freedom

# Register Definitions
BNO055_OPR_MODE_ADDR = 0x3D
BNO055_QUATERNION_DATA_W_LSB = 0x20

# Operation Modes
NDOF_MODE = 0x0C

# Initialize I2C Bus (bus 1 is typical for Raspberry Pi)
bus = SMBus(I2C_BUS)

def set_operation_mode(bus, address, mode):
    """Sets the BNO055 operation mode (e.g., NDOF for quaternion output)."""
    bus.write_byte_data(address, BNO055_OPR_MODE_ADDR, mode)
    time.sleep(0.030)  # Wait 30ms for mode switch

def read_quaternion(bus, address):
    """
    Reads and scales the 4-point quaternion values (w, x, y, z).
    Returns a tuple of 4 floats.
    """
    # Read 8 continuous bytes starting from the W LSB
    data = bus.read_i2c_block_data(address, BNO055_QUATERNION_DATA_W_LSB, 8)
    
    # Convert to signed 16-bit integers
    w = (data[1] << 8) | data[0]
    x = (data[3] << 8) | data[2]
    y = (data[5] << 8) | data[4]
    z = (data[7] << 8) | data[6]
    
    # Handle signed 16-bit representation
    if w > 32767: w -= 65536
    if x > 32767: x -= 65536
    if y > 32767: y -= 65536
    if z > 32767: z -= 65536
    
    # Scale to standard quaternion range [-1.0, 1.0] (1 unit = 2^14)
    scale = 1.0 / 16384.0
    return w * scale, x * scale, y * scale, z * scale

# --- Main Program ---
try:
    print("Setting BNO055 to NDOF sensor fusion mode...")
    set_operation_mode(bus, BNO055_ADDRESS, NDOF_MODE)
    
    while True:
        qw, qx, qy, qz = read_quaternion(bus, BNO055_ADDRESS)
        print(f"Quaternion -> W: {qw:.4f}, X: {qx:.4f}, Y: {qy:.4f}, Z: {qz:.4f}")
        time.sleep(0.1) # Read data at 10Hz

except KeyboardInterrupt:
    print("\nProgram terminated.")
finally:
    bus.close()
