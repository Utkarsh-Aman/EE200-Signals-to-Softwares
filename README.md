# EE200: Signals, Systems and Networks - Course Project

Welcome to the repository for the EE200 course project! This project explores practical applications of signal processing techniques across three distinct domains: image processing (2D DFT and edge detection), biomedical signal analysis (ECG arrhythmia detection), and audio processing (Audio Fingerprinting).

## 🚀 Project Overview

The project is divided into three main modules, each addressing a unique real-world problem using signals and systems concepts:

### 1. Q1: Frequency Forensics & Digital Detective (Image Processing)
- **Part A (Frequency Forensics - 'The Ghost Signal')**: Focuses on analyzing images corrupted by periodic interference. We utilize the 2D Discrete Fourier Transform (2D DFT) to inspect the frequency domain and apply Notch Filters to suppress unwanted periodic noise (spikes) while preserving the natural image content.
- **Part B (Digital Detective - 'Missing Boundaries')**: Explores spatial filtering and edge detection. It demonstrates the use of the Sobel filter to compute image gradients, the impact of high-frequency noise on edge detection, and the necessity of Gaussian smoothing to balance noise suppression and edge preservation.
- **Key Files**: `Q1/Q1_Submission.ipynb`

### 2. Q2: The Midnight Episode (ECG Signal Analysis)
- **'Catching the Arrhythmia'**: Analyzes a 20-second electrocardiogram (ECG) recording to detect abnormal heartbeats (tachycardia and arrhythmia). 
- **Techniques Used**:
  - Frequency domain analysis of nearly periodic signals.
  - Time-domain template matching (normalized cross-correlation) to detect specific heartbeat shapes and inverted beats.
  - Spectrogram analysis to visualize time-varying frequency content and pinpoint the exact onset of arrhythmia.
  - Understanding the effects of sampling rates and aliasing on clinical data.
- **Key Files**: `Q2/Q2_arrhythmia_detection.ipynb`

### 3. Q3: Sonic Signatures (Audio Fingerprinting)
- **'Magical Mystery Tune'**: Implements an audio fingerprinting system (similar to Shazam) to identify songs from short, potentially noisy audio snippets. 
- **Techniques Used**:
  - Spectrogram generation.
  - Constellation map creation (identifying peak frequencies over time).
  - Target zone pairing and hash generation to match audio samples against a database.
- **Key Files**: `Q3/Audio_Fingerprinting/fingerprint.py`, `Q3/3A_Plots.py`
- **Live Streamlit App**: [https://audio-fingerprinting-241114-240622.streamlit.app/](https://audio-fingerprinting-241114-240622.streamlit.app/)
  - *Alternate Link*: [https://audio-fingerprinting-240622-241114.streamlit.app/](https://audio-fingerprinting-240622-241114.streamlit.app/)

## 📂 File Structure

```text
EE200/
├── Q1/                               # Image Processing (DFT & Edge Detection)
│   ├── Q1_Submission.ipynb           # Main Jupyter Notebook for Q1
│   ├── main.tex                      # LaTeX report for Q1
│   ├── Q1_data/                      # Image datasets
│   └── ...
├── Q2/                               # Biomedical Signal Processing (ECG)
│   ├── Q2_arrhythmia_detection.ipynb # Main Jupyter Notebook for Q2
│   ├── main.tex                      # LaTeX report for Q2
│   ├── Q2_data/                      # ECG signal datasets
│   └── ...
├── Q3/                               # Audio Processing (Fingerprinting)
│   ├── Audio_Fingerprinting/         # Core audio fingerprinting logic
│   │   └── fingerprint.py
│   ├── 3A_Plots.py                   # Plotting scripts for Q3
│   ├── main.tex                      # LaTeX report for Q3
│   └── ...
├── Project_Report.md                 # Detailed theoretical analysis and mathematical foundations
└── EE200_course_project_summer_2026.pdf # Original project description/problem statement
```

## 🛠️ How to Run

### Prerequisites
Make sure you have Python installed along with the typical scientific computing stack. We recommend using a virtual environment (`.venv`).
Required libraries generally include:
- `numpy`
- `matplotlib`
- `scipy`
- `jupyter` (for running the notebooks)

### Running the Code

1. **Activate the Virtual Environment**:
   If you are using the `.venv` directory already present in the root:
   ```bash
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```
   Install the required dependencies using pip if they are not already installed.

2. **Run Jupyter Notebooks (for Q1 and Q2)**:
   ```bash
   jupyter notebook
   ```
   Navigate to `Q1/Q1_Submission.ipynb` or `Q2/Q2_arrhythmia_detection.ipynb` and execute the cells sequentially to view the analysis and generated plots.

3. **Run Python Scripts (for Q3)**:
   Navigate to the `Q3` directory and run the python scripts directly:
   ```bash
   cd Q3
   python 3A_Plots.py
   ```

## 📖 Detailed Report

For an in-depth understanding of the mathematical equations, reasoning, and theoretical foundations behind the code, please refer to the [Project_Report.md](./Project_Report.md) located in the root directory.
