# for raspberry pi

from machine import Pin, I2C
import utime

class mpu6050:
    def __init__(self, pscl, psda, pfreq, addr=0x68):
        self.i2c = I2C(0, scl=Pin(pscl), sda=Pin(psda), freq=pfreq)
        
    def byte2int(self, byte1, byte2):
        if not byte1 & 0x80:
            return byte1 << 8 | byte2
        return -(((byte1^255) << 8) | (byte2^255)+1)
    
    def get_datas(self):
        r = self.i2c.readfrom(0x68, 14)
        xa = self.byte2int(r[0], r[1]) / 16384.0
        ya = self.byte2int(r[2], r[3]) / 16384.0
        za = self.byte2int(r[4], r[5]) / 16384.0
        tm = self.byte2int(r[6], r[7])
        xg = self.byte2int(r[8], r[9]) / 131.0
        yg = self.byte2int(r[10], r[11]) / 131.0
        zg = self.byte2int(r[12], r[13]) / 131.0
        
        return {"acc":{"x": xa, "y": ya, "z": za}, "tmp": tm, "gyr":{"x": xg, "y": yg, "z": zg}}
        
        
if __name__ == '__main__':
    from machine import Pin, I2C
    import bytecalc as bc
    
#    i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=1000000)
    gyro = mpu6050(17, 16, 100)
    while True:
        dt = gyro.get_datas()
        print(type(utime.time()))
        print(utime.time())
        print(dt)
        utime.sleep(2)
    
