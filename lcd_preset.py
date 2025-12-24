from time import sleep
from machine import I2C, Pin
from machine_i2c_lcd import I2cLcd
import uasyncio as asyncio


import button_control
# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

async def sequence(disp, row, blink_freq):
    
    while True:
        
        lcd.move_to(0,row)
        lcd.putstr(" "*16)
        
        for i in range(len(disp)):
            
            lcd.move_to(i,row)
            lcd.putstr(disp[i])
            await asyncio.sleep(blink_freq)
    
async def disp_string(disp,row):
    
    lcd.move_to(0,row)
    lcd.putstr(" "*16)
    lcd.move_to(8-(int(len(disp)/2)),row)
    lcd.putstr(disp)
    
    
def clear():
    lcd.clear()
    
async def blink(disp, row, blink_freq, button_event):
    
    lcd.move_to(0,row)
    lcd.putstr(" "*16)
    
    while True:
        
        lcd.move_to(8-(int(len(disp)/2)),row)
        lcd.putstr(disp)
        await asyncio.sleep(blink_freq)
        lcd.move_to(0,row)
        lcd.putstr(" "*(16))
        await asyncio.sleep(blink_freq)