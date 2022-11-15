# demo_filter_blocks_corrected.py
# Block filtering of a wave file, save the output to a wave file.
# Corrected version.

import pyaudio, wave, struct, math
import numpy as np
import scipy.signal
from matplotlib import pyplot as plt

#wavfile = 'author.wav'
#output_wavfile = 'author_output_blocks_corrected.wav'
WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 16000         # frames per second
BLOCKLEN = 1024     # block length in samples
DURATION = 10       # Duration in seconds
f0 = 400

K = int( DURATION * RATE / BLOCKLEN )   # Number of blocks
#print('Play the wave file %s.' % wavfile)

# Open wave file (should be mono channel)
#wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
#CHANNELS        = wf.getnchannels()     # Number of channels
#RATE            = wf.getframerate()     # Sampling rate (frames/second)
#signal_length   = wf.getnframes()       # Signal length
#WIDTH           = wf.getsampwidth()     # Number of bytes per sample

print('The microphone has %d channel(s).'            % CHANNELS)
print('The frame rate is %d frames/second.'    % RATE)
#print('The file has %d frames.'                % signal_length)
print('There are %d bytes per sample.'         % WIDTH)
output_wavfile = 'demo14cezhang.wav'
output_wf = wave.open(output_wavfile, 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)

# Difference equation coefficients
b0 =  0.008442692929081
b2 = -0.016885385858161
b4 =  0.008442692929081
b = [b0, 0.0, b2, 0.0, b4]

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 =  4.942669993770672
a3 = -3.114402101627517
a4 =  0.757546944478829
a = [1.0, a1, a2, a3, a4]

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH =

x = [0 for i in range(BLOCKLEN)]
y = [0 for i in range(BLOCKLEN)]

plt.ion()
fig = plt.figure(1)
plt.subplot(3,1,1)
g1, = plt.plot(x)
plt.ylim(-MAXVALUE, MAXVALUE)
plt.xlim(0, BLOCKLEN)
plt.xlabel('Time (n)')
plt.title('input')

plt.subplot(3,1,3)
g2, = plt.plot(y)
plt.ylim(-MAXVALUE, MAXVALUE)
plt.xlim(0,BLOCKLEN)
plt.xlabel('Time (n)')
plt.title('output')

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True )

 

# Get first set of frame from wave file
#binary_data = wf.readframes(BLOCKLEN)

ORDER = 4   # filter is fourth order
states = np.zeros(ORDER)

#while len(binary_data) == WIDTH * BLOCKLEN:
for n in range(0, K):

    # convert binary data to numbers
    input_string = stream.read(BLOCKLEN,exception_on_overflow = False)
    input_block = struct.unpack('h' * BLOCKLEN, input_string) 

    # filter
    [output_block, states] = scipy.signal.lfilter(b, a, input_block, zi = states)

    # clipping
    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)

    # convert to integer
    output_block = output_block.astype(int)

    # Convert output value to binary data
    binary_data = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio stream
    stream.write(binary_data)

    # Write binary data to output wave file
    output_wf.writeframes(binary_data)

    # Get next frame from wave file
    #binary_data = wf.readframes(BLOCKLEN)
    g2.set_ydata(output_block)
    g1.set_ydata(input_block)
    plt.setp(g1, color = 'green')
    plt.setp(g2, color = 'blue')
    plt.pause(0.00001)
    plt.draw()

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()

# Close wavefiles
#wf.close()
output_wf.close()