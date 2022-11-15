# writehw
# 
# cz2146 

# 8 bits per sample

from struct import pack
from math import sin, pi
import wave

Fs = 8000

# Write a mono wave file 

wf = wave.open('hwwrite8bit.wav', 'w')		# wf : wave file
wf.setnchannels(1)			# one channel (mono)
wf.setsampwidth(1)			# four bytes per sample (8 bits per sample)
wf.setframerate(Fs)			# samples per second
A = 2**7 - 1.0 			# amplitude
f = 261.6					# frequency in Hz (note A3)
N = int(0.5*Fs)				# half-second in samples

for n in range(0, N):	    # half-second loop 
	x = A * sin(2*pi*f/Fs*n)
	byte_string = pack('B', int(x+128)) 
	# 'i' stands for 'integer' (32 bits)
	wf.writeframesraw(byte_string)
wf.close()

