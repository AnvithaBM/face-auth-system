# System Flow Diagrams

## Registration Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER REGISTRATION                          │
└─────────────────────────────────────────────────────────────────────┘

1. User Interface (Browser)
   │
   ├─► Navigate to http://localhost:5000/register
   │
   └─► Enter username: "john_doe"
       │
       └─► Allow webcam access
           │
           └─► Webcam stream starts (getUserMedia API)
               │
               └─► User clicks "Capture Face"
                   │
                   ┌─────────────────────────────────────┐
                   │  JavaScript (register.js)           │
                   │  ├─ Capture frame from video        │
                   │  ├─ Draw to canvas                  │
                   │  ├─ Convert to Base64 JPEG          │
                   │  └─ POST to /api/register           │
                   └─────────────────────────────────────┘
                   │
                   ┌─────────────────────────────────────┐
                   │  Flask Backend (app.py)             │
                   │  ├─ Decode Base64 image             │
                   │  ├─ Check username uniqueness       │
                   │  └─ Call face detection             │
                   └─────────────────────────────────────┘
                   │
                   ┌─────────────────────────────────────┐
                   │  Face Detection (face_utils.py)     │
                   │  ├─ Convert to grayscale            │
                   │  ├─ Haar Cascade detection          │
                   │  ├─ Extract largest face            │
                   │  └─ Return face region              │
                   └─────────────────────────────────────┘
                   │
                   ┌─────────────────────────────────────┐
                   │  Embedding Extraction (face_utils)  │
                   │  ├─ Resize to 224x224               │
                   │  ├─ Convert BGR→RGB                 │
                   │  ├─ Preprocess for MobileNetV2      │
                   │  ├─ Extract 1280-dim embedding      │
                   │  └─ L2 normalize                    │
                   └─────────────────────────────────────┘
                   │
                   ┌─────────────────────────────────────┐
                   │  Database (database.py)             │
                   │  ├─ Serialize embedding to JSON     │
                   │  ├─ INSERT into users table         │
                   │  ├─ Store (username, embedding)     │
                   │  └─ Commit transaction              │
                   └─────────────────────────────────────┘
                   │
                   └─► Success response
                       │
                       └─► Display "User registered successfully!"
```

## Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER AUTHENTICATION                          │
└─────────────────────────────────────────────────────────────────────┘

1. User Interface (Browser)
   │
   ├─► Navigate to http://localhost:5000/authenticate
   │
   └─► Select authentication mode:
       │
       ├─► AUTO-DETECT MODE              ├─► SPECIFIC USER MODE
       │   (Find best match)             │   (Verify against one user)
       │                                 │
       │                                 └─► Select username from dropdown
       │                                     (Loaded via /api/users)
       │
       └─► Allow webcam access
           │
           └─► Webcam stream starts
               │
               └─► User clicks "Capture & Authenticate"
                   │
                   ┌─────────────────────────────────────┐
                   │  JavaScript (authenticate.js)       │
                   │  ├─ Capture frame from video        │
                   │  ├─ Draw to canvas                  │
                   │  ├─ Convert to Base64 JPEG          │
                   │  └─ POST to /api/authenticate       │
                   └─────────────────────────────────────┘
                   │
                   ┌─────────────────────────────────────┐
                   │  Flask Backend (app.py)             │
                   │  ├─ Decode Base64 image             │
                   │  └─ Call face detection             │
                   └─────────────────────────────────────┘
                   │
                   ┌─────────────────────────────────────┐
                   │  Face Detection (face_utils.py)     │
                   │  └─ Extract face region             │
                   └─────────────────────────────────────┘
                   │
                   ┌─────────────────────────────────────┐
                   │  Embedding Extraction               │
                   │  ├─ Extract 1280-dim embedding      │
                   │  └─ L2 normalize                    │
                   └─────────────────────────────────────┘
                   │
                   ┌────────────────────────────────────────────────┐
                   │  Authentication Logic                          │
                   │                                                │
                   │  IF specific user mode:                        │
                   │  ├─ Get stored embedding from DB               │
                   │  ├─ Calculate cosine similarity                │
                   │  └─ Compare with threshold (0.6)               │
                   │                                                │
                   │  IF auto-detect mode:                          │
                   │  ├─ Get all users from DB                      │
                   │  ├─ Calculate similarity with each             │
                   │  ├─ Find highest similarity                    │
                   │  └─ Compare with threshold (0.6)               │
                   └────────────────────────────────────────────────┘
                   │
                   ├─► IF similarity >= 0.6
                   │   └─► ✅ AUTHENTICATED
                   │       "Welcome [username]!"
                   │       Similarity: 87%
                   │
                   └─► IF similarity < 0.6
                       └─► ❌ NOT AUTHENTICATED
                           "Face does not match"
                           Similarity: 43%
```

