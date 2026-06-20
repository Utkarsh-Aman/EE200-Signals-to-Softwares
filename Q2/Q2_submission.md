## Q2. The Midnight Episode - ‘Catching the Arrhythmia’

### (a) Reading the Signal
Assuming $N = 5000$ samples and $f_s = 250$ Hz, and that 1 full beat takes 0.8 seconds:
- **(i) Clip length:** The clip is $5000 / 250 = 20$ seconds long.
- **(ii) Heart rate & samples:** A beat every 0.8 seconds yields a heart rate of $60 / 0.8 = 75$ beats per minute (BPM). One healthy beat occupies $0.8 \times 250 = 200$ samples.
- **(iii) Fundamental frequency:** The healthy ECG is nearly periodic with period $T_0 = 0.8$ s. The fundamental frequency is $f_0 = 1 / T_0 = 1.25$ Hz.

### (b) Healthy Heart in Frequency Domain
- **(i) Spectrum Shape:** As a nearly periodic signal, the magnitude spectrum $|X(f)|$ will *not* be a smooth continuous curve. Instead, it will consist of a series of discrete spikes (harmonics) located at integer multiples of the fundamental frequency ($f_0 = 1.25$ Hz).
- **(ii) High-Frequency Content:** The **QRS spike** is sharp and narrow in time, meaning it contains rapid changes. By Fourier properties, a sharp, narrow signal in the time domain corresponds to broad, high-frequency components in the frequency domain. The broad P and T waves correspond to lower frequencies.
- **(iii) Tachycardia:** If the heart rate rises to 150 bpm ($2.5$ beats per second), the fundamental frequency $f_0$ becomes $2.5$ Hz. The discrete components in the spectrum will space out further apart, occurring at multiples of 2.5 Hz instead of 1.25 Hz.

### (c) Windowing
- **(i) Template Window:** To capture exactly one full beat, the window should be $200$ samples wide. It should be placed in the early portion of the recording where the ECG is known to be healthy and stable.
- **(ii) Incorrect Window Sizes:** A window of **80 samples** is too narrow and will likely clip out crucial parts of the beat (like the P or T waves), meaning the template is incomplete. A window of **600 samples** is too wide; it will encompass three entire beats, making the template overly specific to that exact sequence of three beats rather than serving as a flexible single-beat matcher.
- **(iii) Trade-off:** A short window provides excellent time localization (pinpointing exactly *when* something happens) but lacks frequency resolution (hard to distinguish specific frequency components). A long window accurately captures frequency content but smears timing information. In this time-domain template matching context, an excessively long window smears the boundary of where an anomalous beat starts, while an excessively short one might spuriously match random noise spikes.

### (d) Match the Template (Correlation)
- **(i) Range and Perfect Match:** The normalized correlation score $\rho(m)$ ranges from $-1$ to $1$. A near-perfect match is signaled by a value close to $+1$.
- **(ii) Importance of Normalization:** Without normalization, the dot product $\sum t[k] x[m+k]$ simply scales with the amplitude of the signal. If a healthy beat happened to be twice as tall due to baseline wander or amplitude drift, the un-normalized score would double, potentially exceeding any threshold and confusing the logic. Normalization divides by the energy, factoring out amplitude scale entirely, so it strictly measures *shape similarity*.
- **(iii) Inverted Beats:** For an inverted beat, the shape is flipped, resulting in a strong negative correlation. We would expect $\rho$ to be roughly $-1$. This makes inverted beats exceptionally easy to flag because they drop far below typical positive correlation thresholds.

### (e) Onset Detection & The Spectrogram
- **(i) Simple Rule:** Maya can declare the onset time as the first index $m$ where $\rho(m) < 0.5$. **Trade-off:** A threshold too high (e.g., 0.95) is too sensitive and might falsely flag minor natural variations (false positive). A threshold too low (e.g., 0.1) might miss the beginning of an arrhythmia entirely (false negative).
- **(ii) Spectrogram Differences:** In the healthy region, the spectrogram will show clean, steady, horizontal parallel lines (harmonic bands) at multiples of the fundamental frequency. In the arrhythmia region, the timing irregularity destroys the clear periodicity, causing the distinct harmonic bands to blur, shift chaotically, or merge into broadband vertical smudges corresponding to erratic, non-periodic beats.
- **(iii) Disagreement:** The correlation plot evaluates exact timing sample-by-sample (or beat-by-beat) in the time domain, offering extreme precision. The spectrogram relies on a sliding window (e.g., 600 samples), which inherently blurs time resolution across the width of the window. I would trust the **correlation plot** to pinpoint the single exact moment the bad beat appears, as it is immune to the time-frequency trade-off blurring present in the spectrogram.

### (f) Sampling & Aliasing
- **(i) Nyquist Theorem:** To capture content up to 40 Hz without aliasing, the minimum sampling rate must be strictly greater than $2 \times f_{max} = 2 \times 40 = 80$ Hz.
- **(ii) Aliasing at 50 Hz:** Sampling at 50 Hz violates the Nyquist rate for 40 Hz content. High frequencies (e.g., the 40 Hz components of the QRS spike) will "fold back" and appear as low frequencies (at $50 - 40 = 10$ Hz). This distorts the shape of the sharp QRS spikes, smearing and broadening them. This is dangerous because Maya's template detector relies on the precise, sharp shape of the QRS complex; aliased distortion will drastically lower the correlation score, triggering false arrhythmia alarms.
- **(iii) Fix and Cost:** To fix aliasing before sampling at 50 Hz, an analog **Anti-Aliasing (Low-Pass) Filter** must be applied to strictly cut off all frequencies above the Nyquist frequency ($25$ Hz). The unavoidable cost is that the clinically important sharp features of the QRS complex (the 25-40 Hz content) are permanently lost, resulting in a visibly rounded and less diagnostically useful ECG signal.

---
*Note: The Jupyter Notebooks `Q1_Submission.ipynb` and `Q2_Submission.ipynb` contain the fully implemented code that generates the figures and results supporting this report.*
return this in .tex