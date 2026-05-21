import math

import time
from smbus2 import SMBus

I2C_BUS = 9 
BNO055_ADDR = 0x28

# BNO055 Register Addresses
BNO055_QUA_DATA_W_LSB = 0x20

def read_bno055_quaternion(bus):
    # Read 8 bytes starting from the W component's LSB
    data = bus.read_i2c_block_data(BNO055_ADDR, BNO055_QUA_DATA_W_LSB, 8)
    
    # Combine LSB and MSB for each component, then scale by 2^14 (16384)
    scale = 16384.0
    
    w = (data[1] << 8 | data[0]) / scale
    x = (data[3] << 8 | data[2]) / scale
    y = (data[5] << 8 | data[4]) / scale
    z = (data[7] << 8 | data[6]) / scale
    
    return w, x, y, z

def quaternion_to_euler(w, x, y, z):
    """
    Converts quaternion to Euler angles (Roll, Pitch, Yaw) in degrees
    using the BNO055's coordinate system.
    """
    # Roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)
    
    # Pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp) # Use 90 degrees if out of range
    else:
        pitch = math.asin(sinp)
        
    # Yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)
    
    # Convert radians to degrees
    return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)

# --- Example Usage ---

bus = SMBus(I2C_BUS)

try:
            
    while True:
        w, x, y, z = read_bno055_quaternion(bus)
        roll, pitch, yaw = quaternion_to_euler(w, x, y, z)
        print(f"Roll: {roll:.2f}, Pitch: {pitch:.2f}, Yaw: {yaw:.2f}")
        time.sleep(0.1) # Read data at 10Hz

except KeyboardInterrupt:
    print("\nProgram terminated.")
finally:
    bus.close()

