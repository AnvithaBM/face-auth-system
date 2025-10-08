"""
Database module for managing user face embeddings.
"""

import sqlite3
import numpy as np
import json
from typing import Optional, List, Tuple


class UserDatabase:
    """SQLite database for storing user face embeddings."""
    
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database and create users table if not exists."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    embedding TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS login_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    similarity REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
                )
            ''')
            conn.commit()
    
    def add_user(self, username: str, embedding: np.ndarray) -> bool:
        """
        Add a new user with their face embedding.
        
        Args:
            username: Unique username
            embedding: Face embedding vector
            
        Returns:
            True if user added successfully, False otherwise
        """
        try:
            # Convert embedding to JSON string for storage
            embedding_json = json.dumps(embedding.tolist())
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (username, embedding) VALUES (?, ?)',
                    (username, embedding_json)
                )
                conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            # Username already exists
            return False
        except Exception as e:
            print(f"Error adding user: {str(e)}")
            return False
    
    def get_user_embedding(self, username: str) -> Optional[np.ndarray]:
        """
        Get embedding for a specific user.
        
        Args:
            username: Username to retrieve
            
        Returns:
            Embedding vector or None if user not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT embedding FROM users WHERE username = ?',
                    (username,)
                )
                result = cursor.fetchone()
                
                if result:
                    embedding = np.array(json.loads(result[0]))
                    return embedding
                return None
                
        except Exception as e:
            print(f"Error retrieving user: {str(e)}")
            return None
    
    def get_all_users(self) -> List[Tuple[str, np.ndarray]]:
        """
        Get all users and their embeddings.
        
        Returns:
            List of tuples (username, embedding)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT username, embedding FROM users')
                results = cursor.fetchall()
                
                users = []
                for username, embedding_json in results:
                    embedding = np.array(json.loads(embedding_json))
                    users.append((username, embedding))
                return users
                
        except Exception as e:
            print(f"Error retrieving all users: {str(e)}")
            return []
    
    def user_exists(self, username: str) -> bool:
        """Check if a user exists in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT COUNT(*) FROM users WHERE username = ?',
                    (username,)
                )
                count = cursor.fetchone()[0]
                return count > 0
                
        except Exception as e:
            print(f"Error checking user existence: {str(e)}")
            return False
    
    def delete_user(self, username: str) -> bool:
        """Delete a user from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM users WHERE username = ?', (username,))
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return False
    
    def get_user_count(self) -> int:
        """Get total number of registered users."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM users')
                count = cursor.fetchone()[0]
                return count
                
        except Exception as e:
            print(f"Error getting user count: {str(e)}")
            return 0
    
    def update_user_embedding(self, username: str, embedding: np.ndarray) -> bool:
        """
        Update the face embedding for an existing user.
        
        Args:
            username: Username to update
            embedding: New face embedding vector
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            embedding_json = json.dumps(embedding.tolist())
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE users SET embedding = ? WHERE username = ?',
                    (embedding_json, username)
                )
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Error updating user embedding: {str(e)}")
            return False
    
    def get_user_info(self, username: str) -> Optional[dict]:
        """
        Get user information including registration date.
        
        Args:
            username: Username to retrieve
            
        Returns:
            Dictionary with user info or None if user not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT id, username, created_at FROM users WHERE username = ?',
                    (username,)
                )
                result = cursor.fetchone()
                
                if result:
                    return {
                        'id': result[0],
                        'username': result[1],
                        'created_at': result[2]
                    }
                return None
                
        except Exception as e:
            print(f"Error retrieving user info: {str(e)}")
            return None
    
    def add_login_attempt(self, username: str, success: bool, similarity: float = None) -> bool:
        """
        Record a login attempt in the history.
        
        Args:
            username: Username attempting to login
            success: Whether the login was successful
            similarity: Similarity score (optional)
            
        Returns:
            True if recorded successfully, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO login_history (username, success, similarity) VALUES (?, ?, ?)',
                    (username, 1 if success else 0, similarity)
                )
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error adding login attempt: {str(e)}")
            return False
    
    def get_login_history(self, username: str, limit: int = 50) -> List[dict]:
        """
        Get login history for a specific user.
        
        Args:
            username: Username to get history for
            limit: Maximum number of records to return
            
        Returns:
            List of login attempt dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''SELECT success, similarity, timestamp 
                       FROM login_history 
                       WHERE username = ? 
                       ORDER BY timestamp DESC 
                       LIMIT ?''',
                    (username, limit)
                )
                results = cursor.fetchall()
                
                history = []
                for success, similarity, timestamp in results:
                    history.append({
                        'success': bool(success),
                        'similarity': similarity,
                        'timestamp': timestamp
                    })
                return history
                
        except Exception as e:
            print(f"Error retrieving login history: {str(e)}")
            return []
