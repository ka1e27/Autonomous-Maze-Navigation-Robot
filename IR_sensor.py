from machine import Pin


sensor = Pin(22, Pin.IN)

def IR_read():
    return sensor.value()