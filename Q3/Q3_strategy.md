# Q3 Solving Strategy — Audio Fingerprinting (Shazam-style identifier)

This is a plan for Q3A (algorithm + report) and Q3B (the deployed app). No code here — just
the order of operations, what each step is actually doing, and the traps that eat people's time.

---

## 0. Before touching code: get the songs

- Download the song library from the course page link. Don't rename the files — the filename
  (no extension) **is** the label your system outputs, and Q3B's `results.csv` is graded
  automatically against exact filenames.
- Pick one song as your running example for the Q3A report (the one with the clearest,
  most "musical" structure — vocals + instruments, not pure noise) so your spectrogram and
  constellation plots actually look interpretable.
- Decide your sample rate up front. 22050 Hz is the standard fingerprinting choice (half of
  44100) — high enough for recognizable structure, low enough that the DFTs stay fast. Resample
  everything (database songs + queries) to this same rate, mono. Mismatched sample rates between
  database and query will silently break matching later, so handle this once, early, and never
  think about it again.

---

## 1. Why a single DFT fails (the setup question)

This part is conceptual, not computational, but don't skip writing it up:

- Take the full song, compute one DFT magnitude, plot it. You'll see which frequencies are
  present overall, but the time axis is gone — a note played in the first second and a note
  played in the last second look identical in this plot if they're the same pitch.
- This motivates the spectrogram: chop the signal into short overlapping windows, DFT each
  window, stack the magnitude columns side by side. Frequency on y-axis, time on x-axis,
  color/brightness = magnitude.
- `scipy.signal.spectrogram` or `stft` does this in one call. Don't hand-roll the windowing loop
  unless you want to also demonstrate you understand it — a sentence in the report saying
  "this is equivalent to manually sliding a window and DFT-ing each slice" covers that.

**Time vs frequency resolution experiment**: run the spectrogram with a short window (e.g.
512 samples) and a long window (e.g. 8192 samples) on the same clip, plot both.
- Short window → you can see fast events (drum hits, onsets) sharply in time, but each frequency
  bin is wide, so the pitch content looks blurry/smeared vertically.
- Long window → frequency bins are narrow (you can resolve close pitches), but a transient like
  a drum hit gets smeared across a wide time region.
- This is the same uncertainty-principle trade-off as Q2(c)(iii) — write it that way explicitly,
  the grader will likely be looking for you to connect the two questions.
- State what window length you settle on for the fingerprinting pipeline itself and why (a
  middle value, typically corresponding to ~20-50ms of audio, is standard — short enough to
  localize peaks in time, long enough to get usable frequency bins).

---

## 2. Peak picking → the constellation map

This is the step most people get wrong by overcomplicating.

- A "peak" here means a point in the spectrogram (time bin, frequency bin) whose magnitude is
  larger than all its neighbors in some local 2D window — a local maximum, not a global threshold.
- `scipy.ndimage.maximum_filter` over the spectrogram magnitude array, then keep only points
  where the original value equals the filtered (max-filtered) value, is the standard trick:
  it finds all local maxima in one vectorized pass without writing a manual nested loop.
- You'll also want a minimum magnitude/amplitude threshold on top of "local max" — otherwise you
  pick up local maxima in pure noise/silence too. Tune this by eye against the plotted
  constellation: you want maybe a few hundred points per song, scattered along the actual musical
  content, not thousands of points from background hiss.
- Plot the constellation: scatter of (time, frequency) points overlaid on (or instead of) the
  spectrogram. This is Figure 3 in the handout — that's literally what you're reproducing.

**Don't** try to find "the N loudest points globally" — that tends to clump all your peaks in
the single loudest moment of the song (e.g. one big drum hit) and miss everything else. Local
maxima within small time-frequency neighborhoods spread peaks across the whole clip, which is
what makes the fingerprint robust to only hearing a few seconds of it.

---

## 3. Hashing: pairing peaks

- For each peak (anchor), look at a small window of nearby peaks that come *after* it in time
  (a "target zone" — e.g. within the next ~1 second and within some frequency band).
- For each (anchor, target) pair, build a hash: `(f1, f2, Δt)` where f1, f2 are the two
  frequencies and Δt is the time gap between them. Store this alongside the anchor's absolute
  time `t1` and the song's label.
- Store all of this as `hash → list of (song_id, t1)` — effectively a dictionary/database where
  the hash is the key. A plain Python dict of lists, or a `defaultdict(list)`, is enough; no need
  for an actual database engine.
- Why pairs and not single peaks: a single peak is just one (time, frequency) value — wildly
  non-unique, tons of songs will have *some* peak near 440 Hz. A pair of peaks plus their time
  gap is a much more specific signature, closer to unique across a large song library. This
  is the answer to the "why pairs are more decisive" question — say it in those terms (single
  peak = low specificity/high collision rate; paired hash = combinatorially more specific).

