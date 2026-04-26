# Lab 4 — EEG Brain-Signal Feature Engineering and Classification

Built a full signal processing and ML pipeline on 36-subject EEG data.
Achieved 95.1% balanced accuracy using Random Forest feature selection
with Logistic Regression.

## Pipeline Stages
1. Raw data ingestion and validation
2. Butterworth bandpass (1-40 Hz) and 50 Hz notch filtering
3. 1-second window segmentation (256 samples x 19 channels)
4. 247-feature extraction: Hjorth parameters, Welch PSD, STFT
5. Three feature selection strategies: MI filter, RFE, RF importance
6. Classifier comparison: LDA, Logistic Regression, Random Forest

## Key Skills
Python, NumPy, SciPy, pandas, scikit-learn, EEG signal processing,
Hjorth parameters, spectral analysis, feature engineering, cross-validation

## Files
- `lab04-eeg-classification.ipynb` — Lab notebook
- `lab-guide.pdf` — Lab instructions
- `data/` — EEG dataset (36 subject CSV files)
