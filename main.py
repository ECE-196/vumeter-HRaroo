import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
from time import sleep

# Initialize microphone input and status LED pin
mic_input = AnalogIn(board.IO1)

status_indicator = DigitalInOut(board.IO17)
status_indicator.direction = Direction.OUTPUT

# Define the list of LED pins to control
led_pins_list = [
    board.IO21,
    board.IO26,  # type: ignore
    board.IO47,
    board.IO33,
    board.IO34,
    board.IO48,
    board.IO35,
    board.IO36,
    board.IO37,
    board.IO38,
    board.IO39,
]


led_outputs = []
for pin in led_pins_list:
    led = DigitalInOut(pin)
    led.direction = Direction.OUTPUT
    led_outputs.append(led)

# Function to adjust LED brightness based on sound level
def adjust_leds_by_volume(sound_level, led_list):
    baseline = 20000
    scaling_factor = 1750
    
    # Normalize sound level to a brightness level
    normalized_brightness = max(0, (sound_level - baseline) / scaling_factor)
    
    print(f"Normalized brightness: {normalized_brightness}")
    
    # Control each LED based on brightness
    for i, led in enumerate(led_list):
        if normalized_brightness > i:
            led.value = True
        else:
            led.value = False

# Function to filter volume changes smoothly
def smooth_volume_transition(current_volume, last_volume):
    increase_speed = 1.0
    decrease_speed = 0.1

    if current_volume > last_volume:
        # Quick rise in volume
        return last_volume + (current_volume - last_volume) * increase_speed
    else:
        # Slow decrease in volume
        return last_volume - (last_volume - current_volume) * decrease_speed

# Main loop
filtered_volume = 0

while True:
    # Read current sound level
    current_volume = mic_input.value
    print(f"Current volume: {current_volume}")
  
    filtered_volume = smooth_volume_transition(current_volume, filtered_volume)
    print(f"Filtered volume: {filtered_volume}")
    
  
    adjust_leds_by_volume(filtered_volume, led_outputs)
    
    # Small delay 
    sleep(0.1)
