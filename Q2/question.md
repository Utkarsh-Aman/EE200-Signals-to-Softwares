Q2. The Midnight Episode
‘Catching the Arrhythmia’ [7.5%]
Maya is interning this summer at a cardiology lab.
One of the patients was sent home wearing a Holter
monitor, a small portable device that records the
heart’s electrical activity (an ECG) continuously for
many hours while the patient goes about ordinary
life. When the patient came back, his recording
was hours long, and his cardiologist suspects that
at some point during the night his heart slipped
into an arrhythmia: an episode where the steady,
regular heartbeat becomes irregular. Scanning the
whole recording manually is slow and error-prone.
Maya recalls two pictures from her Signals &
Systems class (Figure 2). In a healthy heart (Fig-
ure 2a) the ECG is almost periodic, the same shape
repeats at steady intervals, like a metronome: a
small bump (the P wave), a tall sharp spike (the
QRS complex), and another bump (the T wave).
During an arrhythmia (Figure 2b) this regularity
falls apart: beats arrive too early or too late, spikes
change shape or even point the wrong way, and the
clean repetition is lost.
Maya had completed EE200, so she could devise
an elegant plan. She decided rather than read the
whole signal, she will teach the computer to rec-
ognize one healthy heartbeat, then convolve it with
the recording and check, stretch by stretch, whether
the signal still looks like a healthy beat. Where the
match breaks down, the episode has begun.
Figure 2: ECG: Electro-Cardio-Grams
The recording. The clip Maya is studying is a
discrete-time signal x[n] sampled at fs= 250 Hz,
and it is having N = 5000 samples. In the early
(healthy) portion, the heart beats with metronome
regularity: one full beat {P, QRS, T} arrives at
every 0.8 seconds.
(a) Reading the signal: [0.75%]
(i) How many seconds long is the clip?
(ii) In the healthy stretch, what is the pa-
tient’s heart rate in beats per minute,
and how many samples does one healthy
beat occupy?
(iii) Treating the healthy ECG as a periodic
signal, what is its fundamental frequency
f0 (in Hz)?
(b) Healthy heart in frequency domain: [0.75%]
(i) As the healthy ECG is (nearly) peri-
odic, what does its magnitude spectrum
|X(f)| look like, a smooth continuous
curve, or something else?
(ii) The QRS spike is sharp and narrow; the
P and T waves are broad and smooth.
Which of these is responsible for the
higher-frequency content of the ECG,
and why?
(iii) Suppose the patient’s heart rate rises
to 150 bpm but stays perfectly regular.
What happens to f0, and to the spac-
ing between the components in the spec-
trum?
(c) Cutting a heartbeat (windowing): [1.0%]
To build her template, Maya multiplies the
signal by a rectangular window, a function
equal to 1 inside some interval [n1,n2] and 0
outside, to snip out a segment.
(i) To capture exactly one full beat, how
wide (in samples) should the window
be, and roughly where in the recording
should she place it?
(ii) She first tries a window only 80 sam-
ples wide, then one 600 samples wide.
For the purpose of making a clean ‘one
healthy beat’ template, explain what
goes wrong in each case.
(iii) In class you saw that a short window
gives sharp time resolution but poor
frequency resolution, while a long win-
dow does the reverse. In one or two
sentences, relate that same trade-off to
Maya’s choice here: why isn’t ‘make the
window as short as possible’ automati-
cally the best idea?
(d) Match the template (correlation): [1.5%]
Let the template (one healthy beat) be t[k]
for k = 0,1,...,L −1. Sliding it to start at
position m, Maya compares it with the seg-
ment x[m],x[m+ 1],...,x[m+ L−1] using a
normalized correlation score as,
ρ(m) =
∑
kt[k] x[m + k]
∥t∥∥xm∥
where ∥·∥ is the energy (root-sum-of-squares)
of a segment. (You do not need to compute
this by hand, just reason about it.) Intu-
itively, ρ(m) measures how similar in shape
the template and the segment are.
(i) What range of values can ρ(m) take, and
what value signals a near-perfect match?
(ii) Real ECG amplitude drifts slowly up
and down over time (this drift is called
baseline wander), and beats vary in
size. Why is the normalization (divid-
ing by the energies) important? In par-
ticular, what would happen to an un-
normalized score ∑
kt[k]x[m+k] if a per-
fectly healthy beat happened to be twice
as tall as the template?
(iii) During the arrhythmia, one abnormal
beat is inverted (flipped upside-down)
relative to the template. Roughly what
value of ρ would you expect for it, and
why does that make inverted beats espe-
cially easy to flag?
(e) Onset detection & the spectrogram: [1.5%]
Maya computes ρ(m) at every position across
the 20-second clip and plots ρ against time. In
the healthy region, it reaches 1; somewhere it
drops and sometimes strongly negative.
(i) Propose a simple rule Maya could use to
declare an onset time for the arrhythmia.
Then discuss the trade-off in setting her
threshold too high versus too low.
(ii) A labmate suggests a second, indepen-
dent view: a spectrogram of the whole
clip (slide a window along the signal,
take the DFT of each windowed piece,
and stack the results as columns over
time). Describe how the spectrogram
would look different in the healthy re-
gion versus the arrhythmia region.
(iii) The correlation plot and the spectro-
gram might disagree slightly on the ex-
act onset time. Explain why, and men-
tion which one you would trust to pin-
point the single moment a bad beat first
appears. (Hint: think back to the trade-
off in part (c).)
(f) sampling & aliasing: [0.5%]
To make wearable’s battery last longer, an en-
gineer proposes recording at only f′s= 50 Hz
instead of 250 Hz. The clinically important
sharp features of the QRS complex contain
frequency content up to about 40 Hz.
(i) By the Nyquist theorem, what minimum
rate is needed to capture content up to
40 Hz without aliasing?
(ii) In plain words, what would aliasing do to
the sharp QRS spikes at 50 Hz, and why
is that dangerous for Maya’s detector?
(iii) If the team really must lower the sam-
pling rate, what is the fix, and what is
the unavoidable cost of it for an ECG?
(g) Prototyping the detector in code: [1.5%]
Maya wants to test her logic on her lap-
top. She has exported the 5000 sample
recording into a file called patient ecg.npy,
and her clean 200-sample template
into template.npy. Write a Python
code find onset(ecg signal, template,
threshold) that:
(1) Calculates the normalized correlation
score ρ for the signal beat-by-beat (i.e.,
jumping forward by the length of the
template each time, not sample-by-
sample).
(2) Identifies and returns the index m of
the very first beat where the correla-
tion drops strictly below the provided
threshold (assume a threshold of 0.5).
If it is never breached, return -1.
(h) Visualizing the Spectrogram: [0.5%]
Maya wants to visually verify the arrhythmia
using a spectrogram before running the corre-
lation script. Assume the 5000-sample record-
ing is loaded as a 1D NumPy array called
ecg signal. Using the scipy.signal and
matplotlib.pyplot libraries, write a brief
Python snippet to compute and plot the spec-
trogram of the recording.
Crucial step: Based on your reasoning in
part (e), choose a specific window length
(nperseg) in samples that will successfully re-
veal the steady horizontal harmonic bands in
the healthy region. State the window length
you chose and briefly comment (1 sentence)
on why you picked that exact number.

-------------------------------------

Submission and Evaluation Guidelines for
Q2 (all parts)
•Submission Requirements: Submit a
Jupyter Notebook (.ipynb) containing the
complete implementation and answers to all
the sub-questions, along with a project report
(PDF) containing the explainations, plots,
observations and final results.
•Clarity of Responses: Responses should be
concise and directly address the core problem.
Please avoid extraneous details and overly
lengthy explanations.
•Dataset and Reporting: Analysis must
be conducted exclusively using the provided
dataset. Additionally, all generated plots, fig-
ures, and explainations must be embedded di-
rectly within the final report file.