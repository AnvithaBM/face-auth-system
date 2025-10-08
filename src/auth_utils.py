"""
Authentication utilities for face comparison.
"""

import numpy as np
from typing import Optional, Tuple


def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two embeddings.
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
        
    Returns:
        Cosine similarity score (0 to 1)
    """
    # Normalize embeddings
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    embedding1_normalized = embedding1 / norm1
    embedding2_normalized = embedding2 / norm2
    
    # Calculate cosine similarity
    similarity = np.dot(embedding1_normalized, embedding2_normalized)
    return float(similarity)


def authenticate_user(query_embedding: np.ndarray, 
                     stored_embedding: np.ndarray,
                     threshold: float = 0.6) -> Tuple[bool, float]:
    """
    Authenticate user by comparing embeddings.
    
    Args:
        query_embedding: Embedding from live capture
        stored_embedding: Stored embedding from database
        threshold: Similarity threshold for authentication (default: 0.6)
        
    Returns:
        Tuple of (is_authenticated, similarity_score)
    """
    similarity = cosine_similarity(query_embedding, stored_embedding)
    is_authenticated = similarity >= threshold
    return is_authenticated, similarity


def find_best_match(query_embedding: np.ndarray,
                    user_embeddings: list,
                    threshold: float = 0.6) -> Optional[Tuple[str, float]]:
    """
    Find the best matching user from a list of user embeddings.
    
    Args:
        query_embedding: Embedding from live capture
        user_embeddings: List of tuples (username, embedding)
        threshold: Minimum similarity threshold
        
    Returns:
        Tuple of (username, similarity) for best match, or None if no match
    """
    if not user_embeddings:
        return None
    
    best_match = None
    best_similarity = 0.0
    
    for username, stored_embedding in user_embeddings:
        similarity = cosine_similarity(query_embedding, stored_embedding)
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = username
    
    if best_similarity >= threshold:
        return (best_match, best_similarity)
    
    return None
