from time import sleep
import uasyncio as asyncio
"""np[1] = (255, 165, 0) #Orange
np[2] = (255, 255, 0) #Yellow
np[3] = (0, 255, 25)#Green
np[4] = (0, 0, 255)#Blue
np[5] = (128, 0, 128) #Purple
np[6] = (255, 0, 255) #Magenta
np[7] = (255, 255, 255) #White
p=2
while p >1:"""
 #Sends this information to the LED strip
async def pulse_effect(np, led1, led2):
    
    while True:
        
        for i in range (0,256):
            
            for n in range(led1,led2):
                
                np[n]=(i, 0 , 0)
                await asyncio.sleep(.0001)
                np.write()
                
        for i in range (0,256):
            
            for n in range(led1, led2):
                
                np[n]=(255-i, 0, 0)
                await asyncio.sleep(.0001)
                np.write()
                
def stop(np, led1, led2):
    
    for i in range(led1, led2):
        
        np[i] = (0,0,0)
        
    np.write()
    
async def seq_effect(np, time,led1, led2):
    
    while True:
        
        for i in range(led1, led2):
            
            np[i] = (255, 0, 0)
            np.write()
            await asyncio.sleep(time)
            np[i] = (0, 0, 0)
            np.write()
            
async def rainbow_fill(np, led1, led2, time):
    """All LEDs show same color, smoothly cycling through rainbow"""
    
    def wheel(pos):
        
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)
    
    pos = 0
    
    while True:
        
        color = wheel(pos)
        for i in range(led1, led2):
            np[i] = color
        np.write()
        pos = (pos + 1) % 256
        await asyncio.sleep(time)
    
    
    
    