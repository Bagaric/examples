#!/usr/bin/python
#############################################################################
# This script is used to draw graphs of real-time audio input from the mic. #
#############################################################################
 
import numpy, alsaaudio, time, wave, audioop, matplotlib.pyplot as plt
from threading import Thread
 
# Used for grabbing the individual samples from a sound fragment captured by the microphone
def get_samples(data):
    return list(audioop.getsample(data, 2, i) for i in xrange(len(data) / 4))
 
# Thread that does the graph drawing
def draw_raw_audio_thread(raw):
    while True:
        plt.cla() # Clears the current axes
        plt.title('Raw Audio')
        plt.plot(raw[-10000:]) # Plots values of the last 10000 elements (samples) of the raw audio
        plt.axis([0,10000,-40000,40000]) # Axis limits ([xmin, xmax, ymin, ymax])
 
        plt.draw() # Draws the figure
 
        time.sleep(0.5) # Wait a bit before drawing again
 
if __name__ == "__main__":
 
    # Initialize audio recording device
    inputaudio = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NORMAL)
 
    # Setting attributes for the audio
    inputaudio.setchannels(2) # 1-mono, 2-stereo
    inputaudio.setrate(8000) # Audio sample rate (samples per second)
    inputaudio.setformat(alsaaudio.PCM_FORMAT_S16_LE) # sample size - 16 bits
 
    # Period size - Sets the actual period size in samples. Each write should consist of
    # exactly this number of samples, and each read will return this number of samples
    # (unless the device is in PCM_NONBLOCK mode, in which case it may return nothing at all)
    inputaudio.setperiodsize(40)
 
    # We will use this variable as a buffer for the audio data
    raw_audio_data = []
 
    # Initialize the GUI
    plt.ion()
    plt.show()
 
    # Start the thread for drawing graphs
    thread = Thread(target = draw_raw_audio_thread, args = (raw_audio_data, ))
    thread.start()
 
    # Start recording audio
    while True:
        periodlen,data = inputaudio.read()  # Read the audio data and length of the period into variables
        raw_audio_data.extend(get_samples(data)) # Add recorded samples into the buffer
 
        # When you have 100 000 samples in the buffer, empty the buffer (besides of last 10 000 samples)
        if len(raw_audio_data) > 100000:
            raw_audio_data[:] = raw_audio_data[-10000:]
