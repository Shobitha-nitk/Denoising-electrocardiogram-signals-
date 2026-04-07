import numpy as np
import scipy.signal as signal
from scipy.ndimage import median_filter
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import wfdb
import time

# -------------------------------
# 1. LOAD REAL ECG (MIT-BIH)
# -------------------------------
def load_ecg():
    print("Loading MIT-BIH ECG...")
    try:
        record = wfdb.rdrecord('100', pn_dir='mitdb')
        ecg = record.p_signal[:, 0]
    except Exception as e:
        print(f"Error loading MITDB: {e}. Generating synthetic signal.")
        # Synthetic ECG-like signal
        t_syn = np.linspace(0, 1, 1000)
        ecg = np.sin(2 * np.pi * 5 * t_syn) + 0.5 * np.sin(2 * np.pi * 50 * t_syn)
        
    ecg = (ecg - np.mean(ecg)) / np.std(ecg)
    return ecg[:1000]

# -------------------------------
# 2. PREPROCESSING
# -------------------------------
def preprocess_ecg(ecg_signal):
    ecg = median_filter(ecg_signal, size=5)
    ecg = signal.detrend(ecg)
    return ecg

# -------------------------------
# 3. S-TRANSFORM (STFT)
# -------------------------------
def s_transform(signal_data, fs=360):
    f, t, Zxx = signal.stft(signal_data, fs=fs, nperseg=128)
    return f, t, Zxx

def inverse_s_transform(Zxx, fs=360):
    _, x_rec = signal.istft(Zxx, fs=fs)
    return x_rec

# -------------------------------
# 4. PIPELINE
# -------------------------------
def ecg_denoising_pipeline(ecg_signal):
    clean_signal = preprocess_ecg(ecg_signal)

    # Transform
    f, t, Zxx = s_transform(clean_signal)
    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)

    # NLM Denoising on the 2D Spectrogram
    sigma_est = np.mean(estimate_sigma(magnitude, channel_axis=None))
    denoised_magnitude = denoise_nl_means(
        magnitude,
        h=1.2 * sigma_est,
        fast_mode=True,
        patch_size=5,
        patch_distance=6,
        channel_axis=None
    )

    # Reconstruct
    Zxx_denoised = denoised_magnitude * np.exp(1j * phase)
    reconstructed_signal = inverse_s_transform(Zxx_denoised)

    # Return everything needed for plotting
    return reconstructed_signal[:len(ecg_signal)], Zxx, Zxx_denoised, f, t

# -------------------------------
# 5. METRICS
# -------------------------------
def compute_metrics(clean, denoised):
    min_len = min(len(clean), len(denoised))
    clean = clean[:min_len]
    denoised = denoised[:min_len]

    noise = clean - denoised
    mse = np.mean(noise**2)
    rmse = np.sqrt(mse)
    snr = 10 * np.log10(np.sum(clean**2) / np.sum(noise**2))
    prd = 100 * np.sqrt(np.sum(noise**2) / np.sum(clean**2))
    psnr = 10 * np.log10(np.max(clean)**2 / mse)
    corr = np.corrcoef(clean, denoised)[0, 1]
    ssim_val = ssim(clean, denoised, data_range=clean.max() - clean.min())

    return mse, rmse, snr, prd, psnr, corr, ssim_val

# -------------------------------
# 6. MAIN
# -------------------------------
# -------------------------------
# 6. MAIN & PLOTTING
# -------------------------------
if __name__ == "__main__":
    clean = load_ecg()
    noise = 0.3 * np.random.randn(len(clean))
    noisy_ecg = clean + noise

    print("Running optimized pipeline...")
    start = time.time()
    denoised, Zxx, Zxx_denoised, f, t = ecg_denoising_pipeline(noisy_ecg)
    end = time.time()

    min_len = min(len(clean), len(denoised))

    # --- PLOT 1: COMPARISON (Clean vs Noisy) ---
    plt.figure(figsize=(12, 4))
    plt.plot(clean[:min_len], label="Original Clean Signal", color='blue', alpha=0.7)
    plt.plot(noisy_ecg[:min_len], label="Noisy Input", color='red', alpha=0.5)
    plt.title("Input: Original Signal vs. Added Noise")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # --- PLOT 2: THE DENOISED SIGNAL (Standalone) ---
    plt.figure(figsize=(12, 4))
    plt.plot(denoised[:min_len], label="Denoised ECG", color='#007acc', linewidth=1.5)
    plt.title("Output: Cleaned/Denoised ECG Signal")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # --- PLOT 3: SPECTROGRAMS ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))
    
    # Noisy Magnitude
    im1 = ax1.pcolormesh(t, f, np.abs(Zxx), shading='gouraud', cmap='magma')
    ax1.set_title("Noisy Spectrogram")
    fig.colorbar(im1, ax=ax1)
    
    # Denoised Magnitude
    im2 = ax2.pcolormesh(t, f, np.abs(Zxx_denoised), shading='gouraud', cmap='magma')
    ax2.set_title("Denoised Spectrogram")
    fig.colorbar(im2, ax=ax2)
    
    plt.tight_layout()
    plt.show()

 
  # --- METRICS ---
    mse, rmse, snr, prd, psnr, corr, ssim_val = compute_metrics(clean, denoised)
    
    print("\n" + "="*40)
    print("       ECG DENOISING PERFORMANCE")
    print("="*40)
    print(f"Execution Time:     {end - start:.4f}s")
    print("-" * 40)
    
    # Fidelity Metrics
    print(f"MSE:                {mse:.6f}")
    print(f"RMSE:               {rmse:.6f}")
    print(f"Correlation (R):    {corr:.4f}")
    print(f"SSIM Score:         {ssim_val:.4f}")
    
    print("-" * 40)
    
    # Quality/Power Metrics
    print(f"SNR Improvement:    {snr:.2f} dB")
    print(f"PSNR:               {psnr:.2f} dB")
    print(f"PRD (Distortion):   {prd:.2f}%")
    
    print("="*40)