## Data Storage Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SQLite Database (users.db)                   │
└─────────────────────────────────────────────────────────────────────┘

Table: users
┌────┬──────────────┬─────────────────────────────┬──────────────────────┐
│ id │  username    │         embedding           │     created_at       │
├────┼──────────────┼─────────────────────────────┼──────────────────────┤
│ 1  │ "john_doe"   │ "[0.123, -0.456, ..., ]"    │ 2024-01-15 10:30:00  │
│ 2  │ "jane_smith" │ "[-0.234, 0.567, ..., ]"    │ 2024-01-15 11:45:00  │
│ 3  │ "bob_wilson" │ "[0.345, -0.678, ..., ]"    │ 2024-01-15 14:20:00  │
└────┴──────────────┴─────────────────────────────┴──────────────────────┘
        (UNIQUE)          (1280 floats as JSON)         (AUTO)

Embedding Structure:
[0.123, -0.456, 0.789, ..., -0.234]  ← 1280 dimensions
 ↑
 L2 normalized: √(sum of squares) = 1.0
```

## Component Dependencies

```
┌─────────────────────────────────────────────────────────────────────┐
│                         System Components                           │
└─────────────────────────────────────────────────────────────────────┘

app.py (Flask Web Application)
  │
  ├─► src/face_utils.py
  │   ├─► FaceDetector
  │   │   └─► OpenCV (cv2.CascadeClassifier)
  │   │       └─► haarcascade_frontalface_default.xml
  │   │
  │   └─► EmbeddingExtractor
  │       └─► TensorFlow/Keras
  │           └─► MobileNetV2 (pre-trained on ImageNet)
  │               └─► GlobalAveragePooling2D
  │
  ├─► src/database.py
  │   └─► UserDatabase
  │       └─► SQLite3
  │           ├─► JSON (for serialization)
  │           └─► NumPy (for arrays)
  │
  └─► src/auth_utils.py
      ├─► cosine_similarity()
      ├─► authenticate_user()
      └─► find_best_match()
          └─► NumPy (for calculations)

