# N3 Sleep Scoring Module

A Python module for **automatic N3 (deep sleep) scoring** from EEG recordings based on **AASM guidelines**.  
It detects **slow-wave activity (SWA, 0.5–2 Hz)** in the **F4-M1 EEG channel** and classifies epochs as `N3` or `Not N3` based on the proportion of slow waves.

---

## Features

- **FIR Bandpass Filtering:** Isolates slow-wave activity (0.5–2 Hz).  
- **Zero-Crossing Detection:** Identifies candidate slow waves.  
- **Amplitude & Duration Checks:** Validates waves with ≥75 µV and 0.5–2 sec duration.  
- **SWA Percentage Calculation:** Computes fraction of epoch occupied by slow waves.  
- **Epoch-wise Scoring:** Scores each epoch (default 30s).  
- **Signal Quality Checks:** Skips poor-quality or flat signals.  
- **Lightweight:** Requires only `numpy` and `scipy`.

---

## Installation

```bash
git clone <your-repo-url>
cd n3-sleep-scoring
pip install -r requirements.txt
Dependencies: Python 3.8+, NumPy, SciPy


Methodology
Signal Quality Check – Rejects flat or noisy EEG epochs.

FIR Bandpass Filtering (0.5–2 Hz) – Isolates slow waves.

Zero-Crossing Detection – Finds candidate waves.

Wave Criteria – Amplitude ≥75 µV, Duration 0.5–2 sec, Both polarities present.

SWA Calculation – Total slow-wave duration / epoch length × 100.

Epoch Scoring – SWA ≥20% → N3, else Not N3.

References
AASM Manual for the Scoring of Sleep and Associated Events 2017

EEG Slow Wave Analysis Principles

License
MIT License – free to use and modify.

Author
Rajan Rajbhar
GitHub: RajanRajbhar12
Email: your.rajannrajb502@gmail.com


