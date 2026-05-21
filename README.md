# BNO055-with-FT260-PythonOnLinux

Similar to other project in this repo () but this time using the same hardware but running on Ubuntu running on a NUC.



## Commands to query the hardware on Linux with I2C Interface
#### List all USB devices
```bash
lsusb
```

#### List USB devices from FTDI
```bash
lsusb | grep 0403:6030
```

### Can use I2C tools to query I2C devices so install i2C tools
```bash
sudo apt install i2c-tools
```

```bash
i2cdetect -l
```

```bash
i2cdump 6 0x28
```
### Example of ```lsusb``` and ```i2cget``` with BNO055
Shows that the BNO055 is Bus 1 Device 9 on this specific PC.
Thjen we query the data at Page 0. The first few bytes are the vendor and device ID. (a0 fb 32 0f etc).

```bash
(.venv) brad@brad-NUC10i3FNK:~/source_py$ lsusb
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 003: ID 3434:d028 Keychron Keychron Ultra-Link 8K
Bus 001 Device 005: ID 8087:0026 Intel Corp. AX201 Bluetooth
Bus 001 Device 008: ID 17ef:608d Lenovo Optical Mouse
Bus 001 Device 009: ID 0403:6030 Future Technology Devices International, Ltd FT260
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
(.venv) brad@brad-NUC10i3FNK:~/source_py$
(.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo i2cdump -y 9 0x28
No size specified (using byte-data access)
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f    0123456789abcdef
00: a0 fb 32 0f 11 03 15 00 00 00 00 00 00 00 00 00    ??2????.........
10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
30: 00 00 00 00 00 00 0f 00 00 01 05 80 ff 10 00 00    ......?..???.?..
40: 00 24 00 00 40 00 00 00 00 00 00 00 40 00 00 00    .$..@.......@...
50: 00 00 00 00 40 00 00 00 00 00 00 00 00 00 00 00    ....@...........
60: 00 00 00 00 00 00 00 00 00 e0 01 00 00 00 00 00    .........??.....
70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
80: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
90: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
a0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
b0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
c0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
d0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
e0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
f0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
(.venv) brad@brad-NUC10i3FNK:~/source_py$ 
```


#### Returns entire 0 page of data from Device 9 bus address 0x28 
```bash
sudo i2cdump -y 9 0x28
```


### The App
#### We will use smbus2 package in the python scripts
```bash
pip3 install smbus2
```

#### Run python app (named bno055test.py) with sudo, I2C_BUS_NUMBER inside ap is 9 to match the Device number from lsusb
```bash
(.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo python3 bno055test.py 
.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo python3 bno055test.py 
BNO055 Initialized. Reading orientation...
User 00 00
Heading: 0.00 | Roll: 0.00 | Pitch: 0.00
User 00 00
Heading: 0.00 | Roll: 0.00 | Pitch: 0.00
User ED 16
Heading: 360.00 | Roll: 4094.81 | Pitch: 0.06
```


