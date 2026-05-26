from download_data import download_ravdess, download_felt
from audio_model import train_audio_model
from video_model import train_video_model
from fusion import late_fusion


def main():
    print("="*60)
    print("COMP40781 — Artificial Perception Coursework")
    print("Multimodal Emotion Recognition Pipeline")
    print("="*60)

    print("\n[1/4] Checking datasets...")
    download_ravdess("ravdess_data")
    download_felt("felt_data")

    print("\n[2/4] Training audio models (MFCC ablation: 13, 20, 40)...")
    train_audio_model("ravdess_data")

    print("\n[3/4] Training video models...")
    train_video_model("felt_data")

    print("\n[4/4] Running fusion pipeline...")
    summary = late_fusion("ravdess_data", "felt_data")

    print("\n" + "="*60)
    print("PIPELINE COMPLETE — all results saved to results/")
    print("="*60)
    for name, acc in summary.items():
        print(f"  {name:45s} {acc:.3f}")


if __name__ == "__main__":
    main()