import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Audio_Fingerprinting'))

import numpy as np
import librosa
import matplotlib.pyplot as plt
import soundfile as sf
from collections import defaultdict
import pickle

from fingerprint import load_audio, compute_spectrogram, find_peaks, generate_hashes, SAMPLE_RATE, identify

PLOTS_DIR = os.path.join(os.path.dirname(__file__), 'plots')
os.makedirs(PLOTS_DIR, exist_ok=True)

# 1. DFT of entire song
def plot_dft_entire_song(y, sr):
    print("Plotting DFT of entire song...")
    D = np.abs(np.fft.rfft(y))
    freqs = np.fft.rfftfreq(len(y), 1/sr)
    plt.figure(figsize=(10, 4))
    plt.plot(freqs, librosa.amplitude_to_db(D, ref=np.max), alpha=0.8)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('DFT Magnitude of Entire Song (Time structure lost)')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'dft_entire_song.png'))
    plt.close()

# 2. Spectrogram (short vs long window)
def plot_spectrograms(y, sr):
    print("Plotting Spectrograms...")
    clip = y[:sr*5] # 5 seconds for clear visualization
    
    # Short window
    S_short, f_short, t_short = compute_spectrogram(clip, sr=sr, n_fft=512, hop=256)
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(t_short, f_short, S_short, shading='auto', cmap='magma')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram (Short Window: N_FFT=512) - High Time Res, Low Freq Res')
    plt.colorbar(label='Magnitude (dB)')
    plt.ylim(0, 5000)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'spectrogram_short.png'))
    plt.close()
    
    # Long window
    S_long, f_long, t_long = compute_spectrogram(clip, sr=sr, n_fft=8192, hop=4096)
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(t_long, f_long, S_long, shading='auto', cmap='magma')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram (Long Window: N_FFT=8192) - Low Time Res, High Freq Res')
    plt.colorbar(label='Magnitude (dB)')
    plt.ylim(0, 5000)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'spectrogram_long.png'))
    plt.close()

# 3. Constellation Map
def plot_constellation(y, sr):
    print("Plotting Constellation...")
    clip = y[:sr*10] # 10 seconds
    S_db, freqs, times = compute_spectrogram(clip, sr=sr)
    peaks = find_peaks(S_db)
    
    plt.figure(figsize=(12, 5))
    plt.pcolormesh(times, freqs, S_db, shading='auto', cmap='magma', alpha=0.6)
    
    t_peaks = [times[p[0]] for p in peaks]
    f_peaks = [freqs[p[1]] for p in peaks]
    plt.scatter(t_peaks, f_peaks, c='cyan', s=10, marker='x', label='Peaks')
    
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Constellation Map (Peaks overlaid on Spectrogram)')
    plt.ylim(0, freqs[512] if len(freqs)>512 else 5000) # limit to frequency bins used for hashing
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'constellation_map.png'))
    plt.close()

# 4. Offset Histograms (paired hashes)
def plot_offset_histogram_paired(query_y, hash_db):
    print("Plotting offset histogram (paired hashes)...")
    S_db, _, _ = compute_spectrogram(query_y)
    peaks = find_peaks(S_db)
    hashes = generate_hashes(peaks)
    
    offsets = defaultdict(lambda: defaultdict(int))
    for h, tq in hashes:
        if h in hash_db:
            for song, tdb in hash_db[h]:
                offsets[song][tdb - tq] += 1
                
    # Find best song and a wrong song
    scores = {song: max(hist.values()) if hist else 0 for song, hist in offsets.items()}
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_song = ranked[0][0]
    wrong_song = ranked[min(1, len(ranked)-1)][0] if len(ranked)>1 else None
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Best song
    hist_best = offsets[best_song]
    axes[0].bar(hist_best.keys(), hist_best.values(), width=1, color='green')
    axes[0].set_title(f'Correct Match: {best_song}')
    axes[0].set_xlabel('Time Offset (database_time - query_time)')
    axes[0].set_ylabel('Number of Matches')
    
    # Wrong song
    if wrong_song:
        hist_wrong = offsets[wrong_song]
        axes[1].bar(hist_wrong.keys(), hist_wrong.values(), width=1, color='red')
        axes[1].set_title(f'Wrong Match: {wrong_song}')
        axes[1].set_xlabel('Time Offset')
        
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'offset_histogram_paired.png'))
    plt.close()

