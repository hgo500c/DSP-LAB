import pyaudio
import wave
import struct
from random import normalvariate
import numpy as np

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return(x)

WIDTH    = 2
RATE     = 8000
CHANNELS = 1
Duration = 2 

MAXVALUE = 2**15-1 

output_wavfile = 'cezhangdemo20wav'
output_wf = wave.open(output_wavfile, 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)


# Karplus-Strong paramters
K = 0.95
N = 60

a = list(np.zeros(N-1))
a.insert(0,1)
a.append(-K/2)
a.append(-K/2)
b = 1

gain = 10000   

BUFFER_LEN = N+1   
buffer = [ 0 for i in range(BUFFER_LEN) ]    


p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(
    format      = PA_FORMAT,
    channels    = CHANNELS,
    rate        = RATE,
    input       = False,
    output      = True )

k = 0      

print("Start")
x = [0] * (Duration * RATE + N)
for i in range (N):
    x[i] = np.random.randn() * 10000
for i in range(Duration* RATE + N):
    
    binput = b * x[i]
    if(k == N):
        output_value = binput - a[N] * buffer[0] - a[N+1] * buffer[k]
    else:
        output_value = binput- a[N] * buffer[k+1] - a[N+1] * buffer[k]

    buffer[k] = output_value
    k = k + 1
    if k >= BUFFER_LEN:
        k = 0
    
    output_string = struct.pack('h', int(clip16(output_value)))

    stream.write(output_string)    

    output_wf.writeframes(output_string)

print("...Finished")

stream.stop_stream()
stream.close()
output_wf.close()
p.terminate()