import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


def snr(in_vec, out_vec):
    # Calculate the noise as the difference between the input and output signals
    noise = in_vec - out_vec
    
    # Calculate the power of the signal and noise
    signal_power = np.sum(in_vec ** 2)
    noise_power = np.sum(noise ** 2)
    
    # Handle edge case: if noise power is zero, SNR is infinite
    if noise_power == 0:
        return float('inf')
    
    # Calculate SNR in decibels
    snr_value = 10 * np.log10(signal_power / noise_power)
    return snr_value


Fs, x = wavfile.read('vega.wav')   # Read the audio file

# Normalize the signal to the range [-1, 1] if it's in integer format
if x.dtype != np.float32 and x.dtype != np.float64:
    x = x / np.max(np.abs(x))

snr_values = []

for n in range (16 , 0, -1):

    # Quantization
    xq = np.floor((x + 1) * 2**(n - 1))
    xq = xq / (2**(n - 1))
    xq = xq - (2**(n - 1) - 1) / 2**n

    # Error signal
    xe = x - xq

    snr_value = snr(x, xq)
    snr_values.append(snr_value)

    # print(f"SNR for {n}-bit quantization: {snr_value:.2f} dB")


# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(range(16, 0, -1), snr_values, marker='o', linestyle='-', color='b')
plt.title('Signal-to-Noise Ratio (SNR) vs Quantization Bit Depth')
plt.xlabel('Quantization Bit Depth')
plt.ylabel('SNR (dB)')
plt.grid(True)
plt.xticks(range(1, 17))
plt.show()