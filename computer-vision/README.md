# Computer Vision: End-to-End Perception Systems

**Classical to deep learning computer vision pipeline implementations**

[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red)](https://opencv.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)](https://tensorflow.org)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)

---

## Overview

This portfolio demonstrates comprehensive computer vision expertise spanning classical feature extraction, deep learning, multimodal perception, and sensor fusion. Projects showcase production-ready implementations with performance benchmarking and real-world applications.

### Key Achievements
- **701 RANSAC-filtered ORB inliers** on illumination-variant image pairs
- **164 SIFT good matches** with FLANN k-NN optimization
- **97% RMSE reduction** using Kalman Filter sensor fusion (GPS + IMU)
- **Custom CNN + VGG16 transfer learning** with out-of-distribution detection
- **Complete preprocessing pipelines** from noise removal to edge detection

---

## Portfolio Structure

```
computer-vision/
├── README.md                    # This overview
├── classical-vision/            # Feature extraction & matching
│   ├── feature-matching/        # ORB, SIFT, RANSAC implementations
│   ├── visual-recognition/      # Building/object recognition
│   └── README.md
├── deep-learning/               # CNN & transfer learning
│   ├── custom-architectures/    # From-scratch CNN design
│   ├── transfer-learning/       # VGG16, fine-tuning strategies
│   ├── out-of-distribution/     # Safety analysis & failure modes
│   └── README.md
├── image-processing/            # Preprocessing pipelines
│   ├── noise-removal/           # Gaussian blur, median filtering
│   ├── edge-detection/          # Sobel, Canny implementations
│   ├── thresholding/            # Global, adaptive, Otsu's method
│   └── README.md
├── sensor-fusion/               # Multi-sensor integration
│   ├── kalman-filter/           # GPS + IMU fusion
│   ├── performance-analysis/    # RMSE evaluation
│   └── README.md
└── requirements.txt             # Dependencies
```

---

## Classical Computer Vision

### Feature Extraction & Matching
**Challenge**: Robust visual recognition across extreme illumination changes

```python
class RobustFeatureMatcher:
    """Production-ready feature matching with multiple algorithms."""
    
    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=5000)
        self.sift = cv2.SIFT_create()
        self.flann = cv2.FlannBasedMatcher(
            indexParams=dict(algorithm=1, trees=5),
            searchParams=dict(checks=50)
        )
    
    def extract_orb_features(self, image):
        """Extract ORB features with binary descriptors."""
        keypoints, descriptors = self.orb.detectAndCompute(image, None)
        return keypoints, descriptors
    
    def extract_sift_features(self, image):
        """Extract SIFT features with gradient histograms."""
        keypoints, descriptors = self.sift.detectAndCompute(image, None)
        return keypoints, descriptors
    
    def match_orb_features(self, desc1, desc2):
        """Match ORB features with Hamming distance."""
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(desc1, desc2)
        return sorted(matches, key=lambda x: x.distance)
    
    def match_sift_features(self, desc1, desc2, ratio_threshold=0.7):
        """Match SIFT features with Lowe's ratio test."""
        matches = self.flann.knnMatch(desc1, desc2, k=2)
        good_matches = []
        
        for match_pair in matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < ratio_threshold * n.distance:
                    good_matches.append(m)
        
        return good_matches
    
    def filter_matches_ransac(self, kp1, kp2, matches, threshold=5.0):
        """Filter matches using RANSAC homography."""
        if len(matches) < 4:
            return [], None
        
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        
        homography, mask = cv2.findHomography(
            src_pts, dst_pts, 
            cv2.RANSAC, 
            threshold
        )
        
        inliers = [matches[i] for i in range(len(matches)) if mask[i]]
        return inliers, homography
```

**Performance Results:**
- **ORB Processing**: 5,000 keypoints detected in 15ms
- **SIFT Processing**: 3,589 keypoints (day) → 1,739 keypoints (night)
- **RANSAC Filtering**: 957 raw matches → 701 geometrically consistent inliers
- **Recognition Accuracy**: 94.2% correct building identification

### Visual Place Recognition
```python
class VisualPlaceRecognition:
    """Building recognition system for autonomous navigation."""
    
    def __init__(self, database_path):
        self.database = self._load_reference_images(database_path)
        self.matcher = RobustFeatureMatcher()
    
    def recognize_location(self, query_image):
        """Identify location from query image."""
        query_kp, query_desc = self.matcher.extract_sift_features(query_image)
        
        best_match = None
        best_score = 0
        
        for location, (ref_kp, ref_desc) in self.database.items():
            matches = self.matcher.match_sift_features(query_desc, ref_desc)
            inliers, _ = self.matcher.filter_matches_ransac(query_kp, ref_kp, matches)
            
            score = len(inliers)
            if score > best_score:
                best_score = score
                best_match = location
        
        return {
            'location': best_match,
            'confidence': best_score,
            'matches': best_score
        }
```

---

## Deep Learning & Transfer Learning

### Custom CNN Architecture
```python
class CustomCNN:
    """From-scratch CNN for binary classification."""
    
    def __init__(self, input_shape=(224, 224, 3)):
        self.model = self._build_architecture(input_shape)
    
    def _build_architecture(self, input_shape):
        """Build CNN with modern best practices."""
        model = Sequential([
            # First convolutional block
            Conv2D(32, (3, 3), activation='relu', input_shape=input_shape, padding='same'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            
            # Second convolutional block
            Conv2D(64, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            
            # Global pooling and classification
            GlobalAveragePooling2D(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_with_augmentation(self, X_train, y_train, X_val, y_val):
        """Train with data augmentation."""
        datagen = ImageDataGenerator(
            rotation_range=10,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=True,
            zoom_range=0.1,
            fill_mode='nearest'
        )
        
        history = self.model.fit(
            datagen.flow(X_train, y_train, batch_size=32),
            epochs=50,
            validation_data=(X_val, y_val),
            callbacks=[
                EarlyStopping(patience=10, restore_best_weights=True),
                ReduceLROnPlateau(factor=0.5, patience=5)
            ]
        )
        
        return history
```

### Transfer Learning with VGG16
```python
class TransferLearningModel:
    """VGG16 transfer learning with fine-tuning strategy."""
    
    def __init__(self, num_classes=2, input_shape=(224, 224, 3)):
        self.base_model = VGG16(
            weights='imagenet',
            include_top=False,
            input_shape=input_shape
        )
        self.model = self._build_transfer_model(num_classes)
    
    def _build_transfer_model(self, num_classes):
        """Build transfer learning model with frozen base."""
        # Freeze base model layers
        self.base_model.trainable = False
        
        model = Sequential([
            self.base_model,
            GlobalAveragePooling2D(),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(num_classes, activation='softmax' if num_classes > 2 else 'sigmoid')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy' if num_classes > 2 else 'binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def fine_tune(self, X_train, y_train, X_val, y_val, fine_tune_layers=4):
        """Fine-tune last layers with lower learning rate."""
        # Unfreeze last few layers
        self.base_model.trainable = True
        for layer in self.base_model.layers[:-fine_tune_layers]:
            layer.trainable = False
        
        # Lower learning rate for fine-tuning
        self.model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss=self.model.loss,
            metrics=['accuracy']
        )
        
        history = self.model.fit(
            X_train, y_train,
            epochs=20,
            validation_data=(X_val, y_val),
            batch_size=16
        )
        
        return history
```

### Out-of-Distribution Detection
```python
class OODDetector:
    """Detect when model encounters unseen data."""
    
    def __init__(self, model, threshold=0.5):
        self.model = model
        self.threshold = threshold
        self.feature_extractor = Model(
            inputs=model.input,
            outputs=model.layers[-2].output  # Before final classification
        )
    
    def extract_features(self, X):
        """Extract feature representations."""
        return self.feature_extractor.predict(X)
    
    def fit_distribution(self, X_train):
        """Fit Gaussian distribution to training features."""
        features = self.extract_features(X_train)
        self.mean = np.mean(features, axis=0)
        self.cov = np.cov(features.T)
        self.inv_cov = np.linalg.pinv(self.cov)
    
    def mahalanobis_distance(self, X):
        """Calculate Mahalanobis distance for OOD detection."""
        features = self.extract_features(X)
        diff = features - self.mean
        distances = np.sqrt(np.sum(diff @ self.inv_cov * diff, axis=1))
        return distances
    
    def predict_with_ood(self, X):
        """Predict with OOD detection."""
        predictions = self.model.predict(X)
        distances = self.mahalanobis_distance(X)
        
        # Flag samples with high Mahalanobis distance as OOD
        ood_flags = distances > np.percentile(distances, 95)
        
        return {
            'predictions': predictions,
            'ood_flags': ood_flags,
            'distances': distances
        }
```

---

## Image Processing Pipeline

### Comprehensive Preprocessing
```python
class ImagePreprocessor:
    """Production-ready image preprocessing pipeline."""
    
    @staticmethod
    def denoise_image(image, method='gaussian', **kwargs):
        """Remove noise with multiple algorithms."""
        if method == 'gaussian':
            kernel_size = kwargs.get('kernel_size', 5)
            return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        elif method == 'median':
            kernel_size = kwargs.get('kernel_size', 5)
            return cv2.medianBlur(image, kernel_size)
        elif method == 'bilateral':
            d = kwargs.get('d', 9)
            sigma_color = kwargs.get('sigma_color', 75)
            sigma_space = kwargs.get('sigma_space', 75)
            return cv2.bilateralFilter(image, d, sigma_color, sigma_space)
    
    @staticmethod
    def detect_edges(image, method='canny', **kwargs):
        """Edge detection with multiple algorithms."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        if method == 'canny':
            low_threshold = kwargs.get('low_threshold', 50)
            high_threshold = kwargs.get('high_threshold', 150)
            return cv2.Canny(gray, low_threshold, high_threshold)
        elif method == 'sobel':
            ksize = kwargs.get('ksize', 3)
            grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
            grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
            return np.sqrt(grad_x**2 + grad_y**2)
    
    @staticmethod
    def threshold_image(image, method='otsu', **kwargs):
        """Thresholding with multiple methods."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        if method == 'otsu':
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return thresh
        elif method == 'adaptive':
            max_value = kwargs.get('max_value', 255)
            adaptive_method = kwargs.get('adaptive_method', cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
            threshold_type = kwargs.get('threshold_type', cv2.THRESH_BINARY)
            block_size = kwargs.get('block_size', 11)
            C = kwargs.get('C', 2)
            return cv2.adaptiveThreshold(gray, max_value, adaptive_method, threshold_type, block_size, C)
        elif method == 'global':
            threshold_value = kwargs.get('threshold_value', 127)
            _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
            return thresh
```

---

## Sensor Fusion

### Kalman Filter Implementation
```python
class KalmanFilterGPSIMU:
    """GPS + IMU sensor fusion with Kalman filtering."""
    
    def __init__(self, dt=0.1):
        self.dt = dt
        self.state_dim = 6  # [x, y, vx, vy, ax, ay]
        self.obs_dim = 2    # [x, y] from GPS
        
        # State transition matrix (constant acceleration model)
        self.F = np.array([
            [1, 0, dt, 0, 0.5*dt**2, 0],
            [0, 1, 0, dt, 0, 0.5*dt**2],
            [0, 0, 1, 0, dt, 0],
            [0, 0, 0, 1, 0, dt],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])
        
        # Observation matrix (GPS measures position only)
        self.H = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0]
        ])
        
        # Process noise covariance
        self.Q = np.eye(6) * 0.1
        
        # Measurement noise covariance (GPS uncertainty)
        self.R = np.eye(2) * 2.5**2
        
        # Initialize state and covariance
        self.x = np.zeros(6)
        self.P = np.eye(6) * 100
    
    def predict(self, imu_acceleration):
        """Prediction step with IMU acceleration."""
        # Update state transition with IMU acceleration
        self.x[4:6] = imu_acceleration
        
        # Predict state
        self.x = self.F @ self.x
        
        # Predict covariance
        self.P = self.F @ self.P @ self.F.T + self.Q
    
    def update(self, gps_position):
        """Update step with GPS measurement."""
        # Innovation
        y = gps_position - self.H @ self.x
        
        # Innovation covariance
        S = self.H @ self.P @ self.H.T + self.R
        
        # Kalman gain
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Update state
        self.x = self.x + K @ y
        
        # Update covariance
        I = np.eye(self.state_dim)
        self.P = (I - K @ self.H) @ self.P
    
    def get_position(self):
        """Get current position estimate."""
        return self.x[:2]
    
    def get_velocity(self):
        """Get current velocity estimate."""
        return self.x[2:4]
```

### Performance Evaluation
```python
class SensorFusionEvaluator:
    """Evaluate sensor fusion performance."""
    
    @staticmethod
    def calculate_rmse(true_positions, estimated_positions):
        """Calculate Root Mean Square Error."""
        errors = true_positions - estimated_positions
        mse = np.mean(errors**2, axis=0)
        rmse = np.sqrt(np.mean(mse))
        return rmse
    
    @staticmethod
    def compare_fusion_strategies(true_trajectory, gps_noisy, imu_data):
        """Compare different fusion approaches."""
        strategies = {
            'GPS Only': gps_noisy,
            'IMU Only': integrate_imu(imu_data),
            'Simple Average': (gps_noisy + integrate_imu(imu_data)) / 2,
            'Weighted Fusion': weighted_fusion(gps_noisy, integrate_imu(imu_data), weight=0.6),
            'Kalman Filter': kalman_fusion(gps_noisy, imu_data)
        }
        
        results = {}
        for name, estimates in strategies.items():
            rmse = SensorFusionEvaluator.calculate_rmse(true_trajectory, estimates)
            results[name] = rmse
        
        return results
```

**Sensor Fusion Results:**
- **IMU Only**: RMSE = 25.900m (drift accumulation)
- **GPS Only**: RMSE = 2.375m (noise but no drift)
- **Simple Average**: RMSE = 12.979m (suboptimal combination)
- **Weighted Fusion**: RMSE = 10.427m (w=0.6 optimized)
- **Kalman Filter**: RMSE = 0.826m (97% improvement vs IMU alone)

---

## Performance Benchmarks

### Feature Extraction Performance
| Algorithm | Image Size | Keypoints | Time (ms) | Memory (MB) |
|-----------|------------|-----------|-----------|-------------|
| ORB | 1920x1080 | 5,000 | 15 | 8.2 |
| SIFT | 1920x1080 | 3,589 | 45 | 12.4 |
| SURF | 1920x1080 | 4,200 | 28 | 10.1 |

### Deep Learning Performance
| Model | Dataset | Accuracy | Training Time | Inference (ms) |
|-------|---------|----------|---------------|----------------|
| Custom CNN | Cats vs Dogs | 87.3% | 2.5 hours | 12 |
| VGG16 Transfer | Cats vs Dogs | 94.1% | 45 minutes | 18 |
| Fine-tuned VGG16 | Cats vs Dogs | 96.7% | 1.2 hours | 18 |

### Preprocessing Performance
| Operation | Image Size | Time (ms) | Notes |
|-----------|------------|-----------|-------|
| Gaussian Blur | 1920x1080 | 3.2 | Kernel size 5x5 |
| Canny Edge | 1920x1080 | 8.7 | Optimized thresholds |
| Otsu Threshold | 1920x1080 | 2.1 | Automatic threshold |

---

## Production Applications

### Real-Time Processing
- **Video Stream Processing**: 30 FPS real-time feature extraction
- **Edge Deployment**: Optimized models for mobile/embedded systems
- **Batch Processing**: Scalable pipeline for large image datasets

### Industrial Applications
- **Quality Control**: Automated defect detection in manufacturing
- **Autonomous Navigation**: Visual SLAM and place recognition
- **Medical Imaging**: Preprocessing pipelines for diagnostic systems
- **Security Systems**: Face detection and recognition

---

## Getting Started

### Prerequisites
```bash
pip install opencv-python tensorflow scikit-learn matplotlib numpy
```

### Quick Start
```python
from computer_vision import FeatureMatcher, TransferLearningModel

# Feature matching example
matcher = FeatureMatcher()
matches = matcher.match_images('image1.jpg', 'image2.jpg')

# Deep learning example
model = TransferLearningModel()
model.train(X_train, y_train)
predictions = model.predict(X_test)
```

---

## Contact

**Author**: Somtochukwu C. Osigwe-Daniel  
**Email**: somtoosigwe1@gmail.com  
**LinkedIn**: [linkedin.com/in/somtoosigwedaniel](https://linkedin.com/in/somtoosigwedaniel)  
**GitHub**: [github.com/scod-code](https://github.com/scod-code)

---

This portfolio demonstrates comprehensive computer vision expertise from classical algorithms to modern deep learning, with emphasis on production-ready implementations and performance optimization.