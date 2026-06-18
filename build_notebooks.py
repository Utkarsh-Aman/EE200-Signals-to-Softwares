import json
import os

def create_notebook(cells, filename):
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(filename, 'w') as f:
        json.dump(notebook, f, indent=2)

def md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [text]
    }

def code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [code]
    }

# --- Q1 Notebook ---
q1_cells = [
    md_cell("# EE200 Course Project - Q1\n\n## Group Members: \n(Student details here)"),
    code_cell("import cv2\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom scipy import signal"),
    md_cell("## Q1A. Frequency Forensics - 'The Ghost Signal'\nLet's load the corrupted image and inspect it in the spatial domain."),
    code_cell("img_path = 'Q1_data/ghost_signal_input.png'\nimg = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)\nif img is None:\n    # Fallback to matplotlib if cv2 fails to read\n    img = plt.imread(img_path)\n    if len(img.shape) > 2:\n        img = np.mean(img, axis=2)\n\nplt.figure(figsize=(6,6))\nplt.imshow(img, cmap='gray')\nplt.title('Corrupted Image (Spatial Domain)')\nplt.axis('off')\nplt.show()"),
    md_cell("### 1. Transform to Frequency Domain\nWe compute the 2D Discrete Fourier Transform (DFT) and shift the zero-frequency component to the center. Then we plot the magnitude spectrum in both linear and logarithmic (dB) scales."),
    code_cell("F = np.fft.fft2(img)\nF_shift = np.fft.fftshift(F)\n\nmagnitude_spectrum_linear = np.abs(F_shift)\nmagnitude_spectrum_db = 20 * np.log10(magnitude_spectrum_linear + 1e-8)\n\nfig, axes = plt.subplots(1, 2, figsize=(12, 6))\naxes[0].imshow(magnitude_spectrum_linear, cmap='gray')\naxes[0].set_title('Magnitude Spectrum (Linear Scale)')\naxes[1].imshow(magnitude_spectrum_db, cmap='gray')\naxes[1].set_title('Magnitude Spectrum (dB Scale)')\nplt.show()"),
    md_cell("### 2. Identifying and Filtering the Interference\nPeriodic interference appears as distinct bright spots (spikes) in the magnitude spectrum away from the center. We will create a filter to suppress these specific frequencies. Since we want to remove specific frequencies, we will use a notch filter (setting the highest non-center peaks to zero)."),
    code_cell("rows, cols = img.shape\ncrow, ccol = rows//2 , cols//2\n\n# Automatically find the top peaks excluding the center (low frequencies)\nmag_copy = np.copy(magnitude_spectrum_linear)\n# Mask out the central region (useful image content)\nmask_radius = 30\ncv2.circle(mag_copy, (ccol, crow), mask_radius, 0, -1)\n\n# Find the coordinates of the maximum peaks (interference)\n# We'll filter out the highest spikes symmetrically\nnum_peaks = 4 \nfilter_mask = np.ones((rows, cols), np.uint8)\nnotch_radius = 5\n\nfor i in range(num_peaks):\n    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(mag_copy)\n    if max_val > 0:\n        cv2.circle(filter_mask, max_loc, notch_radius, 0, -1)\n        # Zero out the local region in mag_copy so we can find the next peak\n        cv2.circle(mag_copy, max_loc, notch_radius, 0, -1)\n\nplt.imshow(filter_mask, cmap='gray')\nplt.title('Notch Filter Mask')\nplt.show()"),
    md_cell("### 3. Reconstructing the Image\nApply the filter mask in the frequency domain and use the Inverse 2D DFT to reconstruct the spatial image."),
    code_cell("F_shift_filtered = F_shift * filter_mask\nF_ishift = np.fft.ifftshift(F_shift_filtered)\nimg_back = np.fft.ifft2(F_ishift)\nimg_recovered = np.abs(img_back)\n\nfig, axes = plt.subplots(1, 2, figsize=(12, 6))\naxes[0].imshow(img, cmap='gray')\naxes[0].set_title('Corrupted Original')\naxes[0].axis('off')\naxes[1].imshow(img_recovered, cmap='gray')\naxes[1].set_title('Recovered Image')\naxes[1].axis('off')\nplt.show()"),
    md_cell("## Q1B. Digital Detective - 'Missing Boundaries'\nLet's apply the Sobel filter to detect edges. We will compare the results with and without image smoothing (noise reduction)."),
    code_cell("img2_path = 'Q1_data/missing_boundaries_input.avif'\n# Try loading AVIF using standard methods; if fails, standard format conversion might be needed outside.\nimport imageio.v3 as iio\ntry:\n    img2 = iio.imread(img2_path)\n    if len(img2.shape) > 2:\n        img2 = np.mean(img2, axis=2)\nexcept:\n    print('Please ensure imageio supports AVIF, or convert the image to PNG for testing.')\n    img2 = np.zeros((100,100)) # Placeholder if AVIF read fails\n\n# Sobel kernels\nsobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])\nsobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])\n\n# 1. Edge detection WITHOUT smoothing\ngrad_x = signal.convolve2d(img2, sobel_x, boundary='symm', mode='same')\ngrad_y = signal.convolve2d(img2, sobel_y, boundary='symm', mode='same')\nedges_raw = np.sqrt(grad_x**2 + grad_y**2)\n\n# 2. Edge detection WITH Gaussian smoothing\nkernel_size = 5\nsigma = 1.0\nax = np.linspace(-(kernel_size - 1) / 2., (kernel_size - 1) / 2., kernel_size)\nxx, yy = np.meshgrid(ax, ax)\nkernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sigma))\ngaussian_kernel = kernel / np.sum(kernel)\n\nimg2_smooth = signal.convolve2d(img2, gaussian_kernel, boundary='symm', mode='same')\ngrad_x_smooth = signal.convolve2d(img2_smooth, sobel_x, boundary='symm', mode='same')\ngrad_y_smooth = signal.convolve2d(img2_smooth, sobel_y, boundary='symm', mode='same')\nedges_smooth = np.sqrt(grad_x_smooth**2 + grad_y_smooth**2)\n\nfig, axes = plt.subplots(1, 3, figsize=(15, 5))\naxes[0].imshow(img2, cmap='gray')\naxes[0].set_title('Original Input')\naxes[1].imshow(edges_raw, cmap='gray')\naxes[1].set_title('Edges (No Smoothing)')\naxes[2].imshow(edges_smooth, cmap='gray')\naxes[2].set_title('Edges (With Smoothing)')\nfor ax in axes: ax.axis('off')\nplt.show()")
]