#### Python Ap listing
```python 
import time
from smbus2 import SMBus

# BNO055 I2C Address (default is 0x28, or 0x29 if ADR pin is pulled high)
DEVICE_ADDRESS = 0x28
I2C_BUS_NUMBER = 9 # Usually 1 for Raspberry Pi

# Register Addresses
BNO055_PAGE_ID_ADDR = 0x07# BNO055 IMU on Linux with I2C Interface

```lsusb```

```bash
lsusb | grep 0403:6030
```

```bash
sudo apt install i2c-tools
```




```bash
pip3 install smbus2
```

```bash
i2cdetect -l
```

```bash
i2cdump 6 0x28
```

#### Returns entire 0$^{th}$ page of data from Device 9 bus address 0x28 
```bash
sudo i2cdump -y 9 0x28
```
### Example of ```lsusb``` and ```i2cget``` with BNO055

```bash
(.venv) brad@brad-NUC10i3FNK:~/source_py$ lsusb
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 003: ID 3434:d028 Keychron Keychron Ultra-Link 8K
Bus 001 Device 005: ID 8087:0026 Intel Corp. AX201 Bluetooth
Bus 001 Device 008: ID 17ef:608d Lenovo Optical Mouse
Bus 001 Device 009: ID 0403:6030 Future Technology Devices International, Ltd FT260
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
(.venv) brad@brad-NUC10i3FNK:~/source_py$
(.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo i2cdump -y 9 0x28
No size specified (using byte-data access)
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f    0123456789abcdef
00: a0 fb 32 0f 11 03 15 00 00 00 00 00 00 00 00 00    ??2????.........
10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
30: 00 00 00 00 00 00 0f 00 00 01 05 80 ff 10 00 00    ......?..???.?..
40: 00 24 00 00 40 00 00 00 00 00 00 00 40 00 00 00    .$..@.......@...
50: 00 00 00 00 40 00 00 00 00 00 00 00 00 00 00 00    ....@...........
60: 00 00 00 00 00 00 00 00 00 e0 01 00 00 00 00 00    .........??.....
70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
80: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
90: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
a0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
b0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
c0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
d0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
e0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
f0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
(.venv) brad@brad-NUC10i3FNK:~/source_py$ 
```

#### Run python app a sudo, I2C_BUS_NUMBER inside ap is 9 to match the Device number from lsusb
```bash
(.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo python3 bno055test.py 
.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo python3 bno055test.py 
BNO055 Initialized. Reading orientation...
User 00 00
Heading: 0.00 | Roll: 0.00 | Pitch: 0.00
User 00 00
Heading: 0.00 | Roll: 0.00 | Pitch: 0.00
User ED 16
Heading: 360.00 | Roll: 4094.81 | Pitch: 0.06


```



### The App
```python
import time
from smbus2 import SMBus

# BNO055 I2C Address (default is 0x28, or 0x29 if ADR pin is pulled high)
DEVICE_ADDRESS = 0x28
I2C_BUS_NUMBER = 9 # Usually 1 for Raspberry Pi

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
    raw_pitch = data[4] | (data[5] << 8)# BNO055 IMU on Linux with I2C Interface

```lsusb```

```bash
lsusb | grep 0403:6030
```

```bash
sudo apt install i2c-tools
```




```bash
pip3 install smbus2
```

```bash
i2cdetect -l
```

```bash
i2cdump 6 0x28
```

#### Returns entire 0$^{th}$ page of data from Device 9 bus address 0x28 
```bash
sudo i2cdump -y 9 0x28
```
### Example of ```lsusb``` and ```i2cget``` with BNO055

```bash
(.venv) brad@brad-NUC10i3FNK:~/source_py$ lsusb
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 003: ID 3434:d028 Keychron Keychron Ultra-Link 8K
Bus 001 Device 005: ID 8087:0026 Intel Corp. AX201 Bluetooth
Bus 001 Device 008: ID 17ef:608d Lenovo Optical Mouse
Bus 001 Device 009: ID 0403:6030 Future Technology Devices International, Ltd FT260
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
(.venv) brad@brad-NUC10i3FNK:~/source_py$
(.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo i2cdump -y 9 0x28
No size specified (using byte-data access)
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f    0123456789abcdef
00: a0 fb 32 0f 11 03 15 00 00 00 00 00 00 00 00 00    ??2????.........
10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
30: 00 00 00 00 00 00 0f 00 00 01 05 80 ff 10 00 00    ......?..???.?..
40: 00 24 00 00 40 00 00 00 00 00 00 00 40 00 00 00    .$..@.......@...
50: 00 00 00 00 40 00 00 00 00 00 00 00 00 00 00 00    ....@...........
60: 00 00 00 00 00 00 00 00 00 e0 01 00 00 00 00 00    .........??.....
70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
80: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
90: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
a0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
b0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
c0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
d0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
e0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
f0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
(.venv) brad@brad-NUC10i3FNK:~/source_py$ 
```

#### Run python app a sudo, I2C_BUS_NUMBER inside ap is 9 to match the Device number from lsusb
```bash
(.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo python3 bno055test.py 
.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo python3 bno055test.py 
BNO055 Initialized. Reading orientation...
User 00 00
Heading: 0.00 | Roll: 0.00 | Pitch: 0.00
User 00 00
Heading: 0.00 | Roll: 0.00 | Pitch: 0.00
User ED 16
Heading: 360.00 | Roll: 4094.81 | Pitch: 0.06


```



### The App
```python
import time
from smbus2 import SMBus

# BNO055 I2C Address (default is 0x28, or 0x29 if ADR pin is pulled high)
DEVICE_ADDRESS = 0x28
I2C_BUS_NUMBER = 9 # Usually 1 for Raspberry Pi

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
# BNO055 IMU on Linux with I2C Interface

```lsusb```

```bash
lsusb | grep 0403:6030
```

```bash
sudo apt install i2c-tools
```




```bash
pip3 install smbus2
```

```bash
i2cdetect -l
```

```bash
i2cdump 6 0x28
```

#### Returns entire 0$^{th}$ page of data from Device 9 bus address 0x28 
```bash
sudo i2cdump -y 9 0x28
```
### Example of ```lsusb``` and ```i2cget``` with BNO055

```bash
(.venv) brad@brad-NUC10i3FNK:~/source_py$ lsusb
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 003: ID 3434:d028 Keychron Keychron Ultra-Link 8K
Bus 001 Device 005: ID 8087:0026 Intel Corp. AX201 Bluetooth
Bus 001 Device 008: ID 17ef:608d Lenovo Optical Mouse
Bus 001 Device 009: ID 0403:6030 Future Technology Devices International, Ltd FT260
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
(.venv) brad@brad-NUC10i3FNK:~/source_py$
(.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo i2cdump -y 9 0x28
No size specified (using byte-data access)
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f    0123456789abcdef
00: a0 fb 32 0f 11 03 15 00 00 00 00 00 00 00 00 00    ??2????.........
10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
30: 00 00 00 00 00 00 0f 00 00 01 05 80 ff 10 00 00    ......?..???.?..
40: 00 24 00 00 40 00 00 00 00 00 00 00 40 00 00 00    .$..@.......@...
50: 00 00 00 00 40 00 00 00 00 00 00 00 00 00 00 00    ....@...........
60: 00 00 00 00 00 00 00 00 00 e0 01 00 00 00 00 00    .........??.....
70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
80: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
90: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
a0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
b0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
c0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
d0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
e0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
f0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
(.venv) brad@brad-NUC10i3FNK:~/source_py$ 
```

#### Run python app a sudo, I2C_BUS_NUMBER inside ap is 9 to match the Device number from lsusb
```bash
(.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo python3 bno055test.py 
.venv) brad@brad-NUC10i3FNK:~/source_py$ sudo python3 bno055test.py 
BNO055 Initialized. Reading orientation...
User 00 00
Heading: 0.00 | Roll: 0.00 | Pitch: 0.00
User 00 00
Heading: 0.00 | Roll: 0.00 | Pitch: 0.00
User ED 16
Heading: 360.00 | Roll: 4094.81 | Pitch: 0.06


```



### The App
```python
import time
from smbus2 import SMBus

# BNO055 I2C Address (default is 0x28, or 0x29 if ADR pin is pulled high)
DEVICE_ADDRESS = 0x28
I2C_BUS_NUMBER = 9 # Usually 1 for Raspberry Pi

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

```
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

```
    
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

```
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

```
