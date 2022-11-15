# AM_from_microphone.py
# Record audio and play it with amplitude modulation. 
# This implementation:
#   uses blocking, 
#   corrects for block-to-block angle mismatch,
#   assumes mono channel
# Original by Gerald Schuller, 2013

from matplotlib import pyplot
import pyaudio
import struct
import math
from matplotlib import pyplot as plt

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return(x)

# f0 = 0      # Normal audio
f0 = 400    # Modulation frequency (Hz)

BLOCKLEN = 1024      # Number of frames per block
WIDTH = 2           # Number of bytes per signal value
CHANNELS = 1        # mono
RATE = 32000        # Frame rate (frames/second)
RECORD_SECONDS = 30
DURATION = 10
K = int( DURATION * RATE / BLOCKLEN )   # Number of blocks

x = [0 for i in range(BLOCKLEN)]
y = [0 for i in range(BLOCKLEN)]
output = [0 for i in range(BLOCKLEN)]
pyplot.ion()           # Turn on interactive mode
pyplot.figure(1)
n = range(0, BLOCKLEN)
pyplot.xlim(0, BLOCKLEN)
pyplot.xlabel('Time (n)')
[g1] = pyplot.plot([], [])
[g2] = pyplot.plot([], [])
g1.set_label('output')
g2.set_label('input')
g1.set_xdata(n)
g2.set_xdata(n)
pyplot.ylim(-32000, 32000)
pyplot.show()

p = pyaudio.PyAudio()
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)


output_block = BLOCKLEN * [0]

# Initialize phase
om = 2*math.pi*f0/RATE
theta = 0

# Number of blocks to run for
num_blocks = int(RATE / BLOCKLEN * RECORD_SECONDS)

print('* Recording for %.3f seconds' % RECORD_SECONDS)

# Start loop
for i in range(K):

    # Get frames from audio input stream
    # input_bytes = stream.read(BLOCKLEN)       # BLOCKLEN = number of frames read
    input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)   # BLOCKLEN = number of frames read

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)
   
    # Go through block
    for n in range(0, BLOCKLEN):
        # No processing:
        # output_block[n] = input_tuple[n]  
        # OR
        # Amplitude modulation:
        theta = theta + om
        output_block[n] = int( input_tuple[n] * math.cos(theta) )
        output_block[n] = int(clip16(output_block[n]))
    # keep theta betwen -pi and pi
   
    while theta > math.pi:
        theta = theta - 2*math.pi

    g1.set_ydata(output_block)
    g2.set_ydata(input_tuple)
    pyplot.setp(g1, color = 'orange',label ='ouput')
    pyplot.setp(g2, color = 'black',label ='intput')
    pyplot.pause(0.0001)
   
    # Convert values to binary data
    output_bytes = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio output stream
    stream.write(output_bytes)
stream.stop_stream()
stream.close()
p.terminate()


pyplot.ioff()           # Turn off interactive mode
pyplot.show()           # Keep plot showing at end of program
pyplot.close()
print('* Finished')