# Quick Start Guide

**COMP40781 Artificial Perception Coursework**  
**Multimodal Emotion Recognition System**

---

## 30-Second Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run pipeline (datasets auto-download on first run)
python main.py
```

**That's it!** Results saved to `results/` directory.

---

## What Happens

### Stage 1: Data Download (~5 minutes)
- RAVDESS audio (~215 MB) downloads from Zenodo
- FELT video features (~945 MB) downloads from Zenodo
- Files cached locally for future runs

### Stage 2: Audio Training (~3 minutes)
- Extracts MFCC features (13, 20, 40 coefficients)
- Trains Random Forest and SVM classifiers
- Generates confusion matrices and reports

### Stage 3: Video Training (~2 minutes)
- Extracts facial landmarks, head pose, action units
- Trains Random Forest and SVM classifiers
- Generates confusion matrices and reports

### Stage 4: Multimodal Fusion (~5 minutes)
- Aligns audio-video pairs
- Trains three fusion strategies:
  1. Weighted probability fusion
  2. Logistic regression meta-classifier
  3. Early-fusion MLP (256→128→64)
- Generates final results and comparison

**Total Time:** ~15 minutes (first run), ~5 minutes (subsequent runs)

---

## Output Files

All results saved to `results/` directory:

```
results/
├── audio_RF_mfcc13_report.txt          # Audio model (RF, 13 MFCC)
├── audio_RF_mfcc13_confusion.png       # Confusion matrix
├── audio_SVM_mfcc20_report.txt         # Audio model (SVM, 20 MFCC)
├── audio_SVM_mfcc20_confusion.png      # Confusion matrix
├── video_RF_report.txt                 # Video model (RF)
├── video_RF_confusion.png              # Confusion matrix
├── fusion_weighted_report.txt          # Weighted probability fusion
├── fusion_weighted_confusion.png       # Confusion matrix
├── fusion_logistic_report.txt          # Logistic regression meta-classifier
├── fusion_logistic_confusion.png       # Confusion matrix
├── fusion_early_report.txt             # Early-fusion MLP
├── fusion_early_confusion.png          # Confusion matrix
└── summary.txt                         # Comparison of all methods
```

---

## Key Results

**Expected Performance:**
- Audio-only (best): ~70% accuracy
- Video-only (best): ~72% accuracy
- **Early-Fusion MLP: ~88.7% accuracy** ← Best result

**Why Fusion Works:**
- Audio captures prosodic information (tone, rhythm)
- Video captures facial expressions and head movements
- Combined: 88.7% vs. 63.2% audio-only and 71.5% video-only

---

## Explore the Code

### Main Entry Point
```python
# main.py — Orchestrates all 4 stages
python main.py
```

### Individual Stages
```python
# Download datasets only
from download_data import download_ravdess, download_felt
download_ravdess("ravdess_data")
download_felt("felt_data")

# Train audio models only
from audio_model import train_audio_model
train_audio_model("ravdess_data")

# Train video models only
from video_model import train_video_model
train_video_model("felt_data")

# Run fusion only
from fusion import late_fusion
summary = late_fusion("ravdess_data", "felt_data")
```

### Extract Features Manually
```python
from features import extract_audio_features, extract_video_features

# Audio features
audio_features = extract_audio_features("path/to/audio.wav", n_mfcc=20)
print(f"Audio shape: {audio_features.shape}")  # (88,)

# Video features
video_features = extract_video_features("path/to/video_features.csv")
print(f"Video shape: {video_features.shape}")  # (318,)
```

---

## Datasets

### RAVDESS (Audio)
- **Source:** https://zenodo.org/records/1188976
- **Size:** ~215 MB
- **Content:** 1,440 audio clips, 24 actors, 8 emotions
- **Format:** WAV files with emotion in filename

### FELT (Video Features)
- **Source:** https://zenodo.org/records/13243600
- **Size:** ~945 MB
- **Content:** Facial landmarks, head pose, action units
- **Format:** CSV files with frame-by-frame features

**Note:** Both datasets auto-download on first run. Subsequent runs use cached copies.

---

## Emotions Recognized

The system classifies 8 emotions:

1. **Neutral** — No emotion
2. **Calm** — Relaxed, peaceful
3. **Happy** — Joyful, positive
4. **Sad** — Sorrowful, melancholic
5. **Angry** — Irritated, hostile
6. **Fearful** — Anxious, scared
7. **Disgusted** — Repulsed, averse
8. **Surprised** — Astonished, shocked

---

## Features Extracted

### Audio Features (per file)
- **MFCC:** 13, 20, or 40 coefficients (mean + std)
- **F0:** Fundamental frequency (mean + std)
- **RMS Energy:** Loudness (mean + std)
- **Zero-Crossing Rate:** Noisiness (mean + std)
- **Total:** 32–86 features

### Video Features (per video)
- **Facial Landmarks:** 68 points × 2 coords (mean + std)
- **Head Pose:** Pitch, Roll, Yaw (mean + std)
- **Action Units:** 20 facial AUs (mean + std)
- **Total:** 318 features

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'librosa'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "FileNotFoundError: ravdess_data not found"
**Solution:** Run download stage first
```python
from download_data import download_ravdess
download_ravdess("ravdess_data")
```

### Issue: "MemoryError" or slow performance
**Solution:** Your system may have limited RAM. The full dataset requires ~4 GB.
- Reduce dataset size by modifying `audio_model.py` and `video_model.py`
- Or run on a machine with more RAM

### Issue: Download fails
**Solution:** Check internet connection and Zenodo availability
```bash
# Manual download
wget https://zenodo.org/records/1188976/files/...
```

---

## Next Steps

### Understand the Code
1. Read `README.md` for detailed documentation
2. Review `features.py` for feature extraction logic
3. Explore `audio_model.py`, `video_model.py`, `fusion.py`
4. Check `main.py` for pipeline orchestration

### Modify & Experiment
1. Change MFCC coefficients: `n_mfcc` parameter
2. Try different classifiers: modify `audio_model.py`, `video_model.py`
3. Adjust fusion weights: modify `fusion.py`
4. Add new features: extend `features.py`

### Deploy
1. Save trained models: `model.save()` or `pickle.dump()`
2. Create REST API: Flask or FastAPI
3. Containerize: Docker
4. Deploy: AWS, GCP, Azure, or on-premises

---

## References

- **RAVDESS Dataset:** Livingstone & Russo (2018), *PLoS ONE*
- **MFCC:** Davis & Mermelstein (1980), *IEEE TASSP*
- **Facial Action Units:** Ekman & Friesen (1978)
- **Multimodal Fusion:** Baltrušaitis et al. (2018), *IEEE TPAMI*

---

## Questions?

- **Documentation:** See `README.md`
- **Code Standards:** See `CONTRIBUTING.md`
- **Contact:** somtoosigwe1@gmail.com

---

**Happy experimenting!** 🎉
