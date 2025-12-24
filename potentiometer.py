from machine import ADC
from time import sleep



def ReadPotentiometer(pin):
    # Set up potentiometer pin
    pot_pin = pin
    pot = ADC(pot_pin)

    # Read potentiometer value
    adc_value = pot.read_u16()

    # Convert into a voltage
    volt = (3.3/65535)*adc_value

    percentPot = ScalePercent(volt)

    return percentPot

# Convert voltage into a percentage of 3.3 V


def ScalePercent(volt):
    percent = (volt/3.3)*100
    return int(percent)

def PotDisp(pin):
        potvalue = ReadPotentiometer(pin)
        return potvalue
