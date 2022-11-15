# plot_wire_gain_ver2.py
#
# plots both input and output signals

import pyaudio
import struct
from matplotlib import pyplot

WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 8000         # frames per second
BLOCKLEN = 512     # block length in samples
DURATION = 10       # Duration in seconds

K = int( DURATION * RATE / BLOCKLEN )   # Number of blocks

print('Block length: %d' % BLOCKLEN)
print('Number of blocks to read: %d' % K)
print('Duration of block in milliseconds: %.1f' % (1000.0 * BLOCKLEN/RATE))

# Set up plotting...

pyplot.ion()           # Turn on interactive mode
pyplot.figure(1)
# [g1] = pyplot.plot([], [], 'blue')  # Create empty line

output_block = BLOCKLEN * [0]       # initialize output block

# [g1] = pyplot.plot([], [], label = 'Input Signal')
# [g2] = pyplot.plot([], [], label = 'Output signal')

[g1] = pyplot.plot(range(BLOCKLEN), output_block, 'blue', label = 'Input Signal')
[g2] = pyplot.plot(range(BLOCKLEN), output_block, 'red', label = 'Output signal')

n = range(0, BLOCKLEN)
pyplot.xlim(0, BLOCKLEN)         # set x-axis limits
pyplot.xlabel('Time (n)')
g1.set_xdata(n)                   # x-data of plot (discrete-time)
g2.set_xdata(n)                   # x-data of plot (discrete-time)
pyplot.legend()

# --- Time axis in units of milliseconds ---
# t = [n*1000/float(RATE) for n in range(BLOCKLEN)]
# pyplot.xlim(0, 1000.0 * BLOCKLEN/RATE)         # set x-axis limits
# pyplot.xlabel('Time (msec)')
# g1.set_xdata(t)                   # x-data of plot (time)

pyplot.ylim(-10000, 10000)        # set y-axis limits

# Open the audio stream

p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(
    format = PA_FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = 256)      # low latency so that plot and output audio are synchronized


output_block = BLOCKLEN * [0]       # initialize output block

# Read microphone, plot audio signal, play output on loud speaker

for i in range(K):

    # Read audio input stream
    input_bytes = stream.read(BLOCKLEN)

    # In case of run-time errors, try using instead:
    # input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)

    signal_block = struct.unpack('h' * BLOCKLEN, input_bytes)  # Convert

    for i in range(BLOCKLEN):
        output_block[i] = int(0.3 * signal_block[i])

    g1.set_ydata(signal_block)   # Update y-data of plot
    g2.set_ydata(output_block)
    pyplot.pause(0.0001)

    # Convert output value to binary data
    output_bytes = struct.pack('h' * BLOCKLEN, *output_block)  

    # Write binary data to audio stream
    stream.write(output_bytes)


stream.stop_stream()
stream.close()
p.terminate()

pyplot.ioff()           # Turn off interactive mode
pyplot.show()           # Keep plot showing at end of program
pyplot.close()

print('* Finished')
