import machine
import utime
from machine import Pin, I2C, SPI
import sdcard
import os
import SHT31
import ds3231

# Configura I2C para RTC y SHT31
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

# Configura SPI para el módulo SD
spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs = Pin(5, Pin.OUT)
sd = sdcard.SDCard(spi, cs)
os.mount(sd, "/sd")

# Inicializa el sensor SHT31
sensor = SHT31.SHT31(i2c)

# Inicializa el RTC
rtc = ds3231.DS3231(i2c)

# Configura el LED de estado
led = Pin(25, Pin.OUT)

def guardar_datos(rtc, temperatura, humedad):
    fecha_hora = rtc.datetime()
    fecha = "{}/{}/{}".format(fecha_hora[0], fecha_hora[1], fecha_hora[2])
    hora = "{:02d}:{:02d}:{:02d}".format(fecha_hora[4], fecha_hora[5], fecha_hora[6])
    datos = "{}, {}, T: {:.2f}°C, H: {:.2f}%\n".format(fecha, hora, temperatura, humedad)

    with open("/sd/datalog.txt", "a") as f:
        f.write(datos)

# Bucle principal
while True:
    temperatura, humedad = sensor.measurements()
    guardar_datos(rtc, temperatura, humedad)
    led.value(1)
    utime.sleep(0.1)
    led.value(0)
    utime.sleep(5)
