from machine import Pin, PWM
from time import sleep
import uasyncio as asyncio
import led_effects
import lcd_preset
import ultrasonic_sensor
import IR_sensor

"""Configures two pins (14 and 15) to control them motors
Pin.OUT means that the raspberry PICO is sending out signals"""
IN1 = Pin(14, Pin.OUT) 
IN2 = Pin(15, Pin.OUT)
' Creates a the control for motor_a'
motor_a = PWM(Pin(13))
'Create motor_b'
IN3 = Pin(16, Pin.OUT)
IN4 = Pin(17, Pin.OUT)

motor_b = PWM(Pin(18))

' Sets a PWM frequency for the motor to 1kHz (kinda a random number thats good for motors'
motor_a.freq(1000)
motor_b.freq(1000)

def motors(speed1, speed2):
    # allows negative numbers to make the motor turn backwards
    if speed1 < 0:
        IN1.value(1)
        IN2.value(0)
    elif speed1 > 0:
        IN1.value(0)
        IN2.value(1)
    if speed2 < 0:
        IN3.value(0)
        IN4.value(1)
    elif speed2 > 0:
        IN3.value(1)
        IN4.value(0)
    
    motor_a.duty_u16(int(abs(speed2) * 65535 / 100))
    motor_b.duty_u16(int(abs(speed1) * 65535 / 100))
    
async def maze_pathfinding(np):
    base_speed = 55
    correction_factor = 4
    
    forward_led = asyncio.create_task(led_effects.seq_effect(np,0.1, 0, 8))
    forward_disp = asyncio.create_task(lcd_preset.disp_string("ONWARDS!",0))
    forward_seq = asyncio.create_task(lcd_preset.sequence("Pathfinding.....", 1, .2))
    
    while True:
        
        current_front = IR_sensor.IR_read()
        current_left = ultrasonic_sensor.get_distance(6,7)
        current_right = ultrasonic_sensor.get_distance(26,27)
        
        
        
        error = current_left - current_right
        correction = error * correction_factor
            
        left_speed = base_speed - correction
        right_speed = base_speed + correction
           
        left_speed = max(20, min(100, left_speed))
        right_speed = max(20, min(100, right_speed))
            
            
            
        motors(int(left_speed) , int(right_speed))
            
        await asyncio.sleep (.01)

async def preset_path():
    
    preset_disp_row_1 = asyncio.create_task(lcd_preset.disp_string("Ive been on this", 0))
    preset_disp_row_2 = asyncio.create_task(lcd_preset.disp_string("path before", 1))
    
    motors(65,70)
    await asyncio.sleep(3.167)
    motors(-70,75)
    await asyncio.sleep(2.167)
    motors(65,70)
    await asyncio.sleep(1.867)
    motors(67,-67)
    await asyncio.sleep(1.067)
    motors(65,70)
    await asyncio.sleep(2.267)
    motors(0,0)
    
    preset_disp_row_1.cancel()
    preset_disp_row_2.cancel()
    
            
