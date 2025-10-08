"""
Flask web application for face authentication system.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import cv2
import numpy as np
import base64
import secrets
from src.face_utils import FaceDetector, EmbeddingExtractor
from src.database import UserDatabase
from src.auth_utils import authenticate_user, find_best_match

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate a secure secret key

# Initialize components
face_detector = FaceDetector()
embedding_extractor = EmbeddingExtractor()
user_db = UserDatabase('users.db')


def decode_image(image_data):
    """Decode base64 image data to OpenCV image."""
    try:
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        return image
    except Exception as e:
        raise Exception(f"Error decoding image: {str(e)}")


@app.route('/')
def index():
    """Home page - redirect to registration."""
    return render_template('index.html')


@app.route('/register')
def register_page():
    """Registration page."""
    return render_template('register.html')


@app.route('/authenticate')
def authenticate_page():
    """Authentication page."""
    return render_template('authenticate.html')


@app.route('/api/register', methods=['POST'])
def register_user():
    """Register a new user with their face embedding."""
    try:
        data = request.json
        username = data.get('username')
        image_data = data.get('image')
        
        if not username or not image_data:
            return jsonify({
                'success': False,
                'message': 'Username and image are required'
            }), 400
        
        # Check if user already exists
        if user_db.user_exists(username):
            return jsonify({
                'success': False,
                'message': f'User "{username}" already exists'
            }), 400
        
        # Decode image
        image = decode_image(image_data)
        
        if image is None:
            return jsonify({
                'success': False,
                'message': 'Failed to decode image'
            }), 400
        
        # Detect face
        face = face_detector.detect_face(image)
        
        if face is None:
            return jsonify({
                'success': False,
                'message': 'No face detected in the image'
            }), 400
        
        # Extract embedding
        embedding = embedding_extractor.extract_embedding(face)
        normalized_embedding = embedding_extractor.normalize_embedding(embedding)
        
        # Store in database
        success = user_db.add_user(username, normalized_embedding)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'User "{username}" registered successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to register user'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """Authenticate a user by comparing face embedding."""
    try:
        data = request.json
        image_data = data.get('image')
        username = data.get('username', None)
        
        if not image_data:
            return jsonify({
                'success': False,
                'message': 'Image is required'
            }), 400
        
        # Decode image
        image = decode_image(image_data)
        
        if image is None:
            return jsonify({
                'success': False,
                'message': 'Failed to decode image'
            }), 400
        
        # Detect face
        face = face_detector.detect_face(image)
        
        if face is None:
            return jsonify({
                'success': False,
                'message': 'No face detected in the image'
            }), 400
        
        # Extract embedding
        embedding = embedding_extractor.extract_embedding(face)
        normalized_embedding = embedding_extractor.normalize_embedding(embedding)
        
        # Authenticate
        if username:
            # Authenticate specific user
            stored_embedding = user_db.get_user_embedding(username)
            
            if stored_embedding is None:
                return jsonify({
                    'success': False,
                    'message': f'User "{username}" not found'
                }), 404
            
            is_authenticated, similarity = authenticate_user(
                normalized_embedding, 
                stored_embedding,
                threshold=0.6
            )
            
            # Record login attempt
            user_db.add_login_attempt(username, is_authenticated, float(similarity))
            
            if is_authenticated:
                # Set session
                session['username'] = username
                session['authenticated'] = True
                
                return jsonify({
                    'success': True,
                    'authenticated': True,
                    'username': username,
                    'similarity': float(similarity),
                    'message': f'Authentication successful! Welcome {username}'
                })
            else:
                return jsonify({
                    'success': True,
                    'authenticated': False,
                    'username': username,
                    'similarity': float(similarity),
                    'message': 'Authentication failed. Face does not match.'
                })
        else:
            # Find best match among all users
            all_users = user_db.get_all_users()
            
            if not all_users:
                return jsonify({
                    'success': False,
                    'message': 'No users registered in the system'
                }), 404
            
            match = find_best_match(normalized_embedding, all_users, threshold=0.6)
            
            if match:
                matched_username, similarity = match
                
                # Record login attempt
                user_db.add_login_attempt(matched_username, True, float(similarity))
                
                # Set session
                session['username'] = matched_username
                session['authenticated'] = True
                
                return jsonify({
                    'success': True,
                    'authenticated': True,
                    'username': matched_username,
                    'similarity': float(similarity),
                    'message': f'Authentication successful! Welcome {matched_username}'
                })
            else:
                return jsonify({
                    'success': True,
                    'authenticated': False,
                    'message': 'No matching user found'
                })
                
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/api/users', methods=['GET'])
def get_users():
    """Get list of all registered users."""
    try:
        all_users = user_db.get_all_users()
        usernames = [username for username, _ in all_users]
        
        return jsonify({
            'success': True,
            'users': usernames,
            'count': len(usernames)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/dashboard')
def dashboard():
    """User dashboard page - requires authentication."""
    if 'authenticated' not in session or not session.get('authenticated'):
        return redirect(url_for('authenticate_page'))
    
    username = session.get('username')
    if not username:
        return redirect(url_for('authenticate_page'))
    
    return render_template('dashboard.html', username=username)


@app.route('/api/profile', methods=['GET'])
def get_profile():
    """Get user profile information."""
    if 'authenticated' not in session or not session.get('authenticated'):
        return jsonify({
            'success': False,
            'message': 'Not authenticated'
        }), 401
    
    username = session.get('username')
    if not username:
        return jsonify({
            'success': False,
            'message': 'No username in session'
        }), 401
    
    try:
        user_info = user_db.get_user_info(username)
        login_history = user_db.get_login_history(username)
        
        if not user_info:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': user_info,
            'login_history': login_history
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/api/update-face', methods=['POST'])
def update_face():
    """Update user's face embedding."""
    if 'authenticated' not in session or not session.get('authenticated'):
        return jsonify({
            'success': False,
            'message': 'Not authenticated'
        }), 401
    
    username = session.get('username')
    if not username:
        return jsonify({
            'success': False,
            'message': 'No username in session'
        }), 401
    
    try:
        data = request.json
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({
                'success': False,
                'message': 'Image is required'
            }), 400
        
        # Decode image
        image = decode_image(image_data)
        
        if image is None:
            return jsonify({
                'success': False,
                'message': 'Failed to decode image'
            }), 400
        
        # Detect face
        face = face_detector.detect_face(image)
        
        if face is None:
            return jsonify({
                'success': False,
                'message': 'No face detected in the image'
            }), 400
        
        # Extract embedding
        embedding = embedding_extractor.extract_embedding(face)
        normalized_embedding = embedding_extractor.normalize_embedding(embedding)
        
        # Update in database
        success = user_db.update_user_embedding(username, normalized_embedding)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Face embedding updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to update face embedding'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/api/delete-account', methods=['POST'])
def delete_account():
    """Delete user account."""
    if 'authenticated' not in session or not session.get('authenticated'):
        return jsonify({
            'success': False,
            'message': 'Not authenticated'
        }), 401
    
    username = session.get('username')
    if not username:
        return jsonify({
            'success': False,
            'message': 'No username in session'
        }), 401
    
    try:
        success = user_db.delete_user(username)
        
        if success:
            # Clear session
            session.clear()
            
            return jsonify({
                'success': True,
                'message': 'Account deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to delete account'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/logout')
def logout():
    """Logout user."""
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
