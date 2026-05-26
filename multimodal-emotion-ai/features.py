"""
Shared feature extraction module for audio and video modalities.

This module centralizes feature extraction logic used across audio_model.py,
video_model.py, and fusion.py to eliminate code duplication and ensure
consistency across the pipeline.

Author: Somtochukwu C. Osigwe-Daniel
Module: COMP40781 Artificial Perception
"""

import numpy as np
import pandas as pd
import librosa
from pathlib import Path


# Emotion mapping from RAVDESS filename convention
EMOTION_MAP = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgusted",
    "08": "surprised"
}

# Video feature column definitions
LANDMARK_COLS = [f"x_{i}" for i in range(68)] + [f"y_{i}" for i in range(68)]
HEADPOSE_COLS = ["Pitch", "Roll", "Yaw"]
AU_COLS = [
    "AU01", "AU02", "AU04", "AU05", "AU06", "AU07", "AU09", "AU10",
    "AU11", "AU12", "AU14", "AU15", "AU17", "AU20", "AU23", "AU24",
    "AU25", "AU26", "AU28", "AU43"
]
VIDEO_FEATURE_COLS = LANDMARK_COLS + HEADPOSE_COLS + AU_COLS


def extract_audio_features(filepath, n_mfcc=20):
    """
    Extract audio features from a WAV file.

    Features extracted:
    - MFCC (Mel-Frequency Cepstral Coefficients): mean and std across time
    - F0 (Fundamental Frequency): mean and std
    - RMS Energy: mean and std
    - Zero-Crossing Rate: mean and std

    Args:
        filepath (str or Path): Path to WAV file
        n_mfcc (int): Number of MFCC coefficients (default: 20)

    Returns:
        np.ndarray: Feature vector of shape (4*n_mfcc + 8,)
                   [mfcc_mean, mfcc_std, f0_mean, f0_std, rms_mean, rms_std, zcr_mean, zcr_std]

    Raises:
        FileNotFoundError: If audio file does not exist
        ValueError: If audio cannot be loaded or features cannot be extracted
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Audio file not found: {filepath}")

    try:
        y, sr = librosa.load(filepath, sr=None)
    except Exception as e:
        raise ValueError(f"Failed to load audio from {filepath}: {e}")

    # MFCC features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    mfcc_mean = mfcc.mean(axis=1)
    mfcc_std = mfcc.std(axis=1)

    # Fundamental frequency (F0) using pYIN algorithm
    f0, _, _ = librosa.pyin(y, fmin=50, fmax=500)
    f0 = f0[~np.isnan(f0)]
    f0_mean = f0.mean() if len(f0) > 0 else 0.0
    f0_std = f0.std() if len(f0) > 0 else 0.0

    # RMS Energy
    rms = librosa.feature.rms(y=y)[0]
    rms_mean = rms.mean()
    rms_std = rms.std()

    # Zero-Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    zcr_mean = zcr.mean()
    zcr_std = zcr.std()

    # Concatenate all features
    features = np.concatenate([
        mfcc_mean, mfcc_std,
        [f0_mean, f0_std],
        [rms_mean, rms_std],
        [zcr_mean, zcr_std]
    ])

    return features


def extract_video_features(filepath):
    """
    Extract video features from a FELT CSV file.

    Features extracted:
    - Facial landmarks: 68 points × 2 coordinates (x, y)
    - Head pose: Pitch, Roll, Yaw angles
    - Action Units: 20 facial action units

    For each feature, computes mean and std across all frames.

    Args:
        filepath (str or Path): Path to FELT CSV file

    Returns:
        np.ndarray: Feature vector of shape (2 * len(VIDEO_FEATURE_COLS),)
                   [feature_means, feature_stds]

    Raises:
        FileNotFoundError: If CSV file does not exist
        ValueError: If no valid feature columns found or no valid frames after cleaning
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Video feature file not found: {filepath}")

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Failed to load CSV from {filepath}: {e}")

    # Select available feature columns
    available_cols = [c for c in VIDEO_FEATURE_COLS if c in df.columns]
    if not available_cols:
        raise ValueError(f"No expected feature columns found in {filepath}")

    # Convert to numeric and drop NaN rows
    data = df[available_cols].apply(pd.to_numeric, errors="coerce").dropna()
    if len(data) == 0:
        raise ValueError(f"No valid frames after dropping NaN rows in {filepath}")

    # Compute mean and std across frames
    means = data.mean().values
    stds = data.std().values

    # Concatenate means and stds
    features = np.concatenate([means, stds])

    return features


def parse_ravdess_files(data_dir):
    """
    Parse RAVDESS audio files and extract emotion labels from filenames.

    RAVDESS filename format: [Actor][Emotion][Intensity][Statement][Repetition][Take].wav
    We extract the emotion code (position 2) and map it to emotion labels.

    Args:
        data_dir (str or Path): Directory containing RAVDESS WAV files

    Returns:
        tuple: (filepaths, labels) where:
            - filepaths: list of Path objects to WAV files
            - labels: list of emotion labels (str)
    """
    data_dir = Path(data_dir)
    filepaths, labels = [], []

    for wav in sorted(data_dir.rglob("*.wav")):
        parts = wav.stem.split("-")
        if len(parts) >= 3:
            emotion_code = parts[2]
            if emotion_code in EMOTION_MAP:
                filepaths.append(wav)
                labels.append(EMOTION_MAP[emotion_code])

    return filepaths, labels


def parse_felt_files(data_dir):
    """
    Parse FELT video feature files and extract emotion labels from filenames.

    FELT filename format: [Actor]-[VocalChannel]-[Emotion]-[Intensity]-[Statement]-[Repetition].csv
    We extract the emotion code (position 2) and filter for speech (VocalChannel="01").

    Args:
        data_dir (str or Path): Directory containing FELT CSV files

    Returns:
        tuple: (filepaths, labels) where:
            - filepaths: list of Path objects to CSV files
            - labels: list of emotion labels (str)
    """
    data_dir = Path(data_dir)
    filepaths, labels = [], []

    for csv in sorted(data_dir.rglob("*.csv")):
        parts = csv.stem.split("-")
        if len(parts) >= 3:
            vocal_channel = parts[1]  # "01" = speech, "02" = song
            emotion_code = parts[2]
            # Only include speech (vocal_channel == "01")
            if vocal_channel == "01" and emotion_code in EMOTION_MAP:
                filepaths.append(csv)
                labels.append(EMOTION_MAP[emotion_code])

    return filepaths, labels
