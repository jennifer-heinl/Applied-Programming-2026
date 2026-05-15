# Copyright 2025 n-squared LAB @ FAU Erlangen-Nürnberg

"""
Reference solution for the EMG Signal Processing Exercise.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal


def load_emg_data(filename: str):
    data = pd.read_pickle(filename)

    print("Data structure:")
    print("-" * 50)
    print(f"Data type: {type(data)}")
    print(f"Data shape: {data.shape if hasattr(data, 'shape') else 'N/A'}")
    print("\nAvailable keys in data:")
    print("-" * 50)
    for key in data.keys():
        print(f"- {key}")
    print("-" * 50)

    emg_signal = data["biosignal"]
    sampling_rate = data["device_information"]["sampling_frequency"]

    print("\nEMG Signal information:")
    print("-" * 50)
    print(f"Signal shape: {emg_signal.shape}")
    print(f"Number of channels: {emg_signal.shape[0]}")
    print(f"Window size: {emg_signal.shape[1]}")
    print(f"Number of windows: {emg_signal.shape[2]}")
    print(f"Sampling rate: {sampling_rate} Hz")

    return emg_signal, sampling_rate


def restructure_emg_data(emg_signal: np.ndarray):
    num_channels = emg_signal.shape[0]
    channel_data = emg_signal.transpose(2, 1, 0).reshape(-1, num_channels).T

    print("\nRestructured EMG Data:")
    print("-" * 50)
    print(f"Original shape: {emg_signal.shape}")
    print(f"New shape: {channel_data.shape}")
    print(f"Number of channels: {num_channels}")
    print(f"Total samples per channel: {channel_data.shape[1]}")

    return channel_data, num_channels


def bandpass_filter_emg(
    channel_data: np.ndarray,
    sampling_rate: float,
    low_cut: float = 20,
    high_cut: float = 450,
):
    nyquist = sampling_rate / 2

    if low_cut <= 0:
        raise ValueError("Low cutoff frequency must be greater than 0 Hz.")
    if high_cut >= nyquist:
        raise ValueError(
            f"High cutoff frequency ({high_cut} Hz) exceeds Nyquist frequency ({nyquist} Hz)."
        )
    if low_cut >= high_cut:
        raise ValueError("Low cutoff frequency must be smaller than high cutoff frequency.")

    low = low_cut / nyquist
    high = high_cut / nyquist

    print("\nFilter Design Parameters:")
    print("-" * 50)
    print(f"Sampling rate: {sampling_rate} Hz")
    print(f"Nyquist frequency: {nyquist} Hz")
    print(f"Low cutoff: {low_cut} Hz ({low:.4f} normalized)")
    print(f"High cutoff: {high_cut} Hz ({high:.4f} normalized)")

    b, a = signal.butter(4, [low, high], btype="band")
    filtered_channels = np.zeros_like(channel_data)

    for i in range(channel_data.shape[0]):
        filtered_channels[i, :] = signal.filtfilt(b, a, channel_data[i, :])

    print("\nFiltered Signal Information:")
    print("-" * 50)
    print(f"Shape of filtered_channels: {filtered_channels.shape}")
    print(f"Type of filtered_channels: {type(filtered_channels)}")
    print(f"Filter cutoff frequencies: {low_cut} Hz to {high_cut} Hz")

    return filtered_channels


import numpy as np

def compute_rms(filtered_channels: np.ndarray, sampling_rate: float, window_ms: float = 100):
    window_size = int((window_ms / 1000) * sampling_rate)
    rms_signals = np.zeros_like(filtered_channels)

    half_window = window_size // 2

    for channel in range(filtered_channels.shape[0]):
        signal = filtered_channels[channel, :]

        for i in range(signal.shape[0]):
            start = max(0, i - half_window)
            end = min(signal.shape[0], i + half_window)

            window = signal[start:end]
            rms_signals[channel, i] = np.sqrt(np.mean(window ** 2))

    print("\nRMS Signal Information:")
    print("-" * 50)
    print(f"Number of channels: {filtered_channels.shape[0]}")
    print(f"Shape of RMS signals: {rms_signals.shape}")
    print(f"Window size: {window_size} samples ({window_size / sampling_rate * 1000:.1f} ms)")

    return rms_signals


def plot_emg_processing(
    channel_data: np.ndarray,
    filtered_channels: np.ndarray,
    rms_signals: np.ndarray,
    sampling_rate: float,
    selected_channel: int = 0,
):
    t = np.arange(channel_data.shape[1]) / sampling_rate

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    ax1.plot(t, channel_data[selected_channel, :])
    ax1.set_title(f"Original EMG Signal - Channel {selected_channel + 1}")
    ax1.set_ylabel("Amplitude (V)")

    ax2.plot(t, filtered_channels[selected_channel, :])
    ax2.set_title(f"Bandpass Filtered Signal - Channel {selected_channel + 1}")
    ax2.set_ylabel("Amplitude (V)")

    ax3.plot(t, rms_signals[selected_channel, :])
    ax3.set_title(f"RMS Signal - Channel {selected_channel + 1}")
    ax3.set_ylabel("Amplitude (V)")
    ax3.set_xlabel("Time (s)")

    plt.tight_layout()
    plt.show()


def main():
    filename = "D:/PhD/Teaching/Applied-Programming-2026/Applied-Programming-2026/recording.pkl"

    emg_signal, sampling_rate = load_emg_data(filename)
    channel_data, _ = restructure_emg_data(emg_signal)
    filtered_channels = bandpass_filter_emg(channel_data, sampling_rate)
    rms_signals = compute_rms(filtered_channels, sampling_rate)

    plot_emg_processing(
        channel_data,
        filtered_channels,
        rms_signals,
        sampling_rate,
        selected_channel=0,
    )


if __name__ == "__main__":
    main()
