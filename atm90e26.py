import mraa
from atm90e26_registers import *

import time
import struct
import binascii
__write__ = False
__read__ = True

class ATM90E26_SPI:

    '''       
    spi - hardware or software SPI implementation
    cs - Chip Select pin
    '''

    def __init__(self, spi):
        self.spi = spi
        self.init_config()
    '''
    rw - True - read, False - write
    address - register to operate
    val - value to write (if any)
    '''

    def comm_atm90(self, RW, address, val = 0xFFFF):
        # switch MSB and LSB of value
        read_buf = bytearray(1)
        write_buf = bytearray(3)
        # Set read write flag
        address |= RW << 7

        if(RW): # 1 as MSB marks a read
            struct.pack_into('>B',read_buf,0,address)
            ''' Must wait 4 us for data to become valid '''
            time.sleep(10e-6)
            # Write address
            read_res = self.spi.write(read_buf)
            return read_res
        else: #0 as MSB and 32 clock cycles marks a write
            struct.pack_into('>B',write_buf,0,address)
            struct.pack_into('>H',write_buf,2,val)
            self.spi.writeByte(write_buf)# write all the bytes
    
    def init_config(self):
        pass
    
    def get_rms_voltages(self):
        VA = 0
        VB = 0
        VC = 0

        return (VA,VB,VC)

    def get_meter_status(self):
        sys_status = self.comm_atm90(1, SysStatus)
        meter_status = self.comm_atm90(1, EnStatus)

        return (sys_status, meter_status)


if __name__=="__main__":
    spi = mraa.Spi(0)
    spi.mode(3)
    spi.frequency(2000000)
    spi.lsbmode(False)
    ss=mraa.Gpio(9)
    ss.dir(mraa.DIR_OUT)
    ss.write(1)
      
    eic1 = ATM90E26_SPI(spi)
    for i in range(10):
        print("Meter Status:",eic1.get_meter_status())
        print("Voltages:",eic1.get_rms_voltages())
