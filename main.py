import numpy as np
import scipy.signal as signal
from scipy.ndimage import median_filter
from skimage.restoration import denoise_nl_means, estimate_sigma
import matplotlib.pyplot as plt

# -------------------------------
# 1. Preprocessing
# -------------------------------
def preprocess_ecg(ecg_signal, kernel_size=5):
    return median_filter(ecg_signal, size=kernel_size)


# -------------------------------
# 2. S-Transform (STFT Approx)
# -------------------------------
def s_transform(signal_data, fs=360):
    # smaller window → more time samples → avoids filtfilt error
    f, t, Zxx = signal.stft(signal_data, fs=fs, nperseg=64)
    return f, t, Zxx


# -------------------------------
# 3. Inverse STFT
# -------------------------------
def inverse_s_transform(Zxx, fs=360):
    _, x_rec = signal.istft(Zxx, fs=fs)
    return x_rec


# -------------------------------
# 4. Robust EMD (FIXED)
# -------------------------------
def emd_decompose(signal_data, max_imfs=3):

    imfs = []
    residue = signal_data.copy()

    # handles short signals safely
    if len(signal_data) < 15:
        return [signal_data], np.zeros_like(signal_data)

    for _ in range(max_imfs):
        b, a = signal.butter(3, 0.1, btype='high')

        try:
            imf = signal.filtfilt(b, a, residue)
        except ValueError:
            # fallback if filtering fails
            imf = residue.copy()

        imfs.append(imf)
        residue = residue - imf

    return imfs, residue


# -------------------------------
# 5. NLM Filtering
# -------------------------------
def nlm_filter(signal_1d):
    image = signal_1d.reshape(1, -1)

    sigma_est = np.mean(estimate_sigma(image, channel_axis=None))

    denoised = denoise_nl_means(
        image,
        h=1.15 * sigma_est,
        fast_mode=True,
        patch_size=3,
        patch_distance=5
    )

    return denoised.flatten()

def compute_mse(original, denoised):
    min_len = min(len(original), len(denoised))
    original = original[:min_len]
    denoised = denoised[:min_len]

    return np.mean((original - denoised) ** 2)

# -------------------------------
# 6. Main Pipeline
# -------------------------------
def ecg_denoising_pipeline(ecg_signal, fs=360):

    # Step 1
    clean_signal = preprocess_ecg(ecg_signal)

    # Step 2
    f, t, Zxx = s_transform(clean_signal, fs)

    # Step 3
    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)

    denoised_magnitude = np.zeros_like(magnitude)

    #  Speed optimization: skip rows
    for i in range(0, magnitude.shape[0], 2):

        imfs, residue = emd_decompose(magnitude[i, :])

        filtered_imfs = [nlm_filter(imf) for imf in imfs]

        denoised_row = np.sum(filtered_imfs, axis=0) + residue
        denoised_magnitude[i, :] = denoised_row

        # fill skipped row
        if i + 1 < magnitude.shape[0]:
            denoised_magnitude[i + 1, :] = denoised_row

    # Step 4
    Zxx_denoised = denoised_magnitude * np.exp(1j * phase)

    # Step 5
    reconstructed_signal = inverse_s_transform(Zxx_denoised, fs)

    #  Fix length mismatch
    reconstructed_signal = reconstructed_signal[:len(ecg_signal)]

    return reconstructed_signal


# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":

    print("Generating signal...")

    t = np.linspace(0, 1, 360)
    ecg = np.sin(2 * np.pi * 5 * t) + 0.5 * np.random.randn(len(t))

    print("Running pipeline...")
    denoised = ecg_denoising_pipeline(ecg)

    print("Plotting...")

    min_len = min(len(ecg), len(denoised))

    plt.figure(figsize=(10, 4))
    plt.plot(ecg[:min_len], label="Noisy ECG")
    plt.plot(denoised[:min_len], label="Denoised ECG")
    plt.legend()
    plt.title("ECG Denoising using ST + EMD + NLM")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()

    mse_value = compute_mse(ecg, denoised)
    print("MSE:", mse_value)
