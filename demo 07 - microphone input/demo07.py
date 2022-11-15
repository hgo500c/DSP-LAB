# mic_filter.py
# Record from microphone, filter the signal,
# and play the output signal on the loud speaker.

import pyaudio
import struct
import math
import wave

from myfunctions import clip16

WIDTH       = 2         # Number of bytes per sample
CHANNELS    = 1         # mono
RATE        = 16000     # Sampling rate (frames/second)
DURATION    = 10         # duration of processing (seconds)
f0          = 400
N = DURATION * RATE     # N : Number of samples to process
def clip16( x ):    
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return (x)
# Difference equation coefficients


# Initialization

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)

print('* Start')

newwf = wave.open('ceezhang.wav', 'w')
newwf.setnchannels(CHANNELS)
newwf.setsampwidth(WIDTH)
newwf.setframerate(RATE)

for n in range(0, N):

    # Get one frame from audio input (microphone)
    #input_bytes = stream.read(1)
    # If you get run-time time input overflow errors, try:
    input_bytes = stream.read(1, exception_on_overflow = False)

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h', input_bytes)

    # Convert one-element tuple to number
    x0 = input_tuple[0]

    # Difference equation
    y0 = math.cos(2*math.pi*f0*n/RATE)*x0

    # Delays
   

    # Compute output value
    output_value = int(clip16(y0))    # Number

    # output_value = int(clip16(x0))   # Bypass filter (listen to input directly)

    # Convert output value to binary data
    output_bytes = struct.pack('h', output_value)  

    # Write binary data to audio stream
    stream.write(output_bytes)
    newwf.writeframesraw(output_bytes)
print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
