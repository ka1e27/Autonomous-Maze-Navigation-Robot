from machine import Pin
from event_list import button_event
import uasyncio as asyncio




def is_pressed():
    return button.value() == 0

async def monitor_button(button):
    """Continuously monitor button and set event when pressed"""
    
    while True:
        
        if button.value() == 0:
            
            button_event.set()  # Signal button was pressed
            await asyncio.sleep(0.3)  # Debounce
            button_event.clear()  # Reset for next press
            
        await asyncio.sleep(0.05)
