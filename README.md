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

# N3 Sleep Scoring Module

A Python module for **automatic N3 (deep sleep) scoring** from EEG recordings based on **AASM guidelines**.  
It detects **slow-wave activity (SWA, 0.5–2 Hz)** in the **F4-M1 EEG channel** and classifies epochs as `N3` or `Not N3` based on the proportion of slow waves.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Output](#output)
- [Example](#example)
- [References](#references)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Features

- **FIR Bandpass Filtering:** Isolates slow-wave activity (0.5–2 Hz).  
- **Zero-Crossing Detection:** Identifies candidate slow waves.  
- **Amplitude & Duration Checks:** Validates waves with ≥75 µV amplitude and 0.5–2 sec duration.  
- **SWA Percentage Calculation:** Measures fraction of each epoch occupied by slow waves.  
- **Epoch-wise Scoring:** Scores each epoch (default 30s) individually.  
- **Signal Quality Checks:** Skips flat or noisy epochs to prevent inaccurate scoring.  
- **Lightweight & Standalone:** Requires only `numpy` and `scipy`.

---

## Installation

Follow these steps to set up the **N3 Sleep Scoring Module**:

### 1. Clone the Repository

Download the project from GitHub:

```bash
git clone https://github.com/RajanRajbhar12/n3-sleep-scoring.git
This will create a folder called n3-sleep-scoring with all the project files.

2. Navigate to the Project Folder
bash
Copy code
cd n3-sleep-scoring
3. (Optional) Create a Python Virtual Environment
It is recommended to use a virtual environment to avoid conflicts with other packages:

bash
Copy code
python -m venv venv         # Create a virtual environment named 'venv'
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
4. Install Dependencies
Install required Python packages:


pip install -r requirements.txt
Dependencies:

Python 3.8 or higher

numpy – for numerical computations

scipy – for signal processing

Tip: If pip is not installed, use:


python -m ensurepip --upgrade
5. Verify Installation
You can test the installation by running the example script:

Usage
Scoring N3 from EEG

import numpy as np
from n3_scoring import score_n3_epochs

# Sampling rate (Hz)
fs = 100

# Example EEG signal (F4-M1) with 1 Hz slow waves
t = np.arange(0, 300, 1/fs)  # 5 minutes
eeg_signal = 100 * np.sin(2 * np.pi * 1 * t)

# Score EEG epochs for N3
results = score_n3_epochs(eeg_signal, fs)

# Print first 10 epochs
for epoch in results[:10]:
    print(f"Epoch {epoch['epoch']}: Stage={epoch['stage']}, SWA={epoch['swa_percent']:.1f}%")

References
American Academy of Sleep Medicine (AASM) Manual for the Scoring of Sleep and Associated Events, 2017

EEG Slow Wave Analysis Principles

Harris, F. J., "On the use of windows for harmonic analysis with the discrete Fourier transform," 1978

Contributing
Contributions are welcome!

Fork the repository

Make your changes

Submit a pull request with a clear description

License
MIT License – free to use and modify.

Author
Rajan Rajbhar

GitHub: RajanRajbhar12

Email: your.rajannrajb502@gmail.com
