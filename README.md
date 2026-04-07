# ECG Denoising using STFT, EMD, and Non-Local Means Filtering

# Overview

This project presents a hybrid signal processing pipeline for denoising Electrocardiogram (ECG) signals. The approach combines time-frequency analysis, signal decomposition, and advanced filtering techniques to effectively suppress noise while preserving important morphological features of the ECG waveform.

The implemented method integrates:

* Short-Time Fourier Transform (STFT) as an approximation to the S-transform
* Empirical Mode Decomposition (EMD)
* Non-Local Means (NLM) filtering


# Objectives

* Remove noise from ECG signals while preserving signal characteristics
* Explore hybrid denoising using time-frequency and decomposition methods
* Evaluate performance using quantitative metrics such as Mean Squared Error (MSE)


# Methodology

The proposed pipeline consists of the following stages:

1. Preprocessing

   * Median filtering is applied to reduce impulsive noise.

2. Time-Frequency Transformation

   * The ECG signal is transformed using STFT to obtain a time-frequency representation.

3. Magnitude-Phase Separation

   * The complex STFT output is separated into magnitude and phase components.

4. Signal Decomposition (EMD)

   * The magnitude is decomposed into Intrinsic Mode Functions (IMFs) using a simplified EMD approach.

5. Denoising (NLM Filtering)

   * Each IMF is denoised using Non-Local Means filtering.

6. Reconstruction

   * Filtered IMFs are recombined.
   * The denoised magnitude is combined with the original phase.

7. Inverse Transformation

   * The denoised signal is reconstructed using inverse STFT.


# Project Structure

```
ecg-denoising/
│
├── ecg_denoising_pipeline.py   # Main implementation
├── README.md                   # Project documentation
```

# Results

![Output](https://github.com/user-attachments/assets/fa464a65-c171-47a5-b7c1-5d9ad77f7d16)


The output includes:

* Generates a noisy ECG signal (for demonstration)
* Applies the denoising pipeline
* Displays a comparison plot of noisy vs denoised signals
* Computes Mean Squared Error (MSE)
* Visual comparison of noisy and denoised ECG signals
* Quantitative evaluation using MSE

# Future Work
 
* Implement true S-transform
* Use advanced EMD variants (EEMD, CEEMDAN)
* Optimize for real-time processing
* Evaluate using real ECG datasets (e.g., PhysioNet)
* Explore hardware acceleration (FPGA/ASIC)

# Applications

* Biomedical signal processing
* ECG monitoring systems
* Noise reduction in physiological signals


# Citation

Bing P, Liu W, Zhai Z, Li J, Guo Z, Xiang Y, He B and Zhu L (2024) A novel approach for denoising electrocardiogram signals to detect cardiovascular diseases using an efficient hybrid scheme. Front. Cardiovasc. Med. 11:1277123. doi: 10.3389/fcvm.2024.1277123



# License

This project is for academic and educational purposes.
EC208 Digital Signal Processing 
National Institute of Technology Surathkal
