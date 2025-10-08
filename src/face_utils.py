"""
Face utilities module for face detection and embedding extraction.
"""

import cv2
import numpy as np

# Try to import TensorFlow, but fall back to simple implementation if not available
try:
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import GlobalAveragePooling2D
    TENSORFLOW_AVAILABLE = True
except Exception as e:
    print(f"TensorFlow import failed: {e}. Using simple feature extraction.")
    TENSORFLOW_AVAILABLE = False


class FaceDetector:
    """Face detector using OpenCV's Haar Cascade."""
    
    def __init__(self):
        # Load pre-trained Haar Cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def detect_face(self, image):
        """
        Detect face in the image.
        
        Args:
            image: Input image (BGR format from OpenCV or RGB from webcam)
            
        Returns:
            Face region as numpy array or None if no face detected
        """
        # Convert to grayscale for detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )
        
        if len(faces) == 0:
            return None
        
        # Return the largest face detected
        largest_face = max(faces, key=lambda face: face[2] * face[3])
        x, y, w, h = largest_face
        
        # Extract face region with some padding
        padding = 20
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image.shape[1], x + w + padding)
        y2 = min(image.shape[0], y + h + padding)
        
        face_region = image[y1:y2, x1:x2]
        return face_region


class EmbeddingExtractor:
    """Extract face embeddings using pre-trained CNN or simple features."""
    
    def __init__(self, input_shape=(224, 224, 3)):
        self.input_shape = input_shape
        if TENSORFLOW_AVAILABLE:
            try:
                self.model = self._build_model()
                self.use_tensorflow = True
            except Exception as e:
                print(f"Failed to build TensorFlow model: {e}. Using simple features.")
                self.use_tensorflow = False
        else:
            self.use_tensorflow = False
    
    def _build_model(self):
        """Build embedding extraction model based on MobileNetV2."""
        # Load pre-trained MobileNetV2
        base_model = MobileNetV2(
            input_shape=self.input_shape,
            include_top=False,
            weights='imagenet'
        )
        
        # Add global average pooling to get embeddings
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        
        # Create model
        model = Model(inputs=base_model.input, outputs=x)
        return model
    
    def _extract_simple_features(self, face_image):
        """
        Extract simple HOG-like features from face image as a fallback.
        This creates a feature vector that can still be used for face matching.
        """
        # Resize to standard size
        face_resized = cv2.resize(face_image, (128, 128))
        
        # Convert to grayscale
        if len(face_resized.shape) == 3:
            gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
        else:
            gray = face_resized
        
        # Divide image into grid
        grid_size = 8
        cell_h = gray.shape[0] // grid_size
        cell_w = gray.shape[1] // grid_size
        
        features = []
        
        # Extract features from each cell
        for i in range(grid_size):
            for j in range(grid_size):
                cell = gray[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
                
                # Calculate gradient features
                gx = cv2.Sobel(cell, cv2.CV_64F, 1, 0, ksize=3)
                gy = cv2.Sobel(cell, cv2.CV_64F, 0, 1, ksize=3)
                
                # Histogram of gradients
                magnitude = np.sqrt(gx**2 + gy**2)
                
                # Simple statistics
                features.extend([
                    np.mean(cell),
                    np.std(cell),
                    np.mean(magnitude),
                    np.max(magnitude)
                ])
        
        return np.array(features, dtype=np.float32)
    
    def extract_embedding(self, face_image):
        """
        Extract embedding from face image.
        
        Args:
            face_image: Face region (BGR or RGB format)
            
        Returns:
            Embedding vector as numpy array
        """
        try:
            if self.use_tensorflow:
                # Resize to model input size
                face_resized = cv2.resize(face_image, self.input_shape[:2])
                
                # Convert BGR to RGB if needed
                if len(face_resized.shape) == 2:
                    face_resized = cv2.cvtColor(face_resized, cv2.COLOR_GRAY2RGB)
                elif face_resized.shape[2] == 3:
                    # Assume BGR from OpenCV, convert to RGB
                    face_resized = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
                
                # Preprocess for MobileNetV2
                face_array = np.expand_dims(face_resized, axis=0)
                face_array = preprocess_input(face_array)
                
                # Extract embedding
                embedding = self.model.predict(face_array, verbose=0)
                return embedding[0]
            else:
                # Use simple feature extraction
                return self._extract_simple_features(face_image)
            
        except Exception as e:
            raise Exception(f"Error extracting embedding: {str(e)}")
    
    def normalize_embedding(self, embedding):
        """Normalize embedding vector (L2 normalization)."""
        norm = np.linalg.norm(embedding)
        if norm == 0:
            return embedding
        return embedding / norm
