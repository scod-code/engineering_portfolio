import numpy as np
import librosa
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

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

def parse_files(data_dir):
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

def extract_features(filepath, n_mfcc=13):
    y, sr = librosa.load(filepath, sr=None)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    mfcc_mean = mfcc.mean(axis=1)
    mfcc_std  = mfcc.std(axis=1)

    f0, _, _ = librosa.pyin(y, fmin=50, fmax=500)
    f0 = f0[~np.isnan(f0)]
    f0_mean = f0.mean() if len(f0) > 0 else 0.0
    f0_std  = f0.std()  if len(f0) > 0 else 0.0

    rms = librosa.feature.rms(y=y)[0]
    rms_mean, rms_std = rms.mean(), rms.std()

    zcr = librosa.feature.zero_crossing_rate(y)[0]
    zcr_mean, zcr_std = zcr.mean(), zcr.std()

    return np.concatenate([
        mfcc_mean, mfcc_std,
        [f0_mean, f0_std],
        [rms_mean, rms_std],
        [zcr_mean, zcr_std]
    ])

def run_experiment(filepaths, labels, n_mfcc):
    print(f"\n{'='*50}")
    print(f"EXPERIMENT: n_mfcc = {n_mfcc}")
    print(f"{'='*50}")

    Path("cache").mkdir(exist_ok=True)
    cache_X = Path(f"cache/audio_mfcc{n_mfcc}_X.npy")
    cache_y = Path(f"cache/audio_mfcc{n_mfcc}_y.npy")

    if cache_X.exists() and cache_y.exists():
        print(f"Loading cached features for n_mfcc={n_mfcc}...")
        X = np.load(cache_X, allow_pickle=False)
        y = list(np.load(cache_y, allow_pickle=True))
    else:
        print(f"Extracting features for {len(filepaths)} files...")
        X, y = [], []
        for fp, label in zip(filepaths, labels):
            try:
                features = extract_features(fp, n_mfcc=n_mfcc)
                X.append(features)
                y.append(label)
            except Exception as e:
                print(f"  Skipped {fp.name}: {e}")
        X = np.array(X)
        np.save(cache_X, X)
        np.save(cache_y, np.array(y))
        print(f"Cached to {cache_X} and {cache_y}")
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.3, random_state=42, stratify=y_enc
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)
    print(f"Train: {len(X_train)} | Test: {len(X_test)}")

    Path("results").mkdir(exist_ok=True)
    results = {}

    for name, clf in [
        ("Random_Forest", RandomForestClassifier(n_estimators=100, random_state=42)),
        ("SVM",           SVC(kernel="rbf", probability=True, random_state=42))
    ]:
        print(f"\nTraining {name}...")
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)

        report = classification_report(y_test, preds, target_names=le.classes_, zero_division=0)
        print(report)

        report_path = f"results/audio_{name}_mfcc{n_mfcc}_report.txt"
        with open(report_path, "w") as f:
            f.write(f"=== {name} | n_mfcc={n_mfcc} ===\n{report}")
        print(f"Saved {report_path}")

        cm = confusion_matrix(y_test, preds)
        disp = ConfusionMatrixDisplay(cm, display_labels=le.classes_)
        fig, ax = plt.subplots(figsize=(10, 8))
        disp.plot(ax=ax, xticks_rotation=45)
        plt.title(f"Audio — {name} | n_mfcc={n_mfcc}")
        plt.tight_layout()
        confusion_path = f"results/audio_{name}_mfcc{n_mfcc}_confusion.png"
        plt.savefig(confusion_path)
        plt.close()
        print(f"Saved {confusion_path}")

        results[name] = {
            "model": clf,
            "label_encoder": le,
            "X_test": X_test,
            "y_test": y_test
        }

    return results

def train_audio_model(data_dir):
    print("Parsing files...")
    filepaths, labels = parse_files(data_dir)
    print(f"Found {len(filepaths)} files across {len(set(labels))} emotions")

    all_results = {}
    for n_mfcc in [13, 20, 40]:
        all_results[n_mfcc] = run_experiment(filepaths, labels, n_mfcc)

    print("\n\nALL EXPERIMENTS COMPLETE. Results saved to results/")
    return all_results[13]

if __name__ == "__main__":
    train_audio_model("ravdess_data")
