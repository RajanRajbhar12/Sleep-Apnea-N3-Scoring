"""
N3 Sleep Scoring Module
======================
This module scores N3 (deep sleep) epochs from EEG F4-M1 channel
following AASM guidelines. It uses slow wave detection (0.5-2 Hz)
and checks whether slow wave activity occupies >=20% of the epoch.

Author: Rajan
"""

import numpy as np
from scipy.signal import firwin, filtfilt

# ---------------------------
# Signal Quality Check
# ---------------------------
def check_signal_quality(signal, fs):
    """
    Ensure the EEG signal is usable for N3 scoring.
    
    Parameters:
    - signal: 1D numpy array of EEG data
    - fs: sampling frequency in Hz
    
    Returns:
    - True if signal quality is acceptable, False otherwise
    """
    if len(signal) < 2:
        return False  # too short to analyze
    if np.max(np.abs(signal)) == 0:
        return False  # flat signal
    # Estimate signal-to-noise ratio (SNR)
    signal_power = np.var(signal)             # variance ~ signal power
    noise_power = np.var(np.diff(signal))     # derivative ~ noise estimate
    if noise_power == 0:
        return signal_power > 0.1
    snr = signal_power / noise_power
    return snr > 5.0  # empirically determined threshold

# ---------------------------
# N3 Epoch Scoring Function
# ---------------------------
def score_n3_epoch(eeg_signal, fs, epoch_duration=30):
    """
    Scores a single EEG epoch for N3 (deep sleep) based on slow-wave activity.

    Steps:
    1. Filter the EEG in 0.5-2 Hz band using FIR filter to isolate slow waves
    2. Find zero-crossings to identify candidate waves
    3. Check each candidate wave for amplitude, duration, and presence of both positive/negative peaks
    4. Accumulate total time of valid slow waves
    5. Compute SWA percentage: (slow wave time / epoch duration) * 100
    6. If SWA >=20%, classify as N3

    Parameters:
    - eeg_signal: 1D numpy array of EEG samples
    - fs: sampling frequency in Hz
    - epoch_duration: duration of the epoch in seconds (default 30s)

    Returns:
    - swa_percent: percentage of epoch occupied by slow-wave activity
    """
    # Step 0: Check if signal quality is good
    if not check_signal_quality(eeg_signal, fs):
        return 0.0  # Poor signal, cannot score

    # Step 1: FIR Bandpass Filter (0.5-2 Hz) for slow waves
    nyquist = 0.5 * fs
    numtaps = 366  # Number of taps determines filter sharpness (Fred Harris rule)
    fir_coeffs = firwin(numtaps, [0.5/nyquist, 2.0/nyquist], pass_zero=False)
    eeg_filtered = filtfilt(fir_coeffs, 1.0, eeg_signal)
    # filtfilt: zero-phase filtering, avoids phase shift in slow waves

    # Step 2: Identify zero crossings
    zero_crossings = np.where(np.diff(np.sign(eeg_filtered)))[0]
    # zero_crossings: indices where signal crosses zero (positive -> negative or vice versa)

    # Step 3: Loop over candidate waves
    total_swa_time = 0.0  # total duration of valid slow waves in this epoch
    i = 0
    while i < len(zero_crossings) - 2:
        start_idx = zero_crossings[i]
        end_idx = zero_crossings[i + 2]  # a wave is defined by 3 zero crossings
        candidate_wave = eeg_filtered[start_idx:end_idx]

        if len(candidate_wave) < 2:
            i += 1
            continue

        # Step 3a: Peak-to-peak amplitude check
        peak_to_peak = np.max(candidate_wave) - np.min(candidate_wave)
        is_tall_enough = peak_to_peak >= 75  # µV, per AASM criteria

        # Step 3b: Duration check
        duration_sec = (end_idx - start_idx) / fs
        is_slow_enough = 0.5 <= duration_sec <= 2.0  # 0.5–2 sec per 0.5–2 Hz

        # Step 3c: Both positive and negative deflections must exist
        has_both_signs = np.any(candidate_wave > 0) and np.any(candidate_wave < 0)

        # Step 4: Accumulate valid slow-wave duration
        if is_tall_enough and is_slow_enough and has_both_signs:
            total_swa_time += duration_sec
            i += 2  # skip to next candidate
        else:
            i += 1

    # Step 5: Compute percentage of slow-wave activity (SWA)
    swa_percent = (total_swa_time / epoch_duration) * 100
    return swa_percent

# ---------------------------
# Full EEG N3 Scoring
# ---------------------------
def score_n3_epochs(eeg_signal, fs, epoch_duration=30):
    """
    Split EEG signal into epochs and score each for N3 sleep.

    Parameters:
    - eeg_signal: 1D numpy array of EEG (F4-M1)
    - fs: sampling frequency in Hz
    - epoch_duration: seconds per epoch (default 30s)

    Returns:
    - List of dicts: [{epoch:0, stage:'N3', swa_percent:25.5}, ...]
    """
    samples_per_epoch = epoch_duration * fs
    num_epochs = len(eeg_signal) // samples_per_epoch
    results = []

    for i in range(num_epochs):
        start = i * samples_per_epoch
        end = start + samples_per_epoch
        epoch_signal = eeg_signal[start:end]

        # Score the epoch for N3 using SWA
        swa_percent = score_n3_epoch(epoch_signal, fs, epoch_duration)

        # Determine stage
        stage = "N3" if swa_percent >= 20.0 else "Not N3"

        # Store results
        results.append({
            "epoch": i,
            "stage": stage,
            "swa_percent": swa_percent
        })

    return results

