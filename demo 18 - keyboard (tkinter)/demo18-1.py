# keyboard_demo_06.py
# Play a note using a second-order difference equation
# when the user presses a key on the keyboard.

import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk    

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 2      # Decay time (seconds)
f1 = 440    # Frequency (Hz)

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
ORDER = 2   # filter order
f = [0] * 12
om = [0] * 12
a = [0,0,0] * 12
b = [0] * 12
for i in range(12): 
    f[i] = 2 ** (i/12) * f1
    om[i] = 2.0 * pi * float(f[i])/RATE
    a[i] = [1, -2*r*cos(om[i]), r**2]
    b[i] = [r*sin(om[i])]

states1 = np.zeros(ORDER)
states2 = np.zeros(ORDER)
states3 = np.zeros(ORDER)
states4 = np.zeros(ORDER)
states5 = np.zeros(ORDER)
states6 = np.zeros(ORDER)
states7 = np.zeros(ORDER)
states8 = np.zeros(ORDER)
states9 = np.zeros(ORDER)
states10 = np.zeros(ORDER)
states11 = np.zeros(ORDER)
states12 = np.zeros(ORDER)

x1 = np.zeros(BLOCKLEN)
x2 = np.zeros(BLOCKLEN)
x3 = np.zeros(BLOCKLEN)
x4 = np.zeros(BLOCKLEN)
x5 = np.zeros(BLOCKLEN)
x6 = np.zeros(BLOCKLEN)
x7 = np.zeros(BLOCKLEN)
x8 = np.zeros(BLOCKLEN)
x9 = np.zeros(BLOCKLEN)
x10 = np.zeros(BLOCKLEN)
x11 = np.zeros(BLOCKLEN)
x12 = np.zeros(BLOCKLEN)


# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
        format      = PA_FORMAT,
        channels    = CHANNELS,
        rate        = RATE,
        input       = False,
        output      = True,
        frames_per_buffer = 128)
# specify low frames_per_buffer to reduce latency

CONTINUE = True
KEYPRESS1 = False
KEYPRESS2 = False
KEYPRESS3 = False
KEYPRESS4 = False
KEYPRESS5 = False
KEYPRESS6 = False
KEYPRESS7 = False
KEYPRESS8 = False
KEYPRESS9 = False
KEYPRESS10 = False
KEYPRESS11 = False
KEYPRESS12 = False
x  = np.zeros(BLOCKLEN)
def my_function(event):
    global CONTINUE
    global KEYPRESS1
    global KEYPRESS2
    global KEYPRESS3
    global KEYPRESS4
    global KEYPRESS5
    global KEYPRESS6
    global KEYPRESS7
    global KEYPRESS8
    global KEYPRESS9
    global KEYPRESS10
    global KEYPRESS11
    global KEYPRESS12
    print('You pressed ' + event.char)
    e = event.char
    if e == 'q':
        print('Good bye')
        CONTINUE = False
    if e == '1':
     KEYPRESS1 = True
    if e == '2':
     KEYPRESS2 = True
    if e == '3':
     KEYPRESS3 = True
    if e == '4':
     KEYPRESS4 = True
    if e == '5':
     KEYPRESS5 = True
    if e == '6':
     KEYPRESS6 = True
    if e == '7':
     KEYPRESS7 = True
    if e == '8':
     KEYPRESS8 = True
    if e == '9':
     KEYPRESS9= True
    if e == '0':
     KEYPRESS10 = True
    if e == '-':
     KEYPRESS11 = True
    if e == '=':
     KEYPRESS12 = True
    # f2 = (2**(k/12))*f1  
    # om2 = 2.0 * pi * float(f2)/RATE 
    # a1 = [1, -2*r*cos(om2), r**2]
    # b1 = [r*sin(om2)]    
root = Tk.Tk()
root.bind("<Key>", my_function)

print('Press keys 1234567890-= for sound.')
print('Press "q" to quit')



CONTINUE = True
while CONTINUE:
    root.update()
    if KEYPRESS1 and CONTINUE:
        x1[0] = 10000.0

    if KEYPRESS2 and CONTINUE:
        x2[0] = 10000.0

    if KEYPRESS3 and CONTINUE:
        x3[0] = 10000.0

    if KEYPRESS4 and CONTINUE:
        x4[0] = 10000.0

    if KEYPRESS5 and CONTINUE:
        x5[0] = 10000.0

    if KEYPRESS6 and CONTINUE:
        x6[0] = 10000.0

    if KEYPRESS7 and CONTINUE:
        x7[0] = 10000.0
       
    if KEYPRESS8 and CONTINUE:
        x8[0] = 10000.0
       
    if KEYPRESS9 and CONTINUE:
        x9[0] = 10000.0

    if KEYPRESS10 and CONTINUE:
        x10[0] = 10000.0
           
    if KEYPRESS11 and CONTINUE:
        x11[0] = 10000.0

    if KEYPRESS12 and CONTINUE:
        x12[0] = 10000.0

    [y1, states1] = signal.lfilter(b[0], a[0], x1, zi = states1)
    [y2, states2] = signal.lfilter(b[1], a[1], x2, zi = states2)
    [y3, states3] = signal.lfilter(b[2], a[2], x3, zi = states3)
    [y4, states4] = signal.lfilter(b[3], a[3], x4, zi = states4)
    [y5, states5] = signal.lfilter(b[4], a[4], x5, zi = states5)
    [y6, states6] = signal.lfilter(b[5], a[5], x6, zi = states6)
    [y7, states7] = signal.lfilter(b[6], a[6], x7, zi = states7)
    [y8, states8] = signal.lfilter(b[7], a[7], x8, zi = states8)
    [y9, states9] = signal.lfilter(b[8], a[8], x9, zi = states9)
    [y10, states10] = signal.lfilter(b[9], a[9], x10, zi = states10)
    [y11, states11] = signal.lfilter(b[10], a[10], x11, zi = states11)
    [y12, states12] = signal.lfilter(b[11], a[11], x12, zi = states12)
    x1[0]= 0.0
    x2[0]= 0.0
    x3[0]= 0.0 
    x4[0] = 0.0 
    x5[0] = 0.0         
    x6[0] = 0.0 
    x7[0]= 0.0 
    x8[0] = 0.0 
    x9[0] = 0.0 
    x10[0] = 0.0 
    x11[0] = 0.0 
    x12[0] = 0.0 

    KEYPRESS1 = False
    KEYPRESS2 = False
    KEYPRESS3 = False
    KEYPRESS4 = False
    KEYPRESS5 = False
    KEYPRESS6 = False
    KEYPRESS7 = False
    KEYPRESS8 = False
    KEYPRESS9 = False
    KEYPRESS10 = False
    KEYPRESS11 = False
    KEYPRESS12 = False
   

    y1 = np.clip(y1.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    y2 = np.clip(y2.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    y3 = np.clip(y3.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    y4 = np.clip(y4.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    y5 = np.clip(y5.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    y6 = np.clip(y6.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    y7 = np.clip(y7.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    y8 = np.clip(y8.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    y9 = np.clip(y9.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    y10 = np.clip(y10.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    y11 = np.clip(y11.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    y12 = np.clip(y12.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    
    binary_data = struct.pack('h' * BLOCKLEN, *(y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8 + y9 + y10 + y11 +y12));    # Convert to binary binary data
    stream.write(binary_data, BLOCKLEN)               

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()