# --- Q2 Notebook ---
q2_cells = [
    md_cell("# EE200 Course Project - Q2\n\n## The Midnight Episode: Catching the Arrhythmia"),
    code_cell("import numpy as np\nimport matplotlib.pyplot as plt\nfrom scipy import signal"),
    md_cell("### Loading the Data"),
    code_cell("ecg_signal = np.load('Q2_data/patient_ecg.npy')\ntemplate = np.load('Q2_data/template.npy')\n\nfs = 250 # Sampling frequency in Hz\nN = len(ecg_signal)\ntime = np.arange(N) / fs\n\nplt.figure(figsize=(12, 4))\nplt.plot(time, ecg_signal)\nplt.title('Patient ECG Recording')\nplt.xlabel('Time (seconds)')\nplt.ylabel('Amplitude')\nplt.show()"),
    md_cell("### (a) Reading the signal\n(i) How many seconds long is the clip?\n(ii) Heart rate & healthy beat samples\n(iii) Fundamental frequency $f_0$"),
    code_cell("total_seconds = N / fs\nbeat_interval_sec = 0.8\nheart_rate_bpm = 60 / beat_interval_sec\nsamples_per_beat = int(beat_interval_sec * fs)\nfundamental_freq = 1 / beat_interval_sec\n\nprint(f\"(i) Clip duration: {total_seconds} seconds\")\nprint(f\"(ii) Heart rate: {heart_rate_bpm} BPM. Samples per healthy beat: {samples_per_beat}\")\nprint(f\"(iii) Fundamental frequency (f0): {fundamental_freq} Hz\")"),
    md_cell("### (g) Prototyping the detector in code\nWriting the `find_onset` function to calculate normalized correlation beat-by-beat and identify the onset index."),
    code_cell("def find_onset(ecg_signal, template, threshold=0.5):\n    L = len(template)\n    N = len(ecg_signal)\n    norm_t = np.linalg.norm(template)\n    \n    correlations = []\n    indices = []\n    \n    # Jumping forward by the length of the template each time\n    for m in range(0, N - L + 1, L):\n        segment = ecg_signal[m:m+L]\n        norm_x = np.linalg.norm(segment)\n        \n        if norm_x == 0:\n            corr = 0\n        else:\n            corr = np.dot(template, segment) / (norm_t * norm_x)\n            \n        correlations.append(corr)\n        indices.append(m)\n        \n        if corr < threshold:\n            return m\n            \n    return -1\n\nonset_index = find_onset(ecg_signal, template, threshold=0.5)\nonset_time = onset_index / fs if onset_index != -1 else -1\nprint(f\"Arrhythmia Onset detected at index: {onset_index} (Time: {onset_time:.2f} s)\")"),
    md_cell("### (h) Visualizing the Spectrogram\nComputing and plotting the spectrogram using `scipy.signal` and `matplotlib.pyplot`.\n\n*Window Length Justification*: To reveal steady horizontal harmonic bands (good frequency resolution) in the healthy region while maintaining enough time resolution to spot the onset, we need a window that covers a few beats. At $fs=250$ Hz and 0.8s per beat, 1 beat is 200 samples. A window of around 600-800 samples (3-4 beats) is ideal. We choose `nperseg=600`."),
    code_cell("nperseg = 600 # Window length\nf_spec, t_spec, Sxx = signal.spectrogram(ecg_signal, fs=fs, nperseg=nperseg, noverlap=nperseg//2)\n\nplt.figure(figsize=(10, 5))\nplt.pcolormesh(t_spec, f_spec, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')\nplt.title('Spectrogram of Patient ECG')\nplt.ylabel('Frequency [Hz]')\nplt.xlabel('Time [sec]')\nplt.colorbar(label='Power/Frequency [dB/Hz]')\nplt.axvline(x=onset_time, color='red', linestyle='--', label='Detected Onset')\nplt.legend()\nplt.show()")
]

create_notebook(q1_cells, 'Q1/Q1_Submission.ipynb')
create_notebook(q2_cells, 'Q2/Q2_Submission.ipynb')
print("Notebooks generated successfully.")
