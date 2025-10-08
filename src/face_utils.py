"""
Face utilities module for face detection and embedding extraction.
"""

import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D


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
    """Extract face embeddings using pre-trained CNN."""
    
    def __init__(self, input_shape=(224, 224, 3)):
        self.input_shape = input_shape
        self.model = self._build_model()
    
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
    
    def extract_embedding(self, face_image):
        """
        Extract embedding from face image.
        
        Args:
            face_image: Face region (BGR or RGB format)
            
        Returns:
            Embedding vector as numpy array
        """
        try:
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
            
        except Exception as e:
            raise Exception(f"Error extracting embedding: {str(e)}")
    
    def normalize_embedding(self, embedding):
        """Normalize embedding vector (L2 normalization)."""
        norm = np.linalg.norm(embedding)
        if norm == 0:
            return embedding
        return embedding / norm
