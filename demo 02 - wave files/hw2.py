
import wave

#cz2146 ce zhang

wf = wave.open('hello.wav')

ch=wf.getnchannels() 	# number of channels

rate=wf.getframerate() 	# frame rate (number of frames per second)

length=wf.getnframes() 	# total number of frames (length of signal)

frame=wf.getsampwidth() 	# number of bytes per sample

print(ch,rate,length,frame)    #print

wf.close()

