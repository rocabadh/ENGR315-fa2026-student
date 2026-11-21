"""
CULMINATING ASSIGNMENT 3: Musical Note Detection

Create a program which detects the note being played from the given audio file based on its frequency.
It is up to you to employ an appropriate methodology to process the audio signal and detect the note.
The relevant data file is named "Guitar-note-1.wav" and is located in data > musical-notes.
In the same directory, we also provide a reference for the corresponding frequencies of each note.

Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
We have provided a possible method for converting the .wav file to usable data below.
All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""
#Import Packages
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import pandas as pd

#Load Reference Frequencies for Musical Notes
ref_path="../../data/musical-notes/note-frequencies-reference.csv"
ref_df=pd.read_csv(ref_path, skiprows=[1])
ref_df["Frequency"]=ref_df["Frequency"].astype(float)

#Load and read the audio file
path="../../data/musical-notes/Guitar-note-1.wav"
sample_rate, audio_data = wavfile.read(path)


#Task 1
#Finding the length of the audio data
duration=len(audio_data)/sample_rate
time=np.arange(len(audio_data))/sample_rate

#Plot audio signal over time 
plt.figure(figsize=(8,5))
plt.plot(time, audio_data, label="Raw Audio Signal")
plt.title("Audio Signal Over Time")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend(loc="lower center")
plt.grid(True,alpha=0.3)
plt.show()

#Task 2
#Center and Normalize the raw audio signal
centered_signal=audio_data.astype(float)-np.mean(audio_data)
norm_original=centered_signal/np.max(np.abs(centered_signal))

#Apply a Bandpass Filter to Remove Noise
nyquist_freq=0.5*sample_rate
high_cutoff=min(4500, 0.95*nyquist_freq)
b, a =signal.butter(N=4, Wn=[25/nyquist_freq, high_cutoff/nyquist_freq], btype='band')
Filtered_signal=signal.lfilter(b, a, norm_original)

#Find Active Note Region
window=int(0.10*sample_rate) #100ms window
diff_signal=np.diff(Filtered_signal, prepend=Filtered_signal[0])
square_signal=np.square(diff_signal)
moving_avg=np.convolve(square_signal, np.ones(window)/window, mode='same')

#Find where signal energy is above 20% of the maximum
active_region=np.where(moving_avg>0.2*np.max(moving_avg))[0]

#Skip first 0.1 seconds to avoid transients 
steady_start=active_region[0]+int(0.1*sample_rate)

#Finding Peaks in Steady State Region
s_end=steady_start+int(0.10*sample_rate)
s_time=time[steady_start:s_end]
s_signal=Filtered_signal[steady_start:s_end]

#Peaks must be 50% of local max height
min_dist=int(sample_rate/ref_df["Frequency"].max()) 
peaks, _=signal.find_peaks(s_signal, height=0.5*np.max(s_signal), prominence=0.5*np.max(s_signal), distance=min_dist)

#Find periods of interest within the signal
z_start=peaks[0]
z_end=peaks[min(5,len(peaks)-1)] 

#Plot Original vs Filtered Signal 
plt.figure(figsize=(8,5))
plt.plot(
    s_time[z_start:z_end]*1000,
    norm_original[steady_start:s_end][z_start:z_end],
    color="Gray",
    linestyle="--",
    label="Original Signal (Normalized)"
)
plt.plot(
    s_time[z_start:z_end]*1000,
    s_signal[z_start:z_end],
    color="Blue",
    label="Processed Signal (Bandpass Filtered)"
)
plt.title("Processed Signal vs Original Signal (Periods of Interest)")
plt.xlabel("Time (ms)")
plt.ylabel("Normalized Amplitude")
plt.legend(loc="lower center", ncol=2)
plt.ylim(-1.1,1.1)
plt.grid(True,alpha=0.3)
plt.show()

#Task 3
#Isolate a slice of the filtered signal
detect_end=min(steady_start+int(0.25*sample_rate), active_region[-1]) 
detect_signal=Filtered_signal[steady_start:detect_end]

#Create window and perform FFT
fft_window=detect_signal*np.hanning(len(detect_signal))
n_fft=1<<20
spectrum=np.abs(np.fft.rfft(fft_window, n=n_fft))
fft_freqs=np.fft.rfftfreq(n_fft, 1/sample_rate)

#Limit to musical note range
in_range=(fft_freqs>=ref_df["Frequency"].min()) & (fft_freqs<=ref_df["Frequency"].max())
valid_freqs=fft_freqs[in_range]
valid_spectrum=spectrum[in_range]

#Find peaks and lowest frequency peak is f0
min_bin_dist=int(20/(sample_rate/n_fft))
spec_peaks, _ =signal.find_peaks(valid_spectrum, height=0.25*np.max(valid_spectrum), distance=min_bin_dist)
detected_freq=valid_freqs[spec_peaks][0] 

#Find Matching Note for Detected Frequency
closest=np.abs(ref_df["Frequency"]-detected_freq).idxmin()
detected_note=ref_df.loc[closest, "Note"]
ref_freq=ref_df.loc[closest, "Frequency"]

#Print Task 3 Results
print("Task 3 Results:")
print(f"Detected Frequency: {detected_freq:.4f} Hz")
print(f"Closest Reference Frequency: {ref_freq:.4f} Hz")
print(f"Detected Musical Note: {detected_note}")

#Print wav file properties
print("WAV File Properties:")
print(f"Sample Rate: {sample_rate} Hz")
print(f"Audio Data Shape: {audio_data.shape}")
print(f"Audio Data Type: {audio_data.dtype}")
print(f"Audio Data Min: {audio_data.min()}")
print(f"Audio Data Max: {audio_data.max()}")
