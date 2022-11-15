
from math import cos, pi 
import pyaudio, struct
import tkinter as Tk   	
from math import sin, pi, cos
from struct import pack
import wave

def fun_quit():
  global CONTINUE
  print('Good bye')
  CONTINUE = False

def fun_triangle():
  global mode
  print('triangle_wave')
  mode = True

def fun_sinusoidal():
  global mode
  print('sinusoidal_wave')
  mode = False

Fs = 8000    
gain = 0.2 * 2**15
time = 10

# Define Tkinter root
root = Tk.Tk()

# Define Tk variables
maxf= Tk.DoubleVar()
minf= Tk.DoubleVar()
time= Tk.IntVar()

# Initialize Tk variables
maxf.set(1500)   # f1 : frequency of sinusoid (Hz)
minf.set(500)
time.set(5)

# Define widgets
S_maxf = Tk.Scale(root, label = 'Maximum Frequency', variable = maxf, from_ = 1300, to = 2600)
S_minf = Tk.Scale(root, label = 'Minimum Frequency', variable = minf, from_ = 0, to = 1300)
S_time = Tk.Scale(root, label = 'Time', variable = time, from_ = 0, to = 10)
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

# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
  format = pyaudio.paInt16,  
  channels = 1, 
  rate = Fs,
  input = False, 
  output = True)            
  # specify low frames_per_buffer to reduce latency

CONTINUE = True
BUFFER_LEN=1024
kr = int(0.5 * BUFFER_LEN)  # read index
kw = 0                      # write index
W = 3.0
RATE = Fs
WIDTH = 2  # Bytes per sample
CHANNELS = 1  # Number of channels
f1 =2000
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)

wf = wave.open('midterm_Q1.wav', 'w')
wf.setnchannels(CHANNELS)
wf.setsampwidth(WIDTH)
wf.setframerate(Fs)

print('* Start')
freq =(maxf.get()+minf.get())/2
f0 =3
A = 2**15 - 1.0       # amplitude
gain = 0.2 * 2 ** 15

roundtime = 10
NumB = int(roundtime * RATE ) 
buffer =  NumB* [0]

while CONTINUE:
  root.update()
  freq =(maxf.get()+minf.get())/2 
  for i in range(0, NumB):
    om1 = 2.0 * pi * f1 * i / RATE
    if om1 > pi:
            om1 = om1 - 2.0 * pi
    x0 = sin(om1)

    g=7
    y0 = gain*(x0+g*buffer[int(kr)]) 
    buffer[kw] = x0
    kr = kr + 1 + W * sin( 2 * pi * f0 * i / RATE )

    if kr >= BUFFER_LEN:
        # End of buffer. Circle back to front.
        kr = kr - BUFFER_LEN

    # Increment write index    
    kw = kw + 1
    if kw == BUFFER_LEN:
        kw = 0

    if y0 > 2**15-1:
        y0 = 2**15-1
    elif y0 < -2**15:
        y0 = -2**15    # make sure they are in this range
  output_bytes = struct.pack('h', int(y0))
  stream.write(output_bytes)
  wf.writeframes(output_bytes)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
