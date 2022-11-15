# play_vibrato_interpolation.py
# Reads a specified wave file (mono) and plays it with a vibrato effect.
# (Sinusoidally time-varying delay)
# Uses linear interpolation

import pyaudio
import wave
import struct
import math


#wavfile = 'decay_cosine_mono.wav'
wavfile = 'author.wav'
# wavfile = 'cosine_200_hz.wav'

print('Play the wave file: %s.' % wavfile)

BLOCKSIZE = 64
# Open wave file
wf = wave.open( wavfile, 'rb')

# Read wave file properties
RATE        = wf.getframerate()     # Frame rate (frames/second)
WIDTH       = wf.getsampwidth()     # Number of bytes per sample
LEN         = wf.getnframes()       # Signal length
CHANNELS    = wf.getnchannels()     # Number of channels

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)
output_block = [0 for n in range(0, BLOCKSIZE)]
# Vibrato parameters
f0 = 2
W = 0.2   # W = 0 for no effect

# f0 = 2; W = 0.2

# OR
# f0 = 2
# ratio = 2.06
# W = (ratio - 1.0) / (2 * math.pi * f0 )
# print(W)

# Buffer to store past signal values. Initialize to zero.
BUFFER_LEN =  1024          # Set buffer length.
buffer = [0.0 for i in range(BUFFER_LEN)]  # list of zeros

# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * BUFFER_LEN)  # write index (initialize to middle of buffer)

print('The buffer is %d samples long.' % BUFFER_LEN)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = False,
                output      = True )
output_all = bytes([]) 
print ('* Playing...')

# Loop through wave file 
for n in range(0, LEN):

    # Get sample from wave file
	input_bytes = wf.readframes(BLOCKSIZE)

    # Convert string to number
	input_blocksize = struct.unpack('h'*BLOCKSIZE, input_bytes)
    
	for k in range(0, BLOCKSIZE):
    # Get previous and next buffer values (since kr is fractional)
		kr_prev = int(math.floor(kr))
		frac = kr - kr_prev 
		kr_next = kr_prev + 1
		if kr_next == BUFFER_LEN:
			kr_next = kr_next - buffer_LEN
		output_block[k] = (1-frac) * buffer[kr_prev] + frac * buffer[kr_next]

        	# Update buffer
		buffer[kw] = input_blocksize[k]

       	# Increment read index
		kr == kr + 1 + W * math.sin( 2 * math.pi * f0 * (n*BLOCKSIZE+k) / RATE )
       	 # Note: kr is fractional (not integer!)

        	# Ensure that 0 <= kr < BUFFER_LEN
		if kr >= BUFFER_LEN:
			kr = 0   
		kw = kw + 1
		if kw == BUFFER_LEN:
			kw = 0

    # Clip and convert output value to binary data
	output_bytes = struct.pack('h'*BLOCKSIZE, *output_block)

    # Write output to audio stream
	stream.write(output_bytes)
	output_all = output_all + output_bytes
print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
wf.close()
