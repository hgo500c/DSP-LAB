# midterm-3
import pyaudio
import struct
from matplotlib import pyplot as plt
import numpy as np
import math
import wave

wavfile = 'Siren_sound.wav'

wf = wave.open( wavfile, 'rb')

# Read wave file properties
RATE        = wf.getframerate()     # Frame rate (frames/second)
WIDTH       = wf.getsampwidth()     # Number of bytes per sample
LEN         = wf.getnframes()       # Signal length
CHANNELS    = wf.getnchannels()     # Number of channels
DURATION    = LEN/RATE
BLOCKSIZE = 1024
NumBlocks = int( DURATION * RATE / BLOCKSIZE  )

plt.ion()           # Turn on interactive mode so plot gets updated
f0 = 200


DBscale = True

f = RATE/BLOCKSIZE * np.arange(0, BLOCKSIZE)

plt.ion()
plt.figure(1)

plt.subplot(3,1,1)
plt.xlim(0, RATE) 
plt.ylim(0, 150)        # set x-axis limits
# plt.xlim(0, 2000)         # set x-axis limits
plt.xlabel('Decibel Scale')
g1, = plt.plot([], [], color = 'blue')  
g1.set_xdata(f)                         # x-data of plot (frequency)

plt.subplot(3,1,3)
plt.xlim(0, RATE)
plt.ylim(0, 20000)
plt.xlabel('Linear Scale')
g2, = plt.plot([], [], color = 'yellow')
g2.set_xdata(f)

# USE audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)

stream = p.open(
    format    = PA_FORMAT,
    channels  = CHANNELS,
    rate      = RATE,
    input     = False,
    output    = True)

for i in range(0, NumBlocks):
    input_bytes = wf.readframes(BLOCKSIZE)
    input_tuple = struct.unpack('h' * BLOCKSIZE, input_bytes)  # Convert

    X = np.fft.fft(input_tuple)

    g1.set_ydata(20 * np.log10(np.abs(X)))
    g2.set_ydata(np.abs(X))

    plt.setp(g1, color = 'blue')
    plt.setp(g2, color = 'orange')
    plt.pause(0.001)
    stream.write(input_bytes)


plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print('* Finished')
