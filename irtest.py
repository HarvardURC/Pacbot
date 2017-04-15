#!/usr/bin/python

import io
import fcntl
#import smbus

address = 0x29
#bus = smbus.SMBus(1)
IOCTL_I2C_SLAVE = 0x0703

fr = io.open("/dev/i2c-1", "rb", buffering=0)
fw = io.open("/dev/i2c-1", "wb", buffering=0)

fcntl.ioctl(fr, IOCTL_I2C_SLAVE, 0x29)
fcntl.ioctl(fw, IOCTL_I2C_SLAVE, 0x29)

def write(data):
    fw.write(data)

def read(num):
    return fr.read(num)

def close():
    fw.close()
    fr.close()

def read_reg8(reg):
    write(bytearray([(reg >> 8) & 0xFF, reg & 0xFF]))
    v = read(1)
    #print type(v), ord(v), hex(ord(v)), v
    return ord(v)

def write_reg8(reg, data):
    write(bytearray([(reg >> 8) & 0xFF, reg & 0xFF, data & 0xFF]))

def start_range():
    write_reg8(0x018, 0x01)

def poll_range():
    # check the status
    status = read_reg8(0x04f)
    range_status = status & 0x07

    # wait for new measurement ready status
    while range_status != 0x04:
        status = read_reg8(0x04f)
        range_status = status & 0x07

def clear_interrupts():
    write_reg8(0x015, 0x07)

def initialize():
    setup = read_reg8(0x016)
    if setup == 1:
        write_reg8(0x0207, 0x01)
        write_reg8(0x0208, 0x01)
        write_reg8(0x0096, 0x00)
        write_reg8(0x0097, 0xfd)
        write_reg8(0x00e3, 0x00)
        write_reg8(0x00e4, 0x04)
        write_reg8(0x00e5, 0x02)
        write_reg8(0x00e6, 0x01)
        write_reg8(0x00e7, 0x03)
        write_reg8(0x00f5, 0x02)
        write_reg8(0x00d9, 0x05)
        write_reg8(0x00db, 0xce)
        write_reg8(0x00dc, 0x03)
        write_reg8(0x00dd, 0xf8)
        write_reg8(0x009f, 0x00)
        write_reg8(0x00a3, 0x3c)
        write_reg8(0x00b7, 0x00)
        write_reg8(0x00bb, 0x3c)
        write_reg8(0x00b2, 0x09)
        write_reg8(0x00ca, 0x09)
        write_reg8(0x0198, 0x01)
        write_reg8(0x01b0, 0x17)
        write_reg8(0x01ad, 0x00)
        write_reg8(0x00ff, 0x05)
        write_reg8(0x0100, 0x05)
        write_reg8(0x0199, 0x05)
        write_reg8(0x01a6, 0x1b)
        write_reg8(0x01ac, 0x3e)
        write_reg8(0x01a7, 0x1f)
        write_reg8(0x0030, 0x00)

        # Recommended : Public registers - See data sheet for more detail
        
        write_reg8(0x0011, 0x10) # Enables polling for 'New Sample ready' when measurement completes
        write_reg8(0x010a, 0x30) # Set the averaging sample period (compromise between lower noise and increased execution time)
        write_reg8(0x003f, 0x46) # Sets the light and dark gain (upper nibble). Dark gain should not be changed.
        write_reg8(0x0031, 0xFF) # sets the # of range measurements after which auto calibration of system is performed
        write_reg8(0x0040, 0x63) # Set ALS integration time to 100ms
        write_reg8(0x002e, 0x01) # perform a single temperature calibratio of the ranging sensor
        write_reg8(0x001b, 0x09) # Set default ranging inter-measurement period to 100ms
        write_reg8(0x003e, 0x31) # Set default ALS inter-measurement period to 500ms
        write_reg8(0x0014, 0x24) # Configures interrupt on 'New Sample Ready threshold event' 

        write_reg8(0x016, 0x00)

def get_distance():
    while 1:
        start_range()
        poll_range()
        rng = read_reg8(0x062)
        clear_interrupts()
        print (rng)
    return rng

initialize()
get_distance()
