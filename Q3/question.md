Q3A. Sonic Signatures
‘Magical Mystery Tune’ [7.5%]
Figure 3: A spectrogram of a short clip, with the
strongest time-frequency peaks → its constellation
(circled)
You are in a noisy caf ́e when a song you cannot
name starts playing. You ask your music quizzer
friend who also has no idea. So you hold up your
phone, and within seconds it tells you the title,
recognised from a few seconds of sound, over all the
chatter. Remarkably, it never compares the actual
audio waveforms. Instead it turns the music into a
picture of which frequencies are present at each in-
stant, and keeps only a sparse set of standout points
from that picture as the song’s fingerprint. In this
question you will build a small version of this iden-
tifier. First, see why a single Fourier transform will
not do. Plot the DFT magnitude of an entire song:
you can read off which frequencies it contains, but
not when they were played, all sense of timing is
gone. What we really want is a way to watch the
frequency content change as the song plays, and
that is exactly what a spectrogram gives us. The
idea is simple: slide a short window along the signal
and take the Fourier transform of each short slice,
then stack those slices side by side into an image.
Time runs along the horizontal axis, frequency up
the vertical axis, and the brightness of each point
shows how strong that frequency is at that moment:
so a rising note traces a rising streak, a steady tone
a horizontal line. Each slice is nothing more than
an ordinary DFT, the Fourier analysis applied to
one short piece of the signal at a time. Compute
and plot the spectrogram of a provided song. Now
experiment a little: redo it with a short window
and with a long one, and describe what you observe
about the resolution in time versus in frequency.
Next, build the fingerprint. From the spectro-
gram keep only the strongest peaks, the local max-
ima that stand out from their surroundings (the
circled points in Figure 3), and plot this ‘constel-
lation’ of points. Pair the nearby peaks together
into compact hashes (two frequencies and the time
gap between them) and store them in a database
for several provided songs. To identify a new clip,
fingerprint it the same way and, for each song, look
at the time offsets at which its hashes match: a true
match lines them all up at a single offset, while a
wrong song gives only scattered, random matches.
Output the name of the matched song. Then re-
peat the matching using single peaks on their own
instead of pairs, and compare what you get, ex-
plain why joining two peaks into a single fingerprint
makes a correct match so much more decisive.
Now see how robust your identifier is. Add in-
creasing amounts of noise to a query and find how
far you can push it before recognition fails; then
shift the whole clip up in pitch by a little (or stretch
it slightly in time) and try again. Describe what
you see in each case and explain why; in particular,
why a small pitch shift can defeat the identifier even
though the song still sounds the same to you. Sug-
gest one change that would make the system more
robust. Present your spectrograms, plots, and writ-
ten observations in the report.
Q3B. Signals to Softwares
‘Zapp tain America’ [5%]
Wrap your identifier in a simple interactive app,
that a user can run: it should index the provided
songs into a database, accept a new query clip, and
display the recognised song, ideally showing the in-
termediate steps (the spectrogram, the constella-
tion of peaks, and the offset histogram that de-
cides the match). Refer to the provided demo video
showcasing expected functionality for a better idea.

-------------------------------------------------

Submission and Evaluation Guidelines for
Q3 (A) and Q3 (B)
•Submission Requirements: For Q3 (A),
submit your report as a PDF containing the
spectrograms, experiments, observations and
explanations. For Q3 (B), deploy your ap-
plication and submit a link to the live app in
the same PDF, so that we can open and test
it directly: both the single-clip mode and the
batch mode, exactly as a user would use it;
also include a link to its source code. Host-
ing is free and quick on Streamlit Community
Cloud (or a similar service); make sure the in-
dexed song database ships with the deployed
app so it works immediately. Also, submit all
your code in a zip file.
•What to Build → Two Modes: (i) a
single-clip mode that identifies one uploaded
query clip and displays (at the very least) the
intermediate steps: the spectrogram, the con-
stellation of peaks, and the offset histogram
that decides the match; and (ii) a batch mode
that accepts a set of query clips and writes a
file results.csv with exactly two columns,
filename, prediction, where prediction
is the matched song’s filename without ex-
tension. The batch format must be followed
exactly, as it will be evaluated automatically.
Note: If the submitted link does not work
then you will be awarded 0 marks for Q3 (B).
•Song Database: Download the provided
song library from the link on the course web-
page, index it once, and keep the resulting
database. Use the files exactly as provided
and do not rename them: a song’s filename
(without extension) is the label your identi-
fier must output.
•Tools: You do not need prior experience
building apps; lightweight frameworks such as
Streamlit or Gradio let you wrap your func-
tions into a usable app rather easily. You
may use any other frameworks you are famil-
iar with provided the single-clip visuals and
the exact results.csv format are produced.
•Report Expectations: Include the spectro-
grams you computed and, for each experi-
ment: window length; single peaks vs. paired
hashes; added noise; pitch shift / time stretch
→ the relevant plots together with a written
explanation of what you observed and why..