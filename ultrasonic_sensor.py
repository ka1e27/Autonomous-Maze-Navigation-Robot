from machine import Pin, time_pulse_us
from time import sleep
import uasyncio as asyncio

def get_distance(trig_pin, echo_pin):
    'TRIG sends a signal out from the third pin'
    TRIG = Pin(trig_pin, Pin.OUT)
    'ECHO takes a signal from the second pin'
    ECHO = Pin(echo_pin, Pin.IN)
    TRIG.low() # turns off signal
    sleep(.02)
    TRIG.high() # turns signal on
    sleep(.00001)  # 10 microseconds
    TRIG.low() # turns signal off
    """waits for pin to be at HIGH level(1) then measures how long it stays HIGH
    waits a max of 30ms or 30000 micro seconds and it will timeout"""
    duration = time_pulse_us(ECHO, 1 , 30000)
    
    if duration < 0:
        return 100
    
    distance = (duration / 2 ) / 29.1
    
    return distance

async def dist_loop(trig_pin, echo_pin):
    
    while True:
        
        print(get_distance(trig_pin, echo_pin))
        await asyncio.sleep(1)