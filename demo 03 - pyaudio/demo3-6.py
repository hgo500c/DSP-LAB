# filter_16_T
# Like filter_16 with prescribed duration

# 16 bit/sample

from math import cos, pi
import pyaudio
import struct

# Fs : Sampling frequency (samples/second)
Fs = 8000
# Also try Fs = 16000 and Fs = 32000

T = 1       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

# Pole location
f1 = 1000 
f2 = 50
om1 = 2 * pi * float(f1) / Fs
om2 = 2 * pi * float(f2) / Fs
r = 0.998

Ta = 0.9    # Ta : Time for envelope to decay to 1% (in seconds)
# Try different values of Ta like 0.5, 0.2, 1.5
r = 0.01**(1.0/(Ta*Fs))

print('Fs = %f' % Fs)
print('r = %f' % r)

# Difference equation coefficients
a01 = 1
a11 = -2 * r * cos(om1)
a21 = r**2
b01 = 1
b11 = 0
b21 = 0

a02 = 1
a12 = -2 * r * cos(om2)
a22 = r**2
b02 = 1
b12 = 0
b22 = 0
# Initialization
y11 = 0.0
y21 = 0.0
y12 = 0.0
y22 = 0.0
gain = 10000.0

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,  
                channels = 2, 
                rate = Fs,
                input = False, 
                output = True)


for n in range(0, N):
    # Use impulse as input signal
	if n == 0:
		x0 = 1.0
	else:
		x0 = 0.0
	y01 = x0 - a11 * y11 - a21 * y21  #channel
	y02 = x0 - a12 * y12 - a22 * y22  #channel
	#delays
	y21 = y11
	y11 = y01
	y22 = y12
	y12 = y02

	output_value_1 = gain * y01
	if output_value_1 > 2**15-1:
		output_value_1 = 2**15-1
	elif output_value_1 < -2**15:
		output_value_1 = -2**15

	output_value_2 = gain * y02
	if output_value_2 > 2**15-1:
		output_value_2 = 2**15-1
	elif output_value_2 < -2**15:
		output_value_2 = -2**15

	output_string = struct.pack('h', int(output_value_1))
	output_string += struct.pack('h', int(output_value_2))
	stream.write(output_string)


print("* Finished *")

stream.stop_stream()
stream.close()
p.terminate()
