# Ce Zhang CZ2146@nyu.edu

import pyaudio
import wave
import struct
import math
import tkinter as Tk  
from scipy import signal

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
BLOCKSIZE = 1024
WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 5000        # frames per second
RECORD_SECONDS = 5       # Duration in seconds
DURATION = RECORD_SECONDS
signal_length = RATE*RECORD_SECONDS       # Signal length/frame
LEN = signal_length
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
print('The file has %d frames.'                % signal_length)
print('There are %d bytes per sample.'         % WIDTH)
output_wf = wave.open('midterm_Q1.wav', 'w')      # wave file
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

freq0 =3

Fs = 8000
W = 0.2
BUFFER_LEN =  1024          # Set buffer length.
buffer = LEN * [0]   # list of zeros
kr = int(0.5 * BUFFER_LEN)  # read index
kw = 0                      # write index

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

        # Compute output value - time-varying delay
        g=4
        output = gain*(x0+g*buffer[int(kr)])  

        # Update buffer
        buffer[kw] = x0

        # Increment read index
        kr = kr + 1 + W * math.sin( 2*math.pi * freq0 * n / RATE )

        # Ensure that 0 <= kr < BUFFER_LEN
        if kr >= BUFFER_LEN:
            kr = kr - BUFFER_LEN

        # Increment write index
        kw = kw + 1
        if kw == BUFFER_LEN:
            # End of buffer. Circle back to front.
            kw = 0

        if output > 2**15-1:
          output = 2**15-1
        elif output < -2**15:
          output = -2**15  # output should be in this range
        binary_data = struct.pack('h', int(output))
        stream.write(binary_data)
        output_wf.writeframes(binary_data)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
output_wf.close()

