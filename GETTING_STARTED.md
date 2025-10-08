# Getting Started with Face Authentication System

This guide will help you set up and run the face authentication system on your local machine.

## Prerequisites

- Python 3.8 or higher
- Webcam
- Modern web browser (Chrome, Firefox, Safari, or Edge)

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/AnvithaBM/face-auth-system.git
cd face-auth-system

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note**: The first run will download the MobileNetV2 weights (~14MB) automatically.

### 2. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 3. Using the Application

#### Register a New User

1. Navigate to `http://localhost:5000`
2. Click "Register New User"
3. Enter a username (must be unique)
4. Allow webcam access when prompted
5. Position your face in the camera frame
6. Click "Capture Face"
7. Review the captured image
8. Click "Register" to save your face data

#### Authenticate

1. From the home page, click "Authenticate"
2. Choose authentication mode:
   - **Auto-detect User**: The system will identify you automatically
   - **Specific User**: Select your username from the dropdown
3. Allow webcam access when prompted
4. Position your face in the camera frame
5. Click "Capture & Authenticate"
6. View the result and similarity score

## Understanding Similarity Scores

- **90-100%**: Excellent match (same person)
- **70-90%**: Good match (likely same person)
- **60-70%**: Acceptable match (threshold is 60%)
- **Below 60%**: Not authenticated (different person or poor image quality)

## Troubleshooting

### Webcam Not Working

- Ensure your browser has permission to access the webcam
- Check that no other application is using the webcam
- Try refreshing the page

### "No face detected" Error

- Ensure your face is well-lit
- Position your face clearly in the camera frame
- Remove sunglasses or face coverings
- Try moving closer to or further from the camera

### Low Similarity Scores

- Ensure consistent lighting conditions
- Face the camera directly
- Keep a neutral expression
- Make sure the face is clearly visible and not blurry

### Import Errors

If you get import errors, ensure all dependencies are installed:

```bash
pip install -r requirements.txt --upgrade
```

### Database Issues

If you encounter database errors, delete the `users.db` file and restart:

```bash
rm users.db  # On macOS/Linux
del users.db  # On Windows
python app.py
```

## System Architecture

```
User (Browser) 
    ↓ (Webcam Capture)
JavaScript (register.js / authenticate.js)
    ↓ (Base64 Image)
Flask API (app.py)
    ↓
Face Detection (face_utils.py)
    ↓
Embedding Extraction (face_utils.py + MobileNetV2)
    ↓
Database Storage / Comparison (database.py + auth_utils.py)
    ↓ (Result)
User (Browser)
```

## API Usage

You can also interact with the system programmatically:

### Register a User

```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "image": "data:image/jpeg;base64,/9j/4AAQ..."
  }'
```

### Authenticate a User

```bash
curl -X POST http://localhost:5000/api/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "image": "data:image/jpeg;base64,/9j/4AAQ..."
  }'
```

### Get All Users

```bash
curl http://localhost:5000/api/users
```

## Performance Tips

1. **Better Lighting**: Natural lighting works best
2. **Face Position**: Center your face in the frame
3. **Distance**: Stay about 2-3 feet from the camera
4. **Consistency**: Register and authenticate under similar conditions
5. **Quality**: Use a good quality webcam if available

## Next Steps

- Explore the `face_recognition_model.ipynb` Jupyter notebook to understand the model training process
- Modify the similarity threshold in `app.py` to adjust authentication strictness
- Add liveness detection to prevent photo-based spoofing
- Implement user management features (delete users, update embeddings)
- Add HTTPS support for production deployment

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the README.md for detailed documentation
- Open an issue on GitHub

Happy authenticating! 🔐
