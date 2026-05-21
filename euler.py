import time
from smbus2 import SMBus

# I2C Configuration
I2C_BUS = 9
BNO055_ADDR = 0x28
MODE_NDOF = 0x08 # Fusion mode with 9 degrees of freedom

# Register definitions
REG_OP_MODE = 0x3D
REG_EULER_X_LSB = 0x1A

# Initialize SMBus
bus = SMBus(I2C_BUS)

def configure_bno():
    # Set the BNO055 to NDOF (Fusion) Mode
    bus.write_byte_data(BNO055_ADDR, REG_OP_MODE, MODE_NDOF)
    time.sleep(0.5) # Wait for mode switch

def read_euler():
    # Read 6 bytes starting from EULER_X_LSB
    # Format: [Heading LSB, Heading MSB, Roll LSB, Roll MSB, Pitch LSB, Pitch MSB]
    data = bus.read_i2c_block_data(BNO055_ADDR, REG_EULER_X_LSB, 6)
    
    # Combine LSB and MSB (16-bit signed integers)
    # The BNO055 scales Euler angles by 16 (i.e., 1 degree = 16 LSB)
    def get_val(lsb, msb):
        val = (msb << 8) | lsb
        if val > 32767:
            val -= 65536
        return val / 16.0

    heading = get_val(data[0], data[1])
    roll = get_val(data[2], data[3])
    pitch = get_val(data[4], data[5])
    
    return heading, roll, pitch

try:
    configure_bno()
    while True:
        heading, roll, pitch = read_euler()
        print(f"Heading: {heading:.2f} | Roll: {roll:.2f} | Pitch: {pitch:.2f}")
        time.sleep(0.1)

except KeyboardInterrupt:
    bus.close()
    print("Bus closed.")
