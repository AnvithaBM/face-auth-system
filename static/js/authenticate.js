// Authenticate page JavaScript
let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let captureBtn = document.getElementById('captureBtn');
let retryBtn = document.getElementById('retryBtn');
let usernameSelect = document.getElementById('username');
let usernameGroup = document.getElementById('usernameGroup');
let messageDiv = document.getElementById('message');
let previewContainer = document.getElementById('previewContainer');
let previewImage = document.getElementById('previewImage');

let stream = null;
let authMode = 'auto';

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

// Load registered users
async function loadUsers() {
    try {
        const response = await fetch('/api/users');
        const data = await response.json();
        
        if (data.success && data.users.length > 0) {
            usernameSelect.innerHTML = '<option value="">-- Select User --</option>';
            data.users.forEach(username => {
                const option = document.createElement('option');
                option.value = username;
                option.textContent = username;
                usernameSelect.appendChild(option);
            });
        } else {
            usernameSelect.innerHTML = '<option value="">No users registered</option>';
        }
    } catch (error) {
        console.error('Error loading users:', error);
        usernameSelect.innerHTML = '<option value="">Error loading users</option>';
    }
}

// Capture and authenticate
async function captureAndAuthenticate() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    let ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    
    // Get image data as base64
    const capturedImageData = canvas.toDataURL('image/jpeg', 0.95);
    
    // Show preview
    previewImage.src = capturedImageData;
    previewContainer.style.display = 'block';
    
    // Disable capture button
    captureBtn.disabled = true;
    showMessage('Authenticating...', 'info');
    
    // Prepare request data
    const requestData = {
        image: capturedImageData
    };
    
    // Add username if specific user mode
    if (authMode === 'specific') {
        const selectedUsername = usernameSelect.value;
        if (!selectedUsername) {
            showMessage('Please select a username', 'error');
            captureBtn.disabled = false;
            return;
        }
        requestData.username = selectedUsername;
    }
    
    try {
        const response = await fetch('/api/authenticate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.authenticated) {
                let message = data.message;
                if (data.similarity) {
                    message += `<div class="similarity-score">Similarity Score: ${(data.similarity * 100).toFixed(2)}%</div>`;
                }
                showMessage(message, 'success');
                
                // Redirect to dashboard after 2 seconds
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            } else {
                let message = data.message;
                if (data.similarity !== undefined) {
                    message += `<div class="similarity-score">Similarity Score: ${(data.similarity * 100).toFixed(2)}%</div>`;
                }
                showMessage(message, 'error');
            }
        } else {
            showMessage(data.message, 'error');
        }
        
        // Show retry button
        video.style.display = 'none';
        captureBtn.style.display = 'none';
        retryBtn.style.display = 'inline-block';
        
    } catch (error) {
        showMessage('Error during authentication: ' + error.message, 'error');
        captureBtn.disabled = false;
    }
}

// Retry authentication
function retry() {
    previewContainer.style.display = 'none';
    video.style.display = 'block';
    captureBtn.style.display = 'inline-block';
    captureBtn.disabled = false;
    retryBtn.style.display = 'none';
    hideMessage();
}

// Show message
function showMessage(text, type) {
    messageDiv.innerHTML = text;
    messageDiv.className = 'message ' + type;
    messageDiv.style.display = 'block';
}

// Hide message
function hideMessage() {
    messageDiv.style.display = 'none';
}

// Handle auth mode change
document.querySelectorAll('input[name="authMode"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        authMode = e.target.value;
        if (authMode === 'specific') {
            usernameGroup.style.display = 'block';
        } else {
            usernameGroup.style.display = 'none';
        }
    });
});

// Event listeners
captureBtn.addEventListener('click', captureAndAuthenticate);
retryBtn.addEventListener('click', retry);

// Initialize on page load
initCamera();
loadUsers();
