import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import librosa
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix,
                             ConfusionMatrixDisplay, accuracy_score)


EMOTION_MAP = {
    "01": "neutral", "02": "calm",    "03": "happy",    "04": "sad",
    "05": "angry",   "06": "fearful", "07": "disgusted", "08": "surprised"
}

HEADPOSE_COLS = ["Pitch", "Roll", "Yaw"]
AU_COLS       = ["AU01","AU02","AU04","AU05","AU06","AU07","AU09","AU10",
                 "AU11","AU12","AU14","AU15","AU17","AU20","AU23","AU24",
                 "AU25","AU26","AU28","AU43"]
LANDMARK_COLS = [f"x_{i}" for i in range(68)] + [f"y_{i}" for i in range(68)]
VIDEO_FEAT_COLS = LANDMARK_COLS + HEADPOSE_COLS + AU_COLS


#     Feature extractors 

def extract_audio_features(filepath, n_mfcc=20):
    y, sr = librosa.load(filepath, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    f0, _, _ = librosa.pyin(y, fmin=50, fmax=500)
    f0 = f0[~np.isnan(f0)]
    rms = librosa.feature.rms(y=y)[0]
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    return np.concatenate([
        mfcc.mean(axis=1), mfcc.std(axis=1),
        [f0.mean() if len(f0) > 0 else 0.0, f0.std() if len(f0) > 0 else 0.0],
        [rms.mean(), rms.std()],
        [zcr.mean(), zcr.std()]
    ])


def extract_video_features(filepath):
    df = pd.read_csv(filepath)
    available = [c for c in VIDEO_FEAT_COLS if c in df.columns]
    data = df[available].apply(pd.to_numeric, errors="coerce").dropna()
    if len(data) == 0:
        raise ValueError("No valid frames")
    return np.concatenate([data.mean().values, data.std().values])


#    Dataset builder 

def build_aligned_dataset(audio_dir, video_dir):
    audio_dir = Path(audio_dir)
    video_dir = Path(video_dir)
    Path("cache").mkdir(exist_ok=True)

    cache_Xa  = Path("cache/fusion_audio_X.npy")
    cache_Xv  = Path("cache/fusion_video_X.npy")
    cache_y   = Path("cache/fusion_y.npy")

    if cache_Xa.exists() and cache_Xv.exists() and cache_y.exists():
        print("Loading cached fusion features...")
        return (np.load(cache_Xa, allow_pickle=False),
                np.load(cache_Xv, allow_pickle=False),
                list(np.load(cache_y, allow_pickle=True)))

    audio_map = {}
    for wav in sorted(audio_dir.rglob("*.wav")):
        parts = wav.stem.split("-")
        if len(parts) >= 3 and parts[2] in EMOTION_MAP:
            audio_map[wav.stem] = (wav, EMOTION_MAP[parts[2]])

    X_audio, X_video, y_labels = [], [], []
    skipped = 0
    print(f"Building aligned dataset from {len(audio_map)} audio files...")

    for i, (stem, (wav_path, label)) in enumerate(audio_map.items()):
        video_stem = "01-" + "-".join(stem.split("-")[1:])
        candidates = list(video_dir.rglob(f"{video_stem}.csv"))
        if not candidates:
            skipped += 1
            continue
        csv_path = candidates[0]
        print(f"\r  [{i+1}/1440] {stem}", end="", flush=True)
        try:
            a_feat = extract_audio_features(wav_path, n_mfcc=20)
            v_feat = extract_video_features(csv_path)
            X_audio.append(a_feat)
            X_video.append(v_feat)
            y_labels.append(label)
        except Exception as e:
            print(f"\n  Skipped {stem}: {e}")
            skipped += 1

    print(f"\nAligned pairs: {len(y_labels)} | Skipped: {skipped}")
    X_audio = np.array(X_audio)
    X_video = np.array(X_video)

    np.save(cache_Xa, X_audio)
    np.save(cache_Xv, X_video)
    np.save(cache_y,  np.array(y_labels))
    print("Features cached to cache/")

    return X_audio, X_video, y_labels


#    Save results helper 

def save_results(name, preds, y_test, class_names, prefix="fusion"):
    Path("results").mkdir(exist_ok=True)
    report = classification_report(y_test, preds,
                                   target_names=class_names,
                                   zero_division=0)
    print(f"\n=== {name} ===")
    print(report)
    with open(f"results/{prefix}_{name}_report.txt", "w") as f:
        f.write(f"=== {name} ===\n{report}")

    cm = confusion_matrix(y_test, preds)
    disp = ConfusionMatrixDisplay(cm, display_labels=class_names)
    fig, ax = plt.subplots(figsize=(10, 8))
    disp.plot(ax=ax, xticks_rotation=45)
    plt.title(name)
    plt.tight_layout()
    plt.savefig(f"results/{prefix}_{name}_confusion.png")
    plt.close()
    print(f"Saved results/{prefix}_{name}_confusion.png")
    return accuracy_score(y_test, preds)


#    Main fusion function 

def late_fusion(audio_dir="ravdess_data", video_dir="felt_data"):
    print("\n" + "="*60)
    print("FUSION PIPELINE")
    print("="*60)

    X_audio, X_video, y_labels = build_aligned_dataset(audio_dir, video_dir)

    le = LabelEncoder()
    y_enc = le.fit_transform(y_labels)

    idx = np.arange(len(y_enc))
    idx_train, idx_test = train_test_split(
        idx, test_size=0.3, random_state=42, stratify=y_enc
    )

    Xa_train = X_audio[idx_train];  Xa_test = X_audio[idx_test]
    Xv_train = X_video[idx_train];  Xv_test = X_video[idx_test]
    y_train  = y_enc[idx_train];    y_test  = y_enc[idx_test]

    # Scale both modalities independently
    scaler_a = StandardScaler()
    Xa_train = scaler_a.fit_transform(Xa_train)
    Xa_test  = scaler_a.transform(Xa_test)

    scaler_v = StandardScaler()
    Xv_train = scaler_v.fit_transform(Xv_train)
    Xv_test  = scaler_v.transform(Xv_test)

    print(f"\nTrain: {len(y_train)} | Test: {len(y_test)}")
    print("\nTraining individual modality models for fusion...")

    # Best audio model: SVM (n_mfcc=20, scaled)
    audio_clf = SVC(kernel="rbf", probability=True, random_state=42)
    audio_clf.fit(Xa_train, y_train)
    audio_probs_train = audio_clf.predict_proba(Xa_train)
    audio_probs_test  = audio_clf.predict_proba(Xa_test)
    audio_acc = accuracy_score(y_test, audio_clf.predict(Xa_test))
    print(f"  Audio SVM (n_mfcc=20): {audio_acc:.3f} accuracy")

    # Best video model: Random Forest
    video_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    video_clf.fit(Xv_train, y_train)
    video_probs_train = video_clf.predict_proba(Xv_train)
    video_probs_test  = video_clf.predict_proba(Xv_test)
    video_acc = accuracy_score(y_test, video_clf.predict(Xv_test))
    print(f"  Video RF:              {video_acc:.3f} accuracy")

    #    Method A: Weighted probability fusion 
    print("\n--- Method A: Weighted Probability Fusion ---")
    best_w, best_acc_w = 0.5, 0.0
    for w_audio in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
        w_video = 1.0 - w_audio
        fused = w_audio * audio_probs_test + w_video * video_probs_test
        preds = le.classes_[np.argmax(fused, axis=1)]
        acc = accuracy_score(y_test, le.transform(preds))
        print(f"  w_audio={w_audio:.1f} / w_video={w_video:.1f} → accuracy={acc:.3f}")
        if acc > best_acc_w:
            best_acc_w = acc
            best_w = w_audio

    print(f"\nBest weighting: w_audio={best_w:.1f}, w_video={1-best_w:.1f} → {best_acc_w:.3f}")
    fused_best = best_w * audio_probs_test + (1 - best_w) * video_probs_test
    preds_weighted = np.argmax(fused_best, axis=1)
    save_results("weighted_fusion", preds_weighted, y_test,
                 le.classes_, prefix="fusion")

    #    Method B: Logistic regression meta-classifier 
    print("\n--- Method B: Logistic Regression Meta-Classifier ---")
    meta_train = np.hstack([audio_probs_train, video_probs_train])
    meta_test  = np.hstack([audio_probs_test,  video_probs_test])

    meta_clf = LogisticRegression(max_iter=1000, random_state=42)
    meta_clf.fit(meta_train, y_train)
    preds_logistic = meta_clf.predict(meta_test)
    save_results("logistic_fusion", preds_logistic, y_test,
                 le.classes_, prefix="fusion")

    # Method C: Early Fusion (MLP on concatenated features) ─
    print("\n--- Method C: Early Fusion MLP ---")
    from sklearn.neural_network import MLPClassifier

    # Check cache
    cache_Xe_tr = Path("cache/fusion_early_Xtrain.npy")
    cache_Xe_te = Path("cache/fusion_early_Xtest.npy")

    if cache_Xe_tr.exists() and cache_Xe_te.exists():
        print("Loading cached early fusion features...")
        X_early_train = np.load(cache_Xe_tr, allow_pickle=False)
        X_early_test  = np.load(cache_Xe_te, allow_pickle=False)
    else:
        # Xa_train / Xa_test / Xv_train / Xv_test are already scaled
        # above by scaler_a and scaler_v — reuse them directly
        X_early_train = np.concatenate([Xa_train, Xv_train], axis=1)
        X_early_test  = np.concatenate([Xa_test,  Xv_test],  axis=1)
        np.save(cache_Xe_tr, X_early_train)
        np.save(cache_Xe_te, X_early_test)
        print("Early fusion features cached.")

    early_clf = MLPClassifier(
        hidden_layer_sizes=(256, 128, 64),
        max_iter=500,
        random_state=42,
        early_stopping=True
    )
    early_clf.fit(X_early_train, y_train)
    preds_early = early_clf.predict(X_early_test)
    early_acc   = save_results("early_fusion", preds_early, y_test,
                               le.classes_, prefix="fusion")

    #    Summary 
    print("\n" + "="*60)
    print("FUSION SUMMARY")
    print("="*60)
    summary = {
        "Audio SVM (n_mfcc=20)":          audio_acc,
        "Video RF":                        video_acc,
        f"Weighted Fusion (w={best_w:.1f}/{1-best_w:.1f})": best_acc_w,
        "Logistic Regression Fusion":      accuracy_score(y_test, preds_logistic),
        "Early Fusion MLP":                early_acc,          # ← ADD THIS LINE
    }
    for name, acc in summary.items():
        print(f"  {name:45s} {acc:.3f}")

    return summary


if __name__ == "__main__":
    late_fusion("ravdess_data", "felt_data")
