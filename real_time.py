import sounddevice as sd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend
import matplotlib.pyplot as plt
import time
import os

# ----------------------------
# CONFIG
# ----------------------------
fs = 44100           # Sampling rate
duration = 10        # Total recording duration (seconds)
block_size = 2048    # Samples per block
device = 'hw:1,0'    # USB microphone device
output_file = "live_waveform.png"
# ----------------------------

print(f"Starting live waveform recording for {duration} seconds...")

num_blocks = int(duration * fs / block_size)
audio_buffer = np.array([], dtype=np.int16)

for i in range(num_blocks):
    block = sd.rec(block_size, samplerate=fs, channels=1, dtype='int16', device=device)
    sd.wait()
    block = block.flatten()
    audio_buffer = np.concatenate((audio_buffer, block))
    
    # Plot the current buffer
    plt.figure(figsize=(10, 4))
    plt.plot(audio_buffer, color='blue')
    plt.title("Live Audio Waveform")
    plt.xlabel("Sample Number")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    
    print(f"Block {i+1}/{num_blocks} recorded. Waveform updated.")

print(f"Recording complete! Waveform saved as {output_file}")
