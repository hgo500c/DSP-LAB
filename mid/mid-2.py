# CE ZHANG CZ2146
import pyaudio
import wave
import struct
import math
import tkinter as Tk  
from scipy import signal
import numpy as np
from matplotlib import pyplot as plt 

def fun_quit():
  global CONTINUE
  print('Good bye')
  CONTINUE = False

def fun_triangle():
  global mode
  print('now is triangle_wave')
  mode = True

def fun_sinusoidal():
  global mode
  print('now is sinusoidal_wave')
  mode = False

Fs = 8000    
gain = 0.2 * 2**15
time = 10
BLOCKSIZE = 512
WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 5000     # frames per second
RECORD_SECONDS = 5       # Duration in seconds
DURATION = RECORD_SECONDS
LEN = RATE*RECORD_SECONDS       # Signal length/frame

NumBlocks = int( DURATION * RATE / BLOCKSIZE )
mode =False 
# Define Tkinter root
root = Tk.Tk()
# Define Tk variables
maxf= Tk.DoubleVar()
minf= Tk.DoubleVar()
time= Tk.IntVar()

# Initialize Tk variables
maxf.set(1300)   # f1 : frequency of sinusoid (Hz)
minf.set(700)
time.set(5)

# Define widgets
S_maxf = Tk.Scale(root, label = 'Maximum Frequency', variable = maxf, from_ = 1000, to = 1800)
S_minf = Tk.Scale(root, label = 'Minimum Frequency', variable = minf, from_ = 0, to = 1000)
S_time = Tk.Scale(root, label = 'Time', variable = time, from_ = 3, to = 13)
B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)
B_triangle = Tk.Button(root, text = ' periodic triangle wave', command = fun_triangle)
B_sinusoidal  = Tk.Button(root, text = 'sinusoidal wave', command = fun_sinusoidal)

# Place widgets
B_quit.pack(side = Tk.BOTTOM, fill = Tk.X)
S_maxf.pack(side = Tk.LEFT)
S_minf.pack(side = Tk.LEFT)
S_time.pack(side= Tk.LEFT)

B_triangle.pack(side=Tk.TOP)
B_sinusoidal.pack(side=Tk.TOP)

print('The file has %d channel(s).'            % CHANNELS)
print('The frame rate is %d frames/second.'    % RATE)
print('The file has %d frames.'                % LEN)
print('There are %d bytes per sample.'         % WIDTH)
output_wf = wave.open('midterm_Q2.wav', 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(
    format      = pyaudio.paInt16,
    channels    = 1,
    rate        = RATE,
    input       = False,
    output      = True )

print ('* Playing...')
print('First is sinusoidal_wave')
CONTINUE = True

f0 =3


Fs = 8000
W = 0.3
BUFFER_LEN =  1024          # Set buffer length.
buffer = LEN * [0]   # list of zeros
kr = int(0.5 * BUFFER_LEN)  # read index
kw = 0                      # write index

f = RATE / BLOCKSIZE *np.arange(0, RATE)

plt.ion()
plt.figure(1)

plt.subplot(3,1,1)
plt.xlim(0, RATE) 
plt.ylim(0, 150)        # set x-axis limits
# plt.xlim(0, 2000)         # set x-axis limits
plt.xlabel('Decibel Scale(HZ/s)')
g1, = plt.plot([], [], color = 'blue')  
g1.set_xdata(f)                         # x-data of plot (frequency)

plt.subplot(3,1,3)
plt.xlim(0, RATE)
plt.ylim(0, 1000000)
plt.xlabel('Linear Scale(HZ/s)')
g2, = plt.plot([], [], color = 'yellow')
g2.set_xdata(f)

output_block = [0] * RATE

while CONTINUE:
    root.update()
    freq=(maxf.get()+minf.get())/2*math.sin(2*math.pi/time.get())
    for n in range(0, RATE):
        if(mode):
          om1 = signal.sawtooth(0.5 * math.pi * 0.5 * n) * freq
        else:
          om1 = 2.0 * math.pi * freq * n / RATE
        if om1 > math.pi:
          om1 = om1 - 2.0 * math.pi
        # Convert string to number
        x0 = math.sin(om1)

        # Compute output value - time-varying delay, no direct path
        g=4
        output = gain*(x0+g*buffer[int(kr)])  # use int() for integer

        # Update buffer
        buffer[kw] = x0

        # Increment read index
        kr = kr + 1 + W * math.sin( 2*math.pi * f0 * n / RATE )
            # Note: kr is not integer!

        # Ensure that 0 <= kr < BUFFER_LEN
        if kr >= BUFFER_LEN:
            # End of buffer. Circle back to front.
            kr = kr - BUFFER_LEN

        # Increment write index
        kw = kw + 1
        if kw == BUFFER_LEN:
            # End of buffer. Circle back to front.
            kw = 0
        if output > 2**15-1:
         output = 2**15-1
        elif output < -2**15:
         output = -2**15 
        
        binary_data = struct.pack('h', int(output))
        stream.write(binary_data)
        output_wf.writeframes(binary_data)

        output_block[n]=int(output)
    X = np.fft.fft(output_block)
    g1.set_ydata(20 * np.log10(np.abs(X)))
    g2.set_ydata(np.abs(X))

    plt.setp(g1, color = 'blue')
    plt.setp(g2, color = 'orange')
    plt.pause(0.001)


print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
output_wf.close()

