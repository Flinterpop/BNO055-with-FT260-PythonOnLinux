import time
from smbus2 import SMBus

# BNO055 I2C Address (default is 0x28, or 0x29 if ADR pin is pulled high)
DEVICE_ADDRESS = 0x28
I2C_BUS_NUMBER = 9 #find with lsusb and lok for FT device

# Register Addresses
BNO055_PAGE_ID_ADDR = 0x07
BNO055_OPR_MODE_ADDR = 0x3D
BNO055_SYS_TRIGGER_ADDR = 0x3F
BNO055_UNIT_SEL_ADDR = 0x3B

# Euler Angle Registers (LSB first)
EULER_H_LSB_ADDR = 0x1A
EULER_H_MSB_ADDR = 0x1B
EULER_R_LSB_ADDR = 0x1C
EULER_R_MSB_ADDR = 0x1D
EULER_P_LSB_ADDR = 0x1E
EULER_P_MSB_ADDR = 0x1F

# Operation Modes
OPERATION_MODE_NDOF = 0x0C  # Nine Degrees of Freedom Fusion Mode

def init_bno055(bus):
    # Select Page 0
    bus.write_byte_data(DEVICE_ADDRESS, BNO055_PAGE_ID_ADDR, 0x00)
    
    # Set to CONFIG Mode to allow configuration changes
    bus.write_byte_data(DEVICE_ADDRESS, BNO055_OPR_MODE_ADDR, 0x00)
    time.sleep(0.02)
    
    # Reset the system
    bus.write_byte_data(DEVICE_ADDRESS, BNO055_SYS_TRIGGER_ADDR, 0x20)
    time.sleep(0.8) # Wait for device to reboot
    
    # 2. Select Degrees for Angular Output
    # Writing 0x00 sets: Euler=Degrees, Gyro=Degrees/s, Accel=m/s^2
    bus.write_byte_data(DEVICE_ADDRESS, BNO055_UNIT_SEL_ADDR, 0x00)
    time.sleep(0.8) # Wait for device to reboot

    # Set to NDOF Operation Mode
    bus.write_byte_data(DEVICE_ADDRESS, BNO055_OPR_MODE_ADDR, OPERATION_MODE_NDOF)
    time.sleep(0.01)


    

def read_euler_angles(bus):
    # Read 6 bytes starting from EULER_H_LSB_ADDR
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, EULER_H_LSB_ADDR, 6)
    
    # Combine LSB and MSB (each angle is 16-bit signed integer)
    raw_heading = data[0] | (data[1] << 8)
    raw_roll = data[2] | (data[3] << 8)
    raw_pitch = data[4] | (data[5] << 8)
    
    # Convert to Degrees (BNO055 outputs 16 LSB per degree)
    heading = raw_heading / 16.0
    roll = raw_roll / 16.0
    pitch = raw_pitch / 16.0

    print("User %02X %02X" % (data[2] , data[1]))

    # Format: Data is 16-bit signed, 1 degree = 16 LSB
    #heading = (data[1] << 8 | data[0]) / 16.0
    #pitch = (data[3] << 8 | data[2]) / 16.0
    #roll = (data[5] << 8 | data[4]) / 16.0
    
    return heading, roll, pitch

# Main Execution
try:
    with SMBus(I2C_BUS_NUMBER) as bus:
        init_bno055(bus)
        print("BNO055 Initialized. Reading orientation...")
        
        while True:
            heading, roll, pitch = read_euler_angles(bus)
            print(f"Heading: {heading:.2f} | Roll: {roll:.2f} | Pitch: {pitch:.2f}")
            time.sleep(0.1)

except Exception as e:
    print(f"Error communicating with BNO055: {e}")
