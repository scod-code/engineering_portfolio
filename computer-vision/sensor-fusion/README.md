# Sensor Fusion: GPS + IMU + Kalman Filter

**NTU MSc AI | Computer Vision Lab 8**

Implementation of a GPS/IMU sensor fusion pipeline using Extended Kalman Filtering (EKF) for state estimation and position tracking.

## Overview

This lab implements sensor fusion between GPS (position measurements) and IMU (acceleration/gyroscope data) to produce accurate state estimates using the Kalman Filter algorithm. The approach models the complementary strengths of both sensors: GPS provides absolute position but with noise; IMU provides high-frequency motion but drifts over time.

## Key Concepts

- **Kalman Filtering**: Linear and Extended Kalman Filter (EKF) for recursive state estimation
- **GPS + IMU Fusion**: Complementary sensor modalities for robust localisation
- **State Estimation**: Position, velocity, and orientation tracking
- **Noise Modelling**: Process noise (Q) and measurement noise (R) covariance tuning

## Tech Stack

| Component | Tool |
|---|---|
| Language | Python 3.10+ |
| Filtering | FilterPy, NumPy |
| Data Handling | Pandas |
| Visualisation | Matplotlib |

## Files

- `Lab_8.ipynb` - Jupyter notebook implementing GPS+IMU sensor fusion with Kalman filtering

## Skills Demonstrated

- Sensor fusion algorithm implementation
- Kalman filter design and parameter tuning
- State-space modelling
- Signal processing and noise handling
- Python scientific computing (NumPy, FilterPy)
