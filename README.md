# Face Authentication System

A complete face-based person authentication system using deep learning and computer vision.

## Features

- **Face Detection**: Automatic face detection using OpenCV Haar Cascades
- **Face Recognition**: Deep learning-based face embedding extraction using MobileNetV2
- **User Registration**: Web interface to register new users with facial data
- **Authentication**: Verify user identity through face comparison
- **Database Storage**: SQLite database for storing user embeddings
- **Web Interface**: Flask-based web application with live webcam capture

## Project Structure

```
face-auth-system/
├── app.py                          # Flask web application
├── requirements.txt                # Python dependencies
├── face_recognition_model.ipynb    # Jupyter notebook for model training
├── src/
│   ├── face_utils.py              # Face detection and embedding extraction
│   ├── database.py                # SQLite database management
│   └── auth_utils.py              # Authentication utilities
├── templates/
│   ├── index.html                 # Home page
│   ├── register.html              # User registration page
│   └── authenticate.html          # Authentication page
└── static/
    └── js/
        ├── register.js            # Registration page JavaScript
        └── authenticate.js        # Authentication page JavaScript
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AnvithaBM/face-auth-system.git
cd face-auth-system
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. **Register a new user**:
   - Click "Register New User"
   - Enter a username
   - Allow webcam access
   - Click "Capture Face" to take a photo
   - Click "Register" to save the user

4. **Authenticate**:
   - Click "Authenticate"
   - Choose authentication mode:
     - Auto-detect: System finds the best matching user
     - Specific User: Verify against a specific registered user
   - Click "Capture & Authenticate"
   - View the authentication result and similarity score

### Working with the Jupyter Notebook

The `face_recognition_model.ipynb` notebook demonstrates:
- Preprocessing hyperspectral data (UWA HSFD database) to grayscale
- Building a CNN model for face embeddings
- Training with triplet loss
- Using pre-trained models

To run the notebook:
```bash
jupyter notebook face_recognition_model.ipynb
```

## Technical Details

### Face Detection
- Uses OpenCV's Haar Cascade classifier
- Detects faces in real-time from webcam input
- Extracts face regions with padding for better recognition

### Face Embedding
- Based on MobileNetV2 pre-trained on ImageNet
- Extracts 1280-dimensional embeddings
- L2 normalization for consistent comparisons
- Works with RGB images from webcam

### Authentication
- Cosine similarity for embedding comparison
- Threshold: 0.6 (configurable)
- Supports both specific user and auto-detection modes

### Database
- SQLite for lightweight storage
- Stores username and normalized embeddings
- JSON serialization for numpy arrays

## API Endpoints

- `GET /` - Home page
- `GET /register` - Registration page
- `GET /authenticate` - Authentication page
- `POST /api/register` - Register new user
- `POST /api/authenticate` - Authenticate user
- `GET /api/users` - Get list of registered users

## Configuration

### Similarity Threshold
Modify the threshold in `app.py`:
```python
authenticate_user(embedding1, embedding2, threshold=0.6)
```

### Database Path
Change database location in `app.py`:
```python
user_db = UserDatabase('users.db')
```

## Requirements

- Python 3.8+
- Webcam
- Modern web browser with webcam support

## Security Notes

- This is a demonstration project
- For production use, add:
  - HTTPS/SSL
  - User authentication
  - Rate limiting
  - Input validation
  - Secure database storage
  - Anti-spoofing measures (liveness detection)

## License

MIT License

## Acknowledgments

- UWA HSFD hyperspectral face database for research purposes
- TensorFlow and Keras for deep learning framework
- OpenCV for computer vision capabilities
- Flask for web framework

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.