# 5. Offset Histograms (single peaks)
def plot_offset_histogram_single(query_y, song_dir):
    print("Plotting offset histogram (single peaks)...")
    songs = ["Hey Jude", "Yesterday"]
    single_db = defaultdict(list)
    for name in songs:
        path = os.path.join(song_dir, f"{name}.mp3")
        y = load_audio(path)
        S, _, _ = compute_spectrogram(y)
        pks = find_peaks(S)
        for t, f in pks:
            single_db[f].append((name, t))
            
    S_q, _, _ = compute_spectrogram(query_y)
    pks_q = find_peaks(S_q)
    
    offsets = defaultdict(lambda: defaultdict(int))
    for tq, fq in pks_q:
        if fq in single_db:
            for song, tdb in single_db[fq]:
                offsets[song][tdb - tq] += 1
                
    scores = {song: max(hist.values()) if hist else 0 for song, hist in offsets.items()}
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_song = ranked[0][0] if ranked else "Unknown"
    wrong_song = ranked[1][0] if len(ranked)>1 else None
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    if ranked:
        hist_best = offsets[best_song]
        axes[0].bar(hist_best.keys(), hist_best.values(), width=1, color='blue')
        axes[0].set_title(f'Single Peaks Match: {best_song}')
        axes[0].set_xlabel('Time Offset')
        axes[0].set_ylabel('Number of Matches')
    
    if wrong_song:
        hist_wrong = offsets[wrong_song]
        axes[1].bar(hist_wrong.keys(), hist_wrong.values(), width=1, color='orange')
        axes[1].set_title(f'Single Peaks Match: {wrong_song}')
        axes[1].set_xlabel('Time Offset')
        
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'offset_histogram_single.png'))
    plt.close()

# 6. Robustness to Noise
def plot_robustness_noise(y, sr, hash_db, metadata):
    print("Plotting robustness to noise...")
    snrs = [20, 10, 5, 0, -5, -10]
    accuracy = []
    
    signal_power = np.mean(y**2)
    for snr in snrs:
        noise_power = signal_power / (10 ** (snr / 10))
        noise = np.random.normal(0, np.sqrt(noise_power), len(y))
        y_noisy = y + noise
        res = identify(y_noisy, hash_db, metadata, sr=sr)
        ratio = res['ratio']
        accuracy.append(ratio if ratio != float('inf') else 10)
        
    plt.figure(figsize=(8, 4))
    plt.plot(snrs, accuracy, marker='o', linestyle='-', color='purple')
    plt.gca().invert_xaxis()
    plt.xlabel('SNR (dB) [Decreasing Noise ->]')
    plt.ylabel('Confidence (Score / Runner-up)')
    plt.title('Robustness to White Noise')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'robustness_noise.png'))
    plt.close()

# 7. Robustness to Pitch Shift
def plot_robustness_pitch(y, sr, hash_db, metadata):
    print("Plotting robustness to pitch shift...")
    shifts = [0.0, 0.2, 0.5, 1.0, 2.0]
    scores = []
    
    for shift in shifts:
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=shift)
        res = identify(y_shifted, hash_db, metadata, sr=sr)
        scores.append(res['score'])
        
    plt.figure(figsize=(8, 4))
    plt.plot(shifts, scores, marker='s', linestyle='--', color='brown')
    plt.xlabel('Pitch Shift (Semitones)')
    plt.ylabel('Matches (Score)')
    plt.title('Robustness to Pitch Shifting')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'robustness_pitch.png'))
    plt.close()


if __name__ == "__main__":
    song_dir = os.path.join(os.path.dirname(__file__), 'Audio_Fingerprinting', 'Q3_data')
    db_file = os.path.join(os.path.dirname(__file__), 'Audio_Fingerprinting', 'song_database.pkl')
    meta_file = os.path.join(os.path.dirname(__file__), 'Audio_Fingerprinting', 'song_metadata.pkl')
    
    print("Loading database...")
    with open(db_file, "rb") as f:
        hash_db = pickle.load(f)
    with open(meta_file, "rb") as f:
        metadata = pickle.load(f)
        
    demo_song = "Yesterday.mp3"
    print(f"Loading {demo_song}...")
    y_full = load_audio(os.path.join(song_dir, demo_song))
    
    mid = len(y_full) // 2
    query_clip = y_full[mid:mid + 10*SAMPLE_RATE]
    
    plot_dft_entire_song(y_full, SAMPLE_RATE)
    plot_spectrograms(y_full, SAMPLE_RATE)
    plot_constellation(y_full, SAMPLE_RATE)
    
    y_hey_jude = load_audio(os.path.join(song_dir, "Hey Jude.mp3"))
    query_jude = y_hey_jude[len(y_hey_jude)//2 : len(y_hey_jude)//2 + 10*SAMPLE_RATE]
    
    plot_offset_histogram_paired(query_jude, hash_db)
    plot_offset_histogram_single(query_jude, song_dir)
    
    plot_robustness_noise(query_clip, SAMPLE_RATE, hash_db, metadata)
    plot_robustness_pitch(query_clip, SAMPLE_RATE, hash_db, metadata)
    
    print("Done. All plots saved to Q3/plots/")
