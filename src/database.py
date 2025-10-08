"""
Database module for managing user face embeddings.
"""

import sqlite3
import numpy as np
import json
from typing import Optional, List, Tuple
from datetime import datetime
import pytz


class UserDatabase:
    """SQLite database for storing user face embeddings."""
    
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.ist_tz = pytz.timezone('Asia/Kolkata')
        self._init_database()
    
    def _convert_utc_to_ist(self, utc_time_str: str) -> str:
        """
        Convert UTC timestamp string to IST.
        
        Args:
            utc_time_str: UTC timestamp string from database
            
        Returns:
            IST formatted timestamp string
        """
        try:
            # Parse the UTC timestamp
            utc_time = datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S')
            utc_time = pytz.utc.localize(utc_time)
            
            # Convert to IST
            ist_time = utc_time.astimezone(self.ist_tz)
            
            # Format as readable string
            return ist_time.strftime('%Y-%m-%d %H:%M:%S IST')
        except Exception as e:
            print(f"Error converting time to IST: {str(e)}")
            return utc_time_str
    
    def _init_database(self):
        """Initialize database and create users and login_history tables if not exists."""
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
                    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success INTEGER NOT NULL,
                    similarity REAL,
                    FOREIGN KEY (username) REFERENCES users(username)
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
    
    def log_authentication(self, username: str, success: bool, similarity: float = None) -> bool:
        """
        Log an authentication attempt.
        
        Args:
            username: Username that was authenticated
            success: Whether authentication was successful
            similarity: Similarity score (optional)
            
        Returns:
            True if logged successfully, False otherwise
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
            print(f"Error logging authentication: {str(e)}")
            return False
    
    def get_login_history(self, username: str = None, limit: int = 50) -> List[dict]:
        """
        Get login history, optionally filtered by username.
        
        Args:
            username: Optional username to filter by
            limit: Maximum number of records to return
            
        Returns:
            List of dictionaries containing login history
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if username:
                    cursor.execute(
                        'SELECT username, login_time, success, similarity FROM login_history WHERE username = ? ORDER BY login_time DESC LIMIT ?',
                        (username, limit)
                    )
                else:
                    cursor.execute(
                        'SELECT username, login_time, success, similarity FROM login_history ORDER BY login_time DESC LIMIT ?',
                        (limit,)
                    )
                
                results = cursor.fetchall()
                
                history = []
                for username, login_time, success, similarity in results:
                    history.append({
                        'username': username,
                        'login_time': self._convert_utc_to_ist(login_time),
                        'success': bool(success),
                        'similarity': similarity
                    })
                return history
                
        except Exception as e:
            print(f"Error retrieving login history: {str(e)}")
            return []
    
    def get_user_info(self, username: str) -> Optional[dict]:
        """
        Get user information including registration time.
        
        Args:
            username: Username to retrieve
            
        Returns:
            Dictionary with user info or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT username, created_at FROM users WHERE username = ?',
                    (username,)
                )
                result = cursor.fetchone()
                
                if result:
                    username, created_at = result
                    return {
                        'username': username,
                        'created_at': self._convert_utc_to_ist(created_at)
                    }
                return None
                
        except Exception as e:
            print(f"Error retrieving user info: {str(e)}")
            return None
    
    def get_all_users_with_info(self) -> List[dict]:
        """
        Get all users with their registration timestamps.
        
        Returns:
            List of dictionaries with user info
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT username, created_at FROM users ORDER BY created_at DESC')
                results = cursor.fetchall()
                
                users = []
                for username, created_at in results:
                    users.append({
                        'username': username,
                        'created_at': self._convert_utc_to_ist(created_at)
                    })
                return users
                
        except Exception as e:
            print(f"Error retrieving all users with info: {str(e)}")
            return []
