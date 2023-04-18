import machine
import utime
import os
from machine import Pin, SPI
import sdcard

# Función para parpadear el LED
def parpadear_led(led, veces, duracion):
    for _ in range(veces):
        led.value(1)
        utime.sleep(duracion)
        led.value(0)
        utime.sleep(duracion)

# Configura el LED de estado
led = Pin(25, Pin.OUT)

# Configura SPI para el módulo SD
spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs = Pin(5, Pin.OUT)
sd = sdcard.SDCard(spi, cs)
os.mount(sd, "/sd")

# Copia main.py desde la tarjeta SD a la Raspberry Pi Pico
with open("/sd/main.py", "r") as f_sd, open("/main.py", "w") as f_pico:
    f_pico.write(f_sd.read())

# Parpadea el LED dos veces para indicar que el programa ha sido cargado
parpadear_led(led, 2, 0.5)

# Borra el contenido de la tarjeta SD
os.remove("/sd/main.py")

# Desmonta la tarjeta SD y reinicia la Raspberry Pi Pico para ejecutar el programa cargado
os.umount("/sd")
machine.reset()
