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
