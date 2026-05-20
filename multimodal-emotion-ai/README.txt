COMP40781 Coursework — Artificial Perception based Multi-modal Tutoring Software

Student: Somtochukwu C. Osigwe-Daniel   Module: COMP40781

Dataset: RAVDESS — The Ryerson Audio-Visual Database of
         Emotional Speech and Song
Source:  https://zenodo.org/records/1188976
Licence: Creative Commons CC BY-NC-SA 4.0

FELT Companion Dataset (facial features):
Source: https://zenodo.org/records/13243600

SETUP & RUN — TWO COMMANDS ONLY

1.  pip install -r requirements.txt

2.  python main.py

    ↳ On first run: dataset downloads automatically (~12 GB).
      Subsequent runs use the cached local copy — no re-download.
    ↳ All results (metrics, plots, confusion matrices) are saved
      to the /results/ folder.

Python 3.10+ required.

