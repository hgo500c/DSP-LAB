# plot_microphone_input_spectrum.py

"""
Using Pyaudio, get audio input and plot real-time FFT of blocks.
Ivan Selesnick, October 2015
Based on program by Gerald Schuller
"""

import pyaudio
import struct
from matplotlib import pyplot as plt
import numpy as np
import math

plt.ion()           # Turn on interactive mode so plot gets updated
f0 = 200
WIDTH     = 2         # bytes per sample
CHANNELS  = 1         # mono
RATE      = 8000     # Sampling rate (samples/second)
BLOCKSIZE = 1024      # length of block (samples)
DURATION  = 8        # Duration (seconds)

NumBlocks = int( DURATION * RATE / BLOCKSIZE )

print('BLOCKSIZE =', BLOCKSIZE)
print('NumBlocks =', NumBlocks)
print('Running for ', DURATION, 'seconds...')

DBscale = True
# DBscale = True

f = RATE/BLOCKSIZE * np.arange(0, BLOCKSIZE)

# Initialize plot window:
plt.ion()
plt.figure(1)
#if DBscale:
    #plt.ylim(0, 150)
#else:
    #plt.ylim(0, 20*RATE)

plt.subplot(3,1,1)
# Frequency axis (Hz)
plt.xlim(0, 0.5*RATE) 
plt.ylim(0, 150)        # set x-axis limits
# plt.xlim(0, 2000)         # set x-axis limits
plt.xlabel('Frequency (Hz)')
g1, = plt.plot([], [], color = 'blue')  
g1.set_xdata(f)                         # x-data of plot (frequency)

plt.subplot(3,1,3)
plt.xlim(0, 0.5*RATE)
plt.ylim(0, 150)
plt.xlabel('Frequency (Hz)')
g2, = plt.plot([], [], color = 'yellow')
g2.set_xdata(f)




# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)

stream = p.open(
    format    = PA_FORMAT,
    channels  = CHANNELS,
    rate      = RATE,
    input     = True,
    output    = True)

output_block = [0 for n in range(0, BLOCKSIZE)]

NumBlocks = int(math.floor(NumBlocks))

om = 2*math.pi*f0/RATE
theta = 0

for i in range(0, NumBlocks):
    input_bytes = stream.read(BLOCKSIZE,exception_on_overflow = False)                    # Read audio input stream
    input_tuple = struct.unpack('h' * BLOCKSIZE, input_bytes)  # Convert
   # X = np.fft.fft(input_tuple)

    for n in range(0, BLOCKSIZE):
         theta = theta + om
         output_block[n] = int( input_tuple[n] * math.cos(theta) )
    while theta > math.pi:
        theta = theta - 2*math.pi
    X = np.fft.fft(input_tuple)
    Y = np.fft.fft(output_block)

    #g1.set_ydata(20*np.log10(abs(X)))
    #g2.set_ydata(20*np.log10(abs(Y)))
    #Update y-data of plot
    if DBscale:
        g1.set_ydata(20 * np.log10(np.abs(X)))
        g2.set_ydata(20 * np.log10(np.abs(Y)))
    else:
        g1.set_ydata(np.abs(X))
        g2.set_ydata(np.abs(Y))
    plt.setp(g1, color = 'blue')
    plt.setp(g2, color = 'orange')
    plt.pause(0.001)
    plt.draw()

    output_byte = struct.pack('h' * BLOCKSIZE, *output_block)
    stream.write(output_byte)
    # plt.draw()

plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print('* Finished')
