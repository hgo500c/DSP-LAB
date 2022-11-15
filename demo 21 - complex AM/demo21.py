

import pyaudio
import wave
import struct
import numpy as np
from scipy import signal
from math import pi


WIDTH     = 2         # bytes per sample
CHANNELS  = 1         # mono
RATE      = 20000    # Sampling rate (samples/second)
BLOCKLEN = 1024      # length of block (samples)
DURATION  = 5        # Duration (seconds)
FRAMERATE = 8
order = 7
BLOCKSIZE = 64
num = RATE*DURATION/FRAMERATE
[b_lpf, a_lpf] = signal.ellip(order, 0.2, 50, 0.48)

Imagine = 1j
x = [Imagine ** i for i in range(order + 1)]
a = [0 * l for l in range(0, order + 1)]
b = [0 * l for l in range(0, order + 1)]

for i in range(order + 1):
    a[i] = a_lpf[i] * x[i]
    b[i] = b_lpf[i] * x[i]


print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
#print('The file has %d frames.'             % LEN)
#print('The file has %d bytes per sample.'   % WIDTH)
#output_block = [0 for n in range(0, BLOCKSIZE)]

filterstates = np.zeros(order)
# Vibrato parameters
f0 = 2
W = 0.2   # W = 0 for no effect

# Buffer to store past signal values. Initialize to zero.
BUFFER_LEN =  1024          # Set buffer length.
buffer = [0.0 for i in range(BUFFER_LEN)]  # list of zeros

# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * BUFFER_LEN)  

#print('The buffer is %d samples long.' % BUFFER_LEN)
print('It will play 5 sec')
# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = CHANNELS,
                rate        = RATE,
                input       = True,
                output      = True )
output_all = bytes([]) 
print ('* Playing...')
wavfile = 'CeZhang.wav'
wf = wave.open( wavfile, 'w')

# Read wave file properties
wf.setframerate(RATE)     # Frame rate (frames/second)
wf.setsampwidth(WIDTH)     # Number of bytes per sample
#wf.setnframes(RATE)       # Signal length
wf.setnchannels(1)     # Number of channels
# Loop through wave file 

for n in range(int(num)):

    # Get sample from wave file
    input_bytes = stream.read(FRAMERATE,exception_on_overflow=False)

    # Convert string to number
    input_blocksize = struct.unpack('h'*FRAMERATE, input_bytes)

    output_block, states = signal.lfilter(b, a, input_blocksize, zi=filterstates)
    
    freq =400

    g = [1j for i in range(0, order + 1)]
    t = [0 for i in range(0, FRAMERATE)]
    
    for i in range(FRAMERATE):
       c = np.e ** (Imagine * 2 * pi * freq * (n * 8 + i) / RATE)
       g[i] = (output_block[i] * c).real
       t[i] = int(g[i].real)
       output = struct.pack('h', t[i])
       wf.writeframesraw(output)
       stream.write(output)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
wf.close()
