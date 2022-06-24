import machine
import utime
from pico_i2c_lcd import I2cLcd
from machine import I2C
from machine import Pin
import dht
 
sensor = dht.DHT22(Pin(2)) 
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
i2c = I2C(id=0,scl=Pin(1),sda=Pin(0),freq=200000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
while True:
    
    
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    
    print(temperature, humidity)
    lcd.move_to(0, 0)
    lcd.putstr("Temp: " + str(round(temperature, 1)) + chr(223) + "C")
    lcd.move_to(0, 1)
    lcd.putstr("Hum: " + str(round(humidity, 1)) + "%")
    utime.sleep(1)
    lcd.clear()