import machine
import utime
from pico_i2c_lcd import I2cLcd
from machine import I2C
from machine import Pin
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
i2c = I2C(id=0,scl=Pin(1),sda=Pin(0),freq=200000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
while True:
    reading = sensor_temp.read_u16() * conversion_factor
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)
    lcd.move_to(0, 0)
    lcd.putstr("Temperature:")
    lcd.move_to(0, 1)
    lcd.putstr(str(round(temperature, 1)) + chr(223) + "C")
    utime.sleep(1)
    lcd.clear()