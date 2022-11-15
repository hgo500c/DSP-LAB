# echo_via_circular_buffer.py
# Reads a specified wave file (mono) and plays it with an echo.
# This implementation uses a circular buffer.

import pyaudio
import wave
import struct
from myfunctions import clip16

#wavfile = 'author.wav'
#print('Play the wave file %s.' % wavfile)

# Open the wave file
#wf = wave.open( wavfile, 'rb')

# Read the wave file properties
#num_channels    = wf.getnchannels()     # Number of channels
#RATE            = wf.getframerate()     # Sampling rate (frames/second)
#signal_length   = wf.getnframes()       # Signal length
#width           = wf.getsampwidth()     # Number of bytes per sample
RATE = 16000
DURATION    = 6    
N = RATE*DURATION   # delay in samples
#print('The file has %d channel(s).'            % num_channels)
#print('The frame rate is %d frames/second.'    % RATE)
#print('The file has %d frames.'                % signal_length)
#print('There are %d bytes per sample.'         % width)

# Set parameters of delay system
# y(n) = b0 x(n) + G x(n-N)
b0 = 1.0            # direct-path gain
G = 0.8             # feed-forward gain
delay_sec = 0.05    # delay in seconds, 50 milliseconds   Try delay_sec = 0.02
Ndelay = int( RATE * delay_sec )   # delay in samples

print('The delay of %.3f seconds is %d samples.' %  (delay_sec, N))

# Buffer to store past signal values. Initialize to zero.
BUFFER_LEN = Ndelay              # length of buffer
buffer = BUFFER_LEN * [0]   # list of zeros

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = True,
                output      = True )

# Get first frame
# input_bytes = wf.readframes(1)

# Initialize buffer index (circular index)
k = 0

print('* Start')

newwf = wave.open('ceezhangdemo8.wav', 'w')
newwf.setnchannels(1)
newwf.setsampwidth(2)
newwf.setframerate(RATE)

for n in range(0, N):
#while len(input_bytes) > 0:
    input_byte = stream.read(1, exception_on_overflow = False)
    # Convert binary data to number
    #x0, = struct.unpack('h', input_bytes)
    input=struct.unpack('h', input_byte)
    x0 = input[0]
    # Compute output value
    # y(n) = b0 x(n) + G x(n-N)
    y0 = b0 * x0 + G * buffer[k]

    # Update buffer
    buffer[k] = x0

    # Increment buffer index
    k = k + 1
    if k >= BUFFER_LEN:
        # The index has reached the end of the buffer. Circle the index back to the front.
        k = 0

    # Clip and convert output value to binary data
    output_bytes = struct.pack('h', int(clip16(y0)))

    # Write output value to audio stream
    stream.write(output_bytes)
    newwf.writeframesraw(output_bytes)
    # Get next frame
    #input_bytes = wf.readframes(1)     

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
#wf.close()