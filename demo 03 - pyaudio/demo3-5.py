
# filter_16.py
# 
# Implement the second-order recursive difference equation
# y(n) = x(n) - a1 y(n-1) - a2 y(n-2)
# 
# 16 bit/sample

from math import cos, pi 
import pyaudio
import struct


# Fs : Sampling frequency (samples/second)
Fs = 8000
# Also try other values of 'Fs'. What happens? Why?
#Fs = 20000
#Fs = 30000

T = 1       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play
f1=800.0
om1 = 2.0 * pi * f1 / Fs
r = 0.998
# Difference equation coefficients
a0 = 1
a1 = -2 * r * cos(om1)
a2 = r**2
b0 = 1
b1 = -r * cos(om1)
b2 = 0

x1 = 0.0
y1 = 0.0
y2 = 0.0
gain = 10000.0
# Also try other values of 'gain'. What is the effect?
# gain = 1500.0

# Create an audio object and open an audio stream for output
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,  
                channels = 1, 
                rate = Fs,
                input = False, 
                output = True)

# paInt16 is 16 bits/sample

# Run difference equation
for n in range(0, N):

    # Use impulse as input signal
    if n == 0:
        x0 = 1.0
    else:
        x0 = 0.0

    # Difference equation
    y0 = x0 - a1 * y1 - a2 * y2 + b1 * x1

    # Delays
    x1 = x0
    y2 = y1
    y1 = y0

    # Output
    output_value = gain * y0
    if output_value > 2**15-1:
        output_value = 2**15-1
    elif output_value < -2**15:
        output_value = -2**15    # make sure they are in this range
    output_string = struct.pack('h', int(output_value))   # 'h' for 16 bits
    stream.write(output_string)
print ( pyaudio . paInt16 )
WIDTH = 2
print ( pyaudio . get_format_from_width ( WIDTH ) )
print("* Finished *")

stream.stop_stream()
stream.close()
p.terminate()