---

## 4. Matching a query

- Fingerprint the query clip exactly the same way (spectrogram → peaks → hashes).
- For every hash in the query that also exists in the database, you get one or more
  `(song_id, t1_database, t1_query)` matches. Compute `offset = t1_database - t1_query` for each.
- For each candidate song, build a histogram of these offsets. A correct match produces a sharp
  spike at one consistent offset (because the query is literally a time-shifted excerpt of the
  database song — every true matching pair has the *same* time relationship). A wrong song
  produces scattered offsets with no dominant spike, because the few hash collisions that occur
  by chance don't share a consistent time relationship.
- The predicted song = whichever song has the tallest spike in its offset histogram (or, more
  robustly, the song with the highest single histogram bin count, compared across all songs in
  the database).
- Plotting this histogram for one correct and one wrong candidate side by side is a great report
  figure — it visually makes the whole "why this works" argument for you.

**Single-peak matching, for comparison**: redo the same matching logic using single peaks
(e.g. just frequency, or (frequency, time) without pairing) as the "hash." You'll see far more
matches by raw count, but they won't concentrate at one offset — the histogram will be flatter,
and wrong songs may now produce comparable peak counts to the right song. This is the experiment
that demonstrates the specificity point.

---

## 5. Robustness experiments

- **Noise**: add white Gaussian noise at increasing amplitude (control via SNR) to a query clip,
  rerun identification, find the rough SNR where the right song stops winning. Strong peaks
  (loud, sustained tones) survive noise; weak ones get buried, so noise mainly costs you small
  peaks but the dominant structure of the song should survive moderate noise. Plot
  accuracy/confidence (peak histogram height) vs noise level.
- **Pitch shift / time stretch**: shifting pitch (e.g. `librosa.effects.pitch_shift`) moves every
  frequency component, which moves every peak vertically in the spectrogram. Since your hashes
  encode exact frequency values, even a small shift means none of the shifted peaks land on the
  exact frequency bins stored in the database — hash lookups fail even though perceptually the
  song is unchanged. This is the "why a small pitch shift defeats it but sounds the same to you"
  answer: human pitch perception is forgiving/relative, exact-bin hash lookup is not.
- **Suggested robustness fix**: quantize frequencies into bins with some tolerance (or allow
  fuzzy matching within ±1-2 bins) instead of requiring exact equality; or use frequency *ratios*
  between paired peaks instead of absolute frequencies, since ratios are invariant to pitch
  shift. Mention this as the proposed improvement — you don't need to fully implement it, just
  justify why it would help.

---

## Q3B — wrapping it as an app

- **Streamlit** is the easiest path: one Python script, `st.file_uploader` for the query clip,
  cached database loading (`@st.cache_resource` so you don't re-index songs on every interaction),
  and `st.pyplot`/`st.image` to show the spectrogram, constellation, and offset histogram inline.
- **Two modes**, both required:
  - *Single-clip mode*: upload one query, show spectrogram → constellation → offset histogram →
    final predicted song name, in that order, as the demo video presumably shows.
  - *Batch mode*: accept multiple files (`st.file_uploader(..., accept_multiple_files=True)`),
    run the same pipeline silently for each, and write `results.csv` with exactly the two columns
    `filename,prediction` (prediction = matched filename **without extension**). Don't add an
    index column, don't rename headers — the format is graded automatically.
- **Indexing the database**: build the hash database once at deploy time (a setup/build script,
  not something recomputed per request), pickle it, and ship the pickle file alongside the app
  so it loads instantly when the app starts — don't make it re-index the whole song library on
  every cold start.
- **Deployment**: Streamlit Community Cloud is free; push the repo (app code + the pickled
  database file, watch the file size limits) to GitHub, connect it on share.streamlit.io. Test
  the *deployed* link yourself in an incognito window before submitting — broken deploy = zero
  marks per the instructions, so this check is not optional.
- Submit: the live app link, the GitHub source link, and a zip of all code, all in the same PDF
  as instructed.

---

## Suggested order of work

1. Get songs, settle sample rate, pick a demo song.
2. Single-DFT-fails demo + spectrogram with short/long window comparison (write-up only needs
   2-3 plots).
3. Peak picking + constellation plot for one song — visually confirm it looks reasonable before
   building the full database.
4. Build hashing + database indexing for all songs.
5. Matching pipeline + offset histogram, test on a couple of known query clips (correct + a
   deliberately wrong one) to sanity check before robustness tests.
6. Single-peak vs paired-hash comparison.
7. Noise and pitch-shift robustness experiments.
8. Wrap everything into the Streamlit app, two modes, test `results.csv` format against a small
   batch manually.
9. Deploy, verify the live link works, write up the report last (once all plots exist).

Doing the report last is deliberate — the report is 100% "explain what you observed," and you
can't write that honestly until the experiments are actually done and the plots exist in front
of you.
