import uasyncio as asyncio
from machine import Pin, PWM
import neopixel
from time import sleep
from event_list import distance_event, button_event

import button_control
import led_effects
import lcd_preset
import ultrasonic_sensor
import motor_control
import buzzer
import potentiometer
import IR_sensor

n = 8
p = 2

led = Pin(15, Pin.OUT)

np = neopixel.NeoPixel(Pin(2),8)

button_start = Pin(12,Pin. IN, Pin.PULL_UP)

button_end = Pin(12,Pin. IN, Pin.PULL_UP)

end_pot_value = 0          
    
async def pot_check():
    
    global end_pot_value
    
    while True:
        
        pot_value = potentiometer.PotDisp(2)
        pot_value = int(float(pot_value))
        if pot_value < 34:
            
            await lcd_preset.disp_string("Forward", 0)
            
        elif 33 < pot_value < 67:
            
            await lcd_preset.disp_string("Preset Path", 0)
            
        else:
            
            await lcd_preset.disp_string("Maze", 0)
            
        end_pot_value = pot_value
        await lcd_preset.disp_string("Potentiometer:"+ str(pot_value),1)
        await asyncio.sleep(.1)
        
async def wait_for_start():
    
    
    button1 = asyncio.create_task(button_control.monitor_button(button_start))
    
    led_start = asyncio.create_task(led_effects.rainbow_fill(np,0, 8, .02))
    
    pot_checker = asyncio.create_task(pot_check())
        
    await button_event.wait()
    
    print("Button pressed - cancelling tasks...")

    #Stop blinking and leds
    pot_checker.cancel()
    button1.cancel()
    led_start.cancel()
    button_event.clear()
    lcd_preset.clear()
    
async def forward():
    
    forward_disp_row_1 = asyncio.create_task(lcd_preset.disp_string("Full Steam", 0))
    forward_disp_row_2 = asyncio.create_task(lcd_preset.disp_string("Ahead!!", 1))
    
    motor_control.motors(65,70)
    await asyncio.sleep(.5)
    motor_control.motors(40,40)
    await asyncio.sleep(6.2)
    motor_control.motors(65,70)
    await asyncio.sleep(.67)
    motor_control.motors(0,0)
    button_event.set()
    
    forward_disp_row_1.cancel()
    forward_disp_row_2.cancel()
    

async def main():
    
    await wait_for_start()
    
    await asyncio.sleep(1)

    asyncio.create_task(button_control.monitor_button(button_end))
    
    if end_pot_value < 34:
        
        forward_straight = asyncio.create_task(forward())
        
    elif 33 < end_pot_value < 67:
        
        preset_path = asyncio.create_task(motor_control.preset_path())
        
    else:
        
        maze = asyncio.create_task(motor_control.maze_pathfinding(np))
    
    await button_event.wait()
    print("Button Pressed")
                                      
    if end_pot_value < 34:
        
        forward_straight.cancel()
        
    elif end_pot_value > 33 and end_pot_value < 67:
        
        preset_path.cancel()
        
    else:
        
        maze.cancel()  

    button_event.clear()
    lcd_preset.clear()
    motor_control.motors(0,0)
    led_effects.stop(np,0,8)
    
asyncio.run(main())