templates/*.html
  │
  └─► static/js/*.js
      ├─► WebRTC (getUserMedia)
      ├─► Canvas API (image capture)
      └─► Fetch API (AJAX requests)

face_recognition_model.ipynb
  │
  ├─► TensorFlow/Keras (model building)
  ├─► NumPy (data processing)
  ├─► Matplotlib (visualization)
  └─► scikit-learn (utilities)
```

## Similarity Calculation

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Cosine Similarity Calculation                  │
└─────────────────────────────────────────────────────────────────────┘

Stored Embedding (from DB):
  E1 = [0.123, -0.456, 0.789, ..., -0.234]  (1280 dims)

Live Embedding (from camera):
  E2 = [0.125, -0.451, 0.791, ..., -0.231]  (1280 dims)

Step 1: Normalize (L2)
  E1_norm = E1 / ||E1||
  E2_norm = E2 / ||E2||

Step 2: Dot Product
  similarity = E1_norm · E2_norm
             = sum(E1_norm[i] × E2_norm[i]) for all i

Step 3: Result
  similarity ∈ [0, 1]
  
  0.0 ────────────── 0.6 ────────────────── 1.0
  Different        Threshold            Same Person
   Person                               (Perfect Match)

Examples:
  Same person:       0.85 - 0.99  ✅ AUTHENTICATED
  Similar person:    0.60 - 0.85  ✅ AUTHENTICATED (borderline)
  Different person:  0.20 - 0.59  ❌ NOT AUTHENTICATED
```

## File Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                           File Organization                         │
└─────────────────────────────────────────────────────────────────────┘

Project Root
│
├─ Configuration & Setup
│  ├─ requirements.txt      → Python dependencies
│  ├─ .gitignore           → Git ignore rules
│  ├─ run.sh               → Unix startup script
│  └─ run.bat              → Windows startup script
│
├─ Documentation
│  ├─ README.md            → Main documentation
│  ├─ GETTING_STARTED.md   → User guide
│  ├─ ARCHITECTURE.md      → System architecture
│  ├─ PROJECT_SUMMARY.md   → Deliverables summary
│  └─ SYSTEM_FLOW.md       → This file (flow diagrams)
│
├─ Application Entry Point
│  └─ app.py               → Flask web application
│
├─ Research & Training
│  └─ face_recognition_model.ipynb → Model training notebook
│
├─ Backend Modules (src/)
│  ├─ __init__.py          → Package marker
│  ├─ face_utils.py        → Face detection & embeddings
│  ├─ database.py          → SQLite operations
│  └─ auth_utils.py        → Authentication logic
│
├─ Frontend UI (templates/)
│  ├─ index.html           → Landing page
│  ├─ register.html        → Registration UI
│  └─ authenticate.html    → Authentication UI
│
└─ Client Scripts (static/js/)
   ├─ register.js          → Registration logic
   └─ authenticate.js      → Authentication logic

Generated at Runtime:
   └─ users.db             → SQLite database (created on first run)
```

## Technology Stack Visualization

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Technology Stack                            │
└─────────────────────────────────────────────────────────────────────┘

Frontend Layer
┌──────────────────────────────────────────────────────────────────┐
│ HTML5 │ CSS3 (Gradients) │ JavaScript ES6+ │ WebRTC │ Canvas   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ↓ HTTP/JSON
                              │
Application Layer
┌──────────────────────────────────────────────────────────────────┐
│                    Flask 2.3.3 (Python Web Framework)            │
│  ├─ Routing                                                      │
│  ├─ Request/Response Handling                                    │
│  ├─ JSON Serialization                                           │
│  └─ Template Rendering                                           │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ↓
Business Logic Layer
┌──────────────────────────────────────────────────────────────────┐
│  Face Detection          Embedding Extraction    Authentication  │
│  ┌──────────────┐       ┌────────────────┐      ┌─────────────┐ │
│  │ OpenCV       │       │ TensorFlow     │      │ NumPy       │ │
│  │ Haar Cascade │  →    │ MobileNetV2    │  →   │ Cosine Sim  │ │
│  └──────────────┘       └────────────────┘      └─────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ↓
Data Layer
┌──────────────────────────────────────────────────────────────────┐
│                    SQLite3 Database (users.db)                   │
│  ├─ User Management                                              │
│  ├─ Embedding Storage (JSON)                                     │
│  └─ Timestamp Tracking                                           │
└──────────────────────────────────────────────────────────────────┘

Supporting Libraries
┌──────────────────────────────────────────────────────────────────┐
│ NumPy │ scikit-learn │ Pillow │ scipy │ matplotlib │ jupyter    │
└──────────────────────────────────────────────────────────────────┘
```

---

**Note**: These diagrams provide a visual overview of how the face authentication system works, from user interaction to data storage and processing.
