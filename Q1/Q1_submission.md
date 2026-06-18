# EE200: Signals, Systems and Networks
## Course Project Report
**Topic:** Frequency Forensics and  Digital Detective

---

## Q1A. Frequency Forensics - ‘The Ghost Signal’

### 1. Mathematical Equations of 2D DFT
The two-dimensional Discrete Fourier Transform (2D DFT) of an $M \times N$ image $I(x, y)$ is given by:
$$ F(u, v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} I(x, y) e^{-j 2\pi (\frac{ux}{M} + \frac{vy}{N})} $$
The Inverse 2D DFT is given by:
$$ I(x, y) = \frac{1}{MN} \sum_{u=0}^{M-1} \sum_{v=0}^{N-1} F(u, v) e^{j 2\pi (\frac{ux}{M} + \frac{vy}{N})} $$

### 2. Spectral Components and Centering
If we plot the magnitude spectrum of the given image, the dominant spectral components (representing the core structure and large uniform regions of the image) are naturally located at the **corners** of the 2D transform array ($u=0, v=0$). The spectrum is **not naturally centered**. To place the lower frequencies at the center (which makes it easier to visualize and interpret radially), we shift the zero-frequency component to the center of the spectrum using the `fftshift` operation.

### 3. Locating and Filtering the Corruption
The periodic interference manifests itself as symmetric bright dots (spikes) located away from the center in the shifted magnitude spectrum. These represent high-energy, specific frequency patterns distinct from the continuous low-frequency blob of the natural image content. We locate these frequencies by identifying the maximum local peaks in the magnitude spectrum outside the central DC region. By applying a **Notch Filter** (setting the Fourier coefficients at these specific coordinates to zero), we suppress the unwanted frequencies while preserving the useful information.

### 4. Observations and Practical Applications
Removing the identified interference spikes significantly cleans the image upon reconstruction via Inverse DFT. Removing *too many* frequencies (a larger notch radius) or removing incorrect frequencies can destroy useful structural information, leading to blurring or ringing artifacts in the recovered image. 
**Practical Applications:** Frequency-domain image restoration is widely used in medical imaging (e.g., removing MRI artifacts), remote sensing (removing periodic noise from satellite sensor interference), and communications (suppressing narrow-band jamming signals).

---

## Q1B. Digital Detective - ‘Missing Boundaries’

### 1. Mathematical Foundation of Edge Detection
To identify regions where intensity changes rapidly, we use **spatial differentiation**. The first-order derivative of a 2D image is mathematically represented by its gradient $\nabla I$:
$$ \nabla I = \begin{bmatrix} g_x \\ g_y \end{bmatrix} = \begin{bmatrix} \frac{\partial I}{\partial x} \\ \frac{\partial I}{\partial y} \end{bmatrix} $$
Edges correspond to local maxima in the gradient magnitude. The Sobel filter approximates this derivative by performing a 2D convolution with specific $3 \times 3$ kernels ($S_x$ and $S_y$), which simultaneously compute the derivative and apply slight smoothing perpendicular to the derivative direction.



---
*Note: The Jupyter Notebooks `Q1_Submission.ipynb` contain the fully implemented code that generates the figures and results supporting this report.*
