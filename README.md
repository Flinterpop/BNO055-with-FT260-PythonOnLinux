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
Then we query the data at Page 0. The first few bytes are the vendor and device ID(a0 fb 32 0f etc).

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


#### Python App listing (euler.py)

```python
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


