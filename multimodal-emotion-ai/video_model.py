import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay


EMOTION_MAP = {
    "01": "neutral", "02": "calm",    "03": "happy",    "04": "sad",
    "05": "angry",   "06": "fearful", "07": "disgusted", "08": "surprised"
}

LANDMARK_COLS = [f"x_{i}" for i in range(68)] + [f"y_{i}" for i in range(68)]
HEADPOSE_COLS  = ["Pitch", "Roll", "Yaw"]
AU_COLS        = ["AU01","AU02","AU04","AU05","AU06","AU07","AU09","AU10",
                  "AU11","AU12","AU14","AU15","AU17","AU20","AU23","AU24",
                  "AU25","AU26","AU28","AU43"]
FEATURE_COLS   = LANDMARK_COLS + HEADPOSE_COLS + AU_COLS


def parse_felt_files(data_dir):
    data_dir = Path(data_dir)
    filepaths, labels = [], []
    for csv in sorted(data_dir.rglob("*.csv")):
        parts = csv.stem.split("-")
        if len(parts) >= 3:
            vocal_channel  = parts[1]   # "01" = speech, "02" = song
            emotion_code   = parts[2]
            if vocal_channel == "01" and emotion_code in EMOTION_MAP:
                filepaths.append(csv)
                labels.append(EMOTION_MAP[emotion_code])
    return filepaths, labels


def extract_video_features(filepath):
    df = pd.read_csv(filepath)
    available = [c for c in FEATURE_COLS if c in df.columns]
    if not available:
        raise ValueError("No expected feature columns found")
    data = df[available].apply(pd.to_numeric, errors="coerce").dropna()
    if len(data) == 0:
        raise ValueError("No valid frames after dropping NaN rows")
    means = data.mean().values
    stds  = data.std().values
    return np.concatenate([means, stds])


def train_video_model(data_dir):
    print("=== VIDEO MODEL ===")
    print("Parsing FELT CSV files...")
    filepaths, labels = parse_felt_files(data_dir)
    print(f"Found {len(filepaths)} files across {len(set(labels))} emotions")

    print("Extracting features (this may take a few minutes)...")
    X, y = [], []
    for fp, label in zip(filepaths, labels):
        try:
            features = extract_video_features(fp)
            X.append(features)
            y.append(label)
        except Exception as e:
            print(f"  Skipped {fp.name}: {e}")

    X = np.array(X)
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.3, random_state=42, stratify=y_enc
    )
    print(f"Train: {len(X_train)} | Test: {len(X_test)}")

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)

    Path("results").mkdir(exist_ok=True)
    results = {}

    for name, clf in [
        ("Random_Forest", RandomForestClassifier(n_estimators=100, random_state=42)),
        ("SVM",           SVC(kernel="rbf", probability=True, random_state=42))
    ]:
        print(f"\nTraining {name}...")
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)

        report = classification_report(y_test, preds,
                                       target_names=le.classes_,
                                       zero_division=0)
        print(report)

        with open(f"results/video_{name}_report.txt", "w") as f:
            f.write(f"=== VIDEO {name} ===\n{report}")
        print(f"Saved results/video_{name}_report.txt")

        cm = confusion_matrix(y_test, preds)
        disp = ConfusionMatrixDisplay(cm, display_labels=le.classes_)
        fig, ax = plt.subplots(figsize=(10, 8))
        disp.plot(ax=ax, xticks_rotation=45)
        plt.title(f"Video — {name}")
        plt.tight_layout()
        plt.savefig(f"results/video_{name}_confusion.png")
        plt.close()
        print(f"Saved results/video_{name}_confusion.png")

        results[name] = {
            "model":         clf,
            "scaler":        scaler,
            "label_encoder": le,
            "X_test":        X_test,
            "y_test":        y_test
        }

    return results


if __name__ == "__main__":
    train_video_model("felt_data")
