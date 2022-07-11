import machine
import utime
from pico_i2c_lcd import I2cLcd
from machine import I2C
from machine import Pin
import dht
from os import statvfs, stat
 
is_test = False
 
sensor = dht.DHT22(Pin(2)) 
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
i2c = I2C(id=0,scl=Pin(1),sda=Pin(0),freq=200000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
logfile = "log.csv"
previous_min = machine.RTC().datetime()[5]
is_mem_full = False

try:
    stat(logfile)
except OSError:
    with open(logfile, "a") as log:
        log.write("temp,hum\n")
    

def write_temp_hum_data(logfile, datetime, temp, hum):
    with open (logfile, "a") as log:
        log.write(str(datetime[0]) + "-"
                  + str(datetime[1]) + "-"
                  + str(datetime[2]) + "-"
                  + str(datetime[4]) + "-"
                  + str(datetime[5]) + ",")
        log.write(str(temp) + ",")
        log.write(str(hum))
        log.write("\n")

def get_free_space():
    return statvfs("/")[3]

while True:
    
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    current_time = machine.RTC().datetime()
    if (is_test or current_time[5] != previous_min) and is_mem_full is False:
        write_temp_hum_data(logfile, current_time, temperature, humidity)
        previous_min = current_time[5]
    if get_free_space() < 10:
        is_mem_full = True
    
    print(temperature, humidity, get_free_space())
    lcd.move_to(0, 0)
    lcd.putstr("Temp: " + str(round(temperature, 1)) + chr(223) + "C  " + (chr(255) if is_mem_full is True else ""))
    lcd.move_to(0, 1)
    lcd.putstr("Hum: " + str(round(humidity, 1)) + "%")
    utime.sleep(1)
    lcd.clear()