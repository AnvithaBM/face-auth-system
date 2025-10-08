// Register page JavaScript
let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let captureBtn = document.getElementById('captureBtn');
let recaptureBtn = document.getElementById('recaptureBtn');
let registerBtn = document.getElementById('registerBtn');
let usernameInput = document.getElementById('username');
let messageDiv = document.getElementById('message');
let previewContainer = document.getElementById('previewContainer');
let previewImage = document.getElementById('previewImage');

let capturedImageData = null;
let stream = null;

// Initialize webcam
async function initCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user'
            } 
        });
        video.srcObject = stream;
    } catch (error) {
        showMessage('Error accessing webcam: ' + error.message, 'error');
        console.error('Camera error:', error);
    }
}

// Capture image from video
function captureImage() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    let ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    
    // Get image data as base64
    capturedImageData = canvas.toDataURL('image/jpeg', 0.95);
    
    // Show preview
    previewImage.src = capturedImageData;
    previewContainer.style.display = 'block';
    
    // Hide video, show recapture and register buttons
    video.style.display = 'none';
    captureBtn.style.display = 'none';
    recaptureBtn.style.display = 'inline-block';
    registerBtn.style.display = 'inline-block';
}

// Recapture image
function recapture() {
    capturedImageData = null;
    previewContainer.style.display = 'none';
    video.style.display = 'block';
    captureBtn.style.display = 'inline-block';
    recaptureBtn.style.display = 'none';
    registerBtn.style.display = 'none';
    hideMessage();
}

// Register user
async function registerUser() {
    const username = usernameInput.value.trim();
    
    if (!username) {
        showMessage('Please enter a username', 'error');
        return;
    }
    
    if (!capturedImageData) {
        showMessage('Please capture an image first', 'error');
        return;
    }
    
    // Disable buttons during registration
    registerBtn.disabled = true;
    recaptureBtn.disabled = true;
    
    showMessage('Registering user...', 'info');
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                image: capturedImageData
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(data.message, 'success');
            
            // Clear form after successful registration
            setTimeout(() => {
                usernameInput.value = '';
                recapture();
            }, 2000);
        } else {
            showMessage(data.message, 'error');
            registerBtn.disabled = false;
            recaptureBtn.disabled = false;
        }
        
    } catch (error) {
        showMessage('Error registering user: ' + error.message, 'error');
        registerBtn.disabled = false;
        recaptureBtn.disabled = false;
    }
}

// Show message
function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = 'message ' + type;
    messageDiv.style.display = 'block';
}

// Hide message
function hideMessage() {
    messageDiv.style.display = 'none';
}

// Event listeners
captureBtn.addEventListener('click', captureImage);
recaptureBtn.addEventListener('click', recapture);
registerBtn.addEventListener('click', registerUser);

// Initialize camera on page load
initCamera();
