Q1A. Frequency Forensics
‘The Ghost Signal’ [3%]
In intelligence and surveillance systems, infor-
mation is often transmitted through hostile envi-
ronments where signals may be intentionally cor-
rupted to prevent unauthorized access. Imagine
that a reconnaissance satellite intercepts a grayscale
image suspected to contain critical information.
Unfortunately, the received image appears heavily
distorted by a repetitive pattern, making the orig-
inal content nearly impossible to recognize. Intel-
ligence analysts believe that the image contains an
important question whose answer may reveal the
next stage of the mission. However, before the ques-
tion can be answered, it must first be recovered
from the corruption. To an observer in the spatial
domain, the image looks corrupted beyond repair.
However, a signal processing engineer knows that
periodic interference leaves unique fingerprints in
the frequency domain.

An image I(x,y) is a finite two-dimensional dis-
crete signal containing intensity variations along
both spatial directions. Since periodic disturbances
correspond to specific frequency components, ana-
lyzing the image in the Fourier domain may reveal
the source of corruption. By transforming the im-
age into the frequency domain, can you identify sig-
natures of the unwanted interference?
 What mathematical equations govern the two-dimensional Dis-
crete Fourier Transform (DFT) and its inverse?
 If you plot the magnitude spectrum of the given image
in both linear and dB scales, where are the domi-
nant spectral components located?
 Is the spectrum naturally centered, and if not, how can it be shifted
to place the lower frequencies at the center of the
transform?

The interference has been deliberately intro-
duced in such a way that only a few frequency com-
ponents are responsible for the corruption. Can
you locate these components in the spectrum?
How do they differ from the frequencies associ-
ated with the actual image content? Design a suit-
able frequency-domain system capable of suppress-
ing the unwanted frequencies while preserving the
useful information. Carefully analyze how periodic
noise manifests itself in the Fourier domain and jus-
tify the frequencies selected for removal.
After filtering, reconstruct the image using the
inverse Fourier transform. Has the hidden mes-
sage been successfully recovered? Compare the cor-
rupted image, its frequency spectrum, the filtered
spectrum, and the recovered image. How does the
choice of filter parameters affect the quality of re-
construction? Does removing more frequencies al-
ways improve the result, or can it also destroy useful
information? Discuss your observations and com-
ment on practical applications of frequency-domain
image restoration in communication systems, re-
mote sensing, surveillance and medical imaging.
This is known as a Frequency-Domain Image Re-
covery System. Use the ghost signal input im-
age as an input to this system.
Q1B. Digital Detective
‘Missing Boundaries’ [2%]
Figure 1: Edge detector system: input & output
Humans can effortlessly recognize faces, vehi-
cles, roads, handwritten text and everyday ob-
jects, often within a fraction of a second. Sur-
prisingly, much of this ability comes from identi-
fying boundaries where intensity changes abruptly.
These boundaries, known as edges, contain a signifi-
cant portion of the structural information present in
an image. Modern technologies such as autonomous
vehicles, medical imaging systems, facial recogni-
tion software and industrial inspection tools all rely
on the ability to detect and analyze edges accu-
rately. Image I(x,y) is a finite two-dimensional
discrete signal whose intensity varies in both spatial
directions. Abrupt intensity transitions often cor-
respond to object boundaries and therefore contain
valuable information about the scene. What math-
ematical operation can be used to identify regions
where intensity changes rapidly? How are deriva-
tives and gradients related to edge detection? Ex-
plore the concepts behind the Sobel filter, which
is used for 2D convolution operation on images to
detect edges.
Using the given image, apply the Sobel ker-
nel to reveal the hidden boundaries within the
scene. How does noise affect the detected bound-
aries, and what role does image smoothing play
before edge extraction? Can weak edges be pre-
served without introducing excessive noise? Use
missing boundaries input image for your com-
plete analysis

EVALUATION AND SUBMISSION --------------------------

Submission and Evaluation Guidelines for
Q1A and Q1B
•Evaluation Scheme: 40% marks will be
awarded for the final results, analysis and cor-
rectness of the output, while 60% marks will
be awarded for the methodology, implemen-
tation process, explanations, justification of
approaches and the quality of the project re-
port.

•Submission Requirements: Submit a
Jupyter Notebook (.ipynb) containing the
complete implementation and answers to all
the sub-questions, along with a project report
(PDF) containing the methodology, plots, ob-
servations and final results.

•Dataset Usage Policy: Only the provided
images must be used as inputs for the assign-
ment, and all results must be obtained from
the given dataset. The use of AI-generated
or externally generated images is strictly pro-
hibited and will attract a strict penalty.

•Report Expectations: The report should
include relevant plots, intermediate observa-
tions, comparisons, discussions and final con-
clusions. Marks will be awarded for both the
quality of the results and the reasoning used
to obtain them, not just the final output.