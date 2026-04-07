#  ECG Denoising using STFT + Non-Local Means

##  Overview
This project implements an ECG signal denoising pipeline using:
- Preprocessing (median filtering + detrending)
- Time-frequency transformation via STFT
- Non-Local Means (NLM) denoising on the spectrogram
- Signal reconstruction using inverse STFT

The pipeline is evaluated using standard signal quality metrics.

##  Features
- Loads real ECG data (MIT-BIH dataset via wfdb)
- Falls back to synthetic ECG if dataset unavailable
- Applies noise artificially for testing
- Denoises in time-frequency domain
- Computes multiple performance metrics
- Visualizes signals and spectrograms

##  Project Structure
```
ecg_denoising.py   # Main script (pipeline + plots + metrics)
README.md          # Project documentation
Output files 
```

##  Methodology

### 1. Data Loading
- Loads ECG signal from MIT-BIH database (record 100)
- Normalizes signal
- Uses synthetic signal if dataset fails

### 2. Preprocessing
- Median filter → removes impulsive noise
- Detrending → removes baseline wander

### 3. Transformation
- Short-Time Fourier Transform (STFT)
- Converts signal → time-frequency domain

### 4. Denoising
- Applies Non-Local Means (NLM) on magnitude spectrogram
- Preserves structure while reducing noise

### 5. Reconstruction
- Combines denoised magnitude with original phase
- Uses inverse STFT to reconstruct signal

##  Performance Metrics
- MSE – Mean Squared Error
- RMSE – Root Mean Squared Error
- SNR – Signal-to-Noise Ratio
- PSNR – Peak Signal-to-Noise Ratio
- PRD – Percent Root Difference
- Correlation (R)
- SSIM – Structural Similarity Index

##  Outputs

### Plots:
1. Clean vs Noisy ECG
2. Denoised ECG
3. Spectrogram comparison (Noisy vs Denoised)

### Console Output:
- Execution time
- All performance metrics

##  How to Run

Install dependencies:
pip install numpy scipy matplotlib scikit-image wfdb

Run the script:
python ecg_denoising.py


## Citation
Bing P, Liu W, Zhai Z, Li J, Guo Z, Xiang Y, He B and Zhu L (2024) A novel approach for denoising electrocardiogram signals to detect cardiovascular diseases using an efficient hybrid scheme. Front. Cardiovasc. Med. 11:1277123. doi: 10.3389/fcvm.2024.1277123


Developed as part of EC208 Digital Signal Processing project,
National Institute of Technology Surathkal
