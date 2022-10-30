from scipy.io import wavfile
import librosa
import librosa.display
import numpy as np
import soundfile as sf


def extract_features(filepath):
    audio, sr = librosa.load(filepath, sr= 32000, mono=True)
    clip = librosa.effects.trim(audio, top_db= 10)
    sf.write('filtered.wav', clip[0], 32000)
    f_s, signal = wavfile.read('filtered.wav')
    n_fft = int(0.025 * f_s)  # 25 ms
    hop_length = int(0.01 * f_s)  # 10 ms
    mel_spec = librosa.feature.melspectrogram(
        y=signal / 1.0, sr=f_s, n_mels=40,
        n_fft=n_fft, hop_length=hop_length
    )
    log_mel_spec = np.log(mel_spec)
    print("Before T")
    print(log_mel_spec.shape)
    return log_mel_spec.T

