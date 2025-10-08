// Dashboard JavaScript
let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let captureBtn = document.getElementById('captureBtn');
let recaptureBtn = document.getElementById('recaptureBtn');
let confirmUpdateBtn = document.getElementById('confirmUpdateBtn');
let updateFaceBtn = document.getElementById('updateFaceBtn');
let deleteAccountBtn = document.getElementById('deleteAccountBtn');
let updateFaceModal = document.getElementById('updateFaceModal');
let previewContainer = document.getElementById('previewContainer');
let previewImage = document.getElementById('previewImage');
let updateMessage = document.getElementById('updateMessage');

let capturedImageData = null;
let stream = null;

// Load profile data on page load
window.addEventListener('load', loadProfileData);

async function loadProfileData() {
    try {
        const response = await fetch('/api/profile');
        const data = await response.json();
        
        if (data.success) {
            // Update profile info
            document.getElementById('username').textContent = data.user.username;
            document.getElementById('registeredDate').textContent = new Date(data.user.created_at).toLocaleString();
            
            // Update login history
            displayLoginHistory(data.login_history);
        } else {
            console.error('Failed to load profile:', data.message);
            if (response.status === 401) {
                window.location.href = '/authenticate';
            }
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

function displayLoginHistory(history) {
    const historyContainer = document.getElementById('loginHistory');
    
    if (!history || history.length === 0) {
        historyContainer.innerHTML = '<div class="empty-history">No login history available</div>';
        return;
    }
    
    historyContainer.innerHTML = '';
    
    history.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = `history-item ${item.success ? '' : 'failed'}`;
        
        const timestamp = new Date(item.timestamp).toLocaleString();
        const status = item.success ? 'Success' : 'Failed';
        const statusClass = item.success ? 'success' : 'failed';
        const similarity = item.similarity ? `(${(item.similarity * 100).toFixed(1)}% match)` : '';
        
        historyItem.innerHTML = `
            <div class="timestamp">📅 ${timestamp}</div>
            <div class="status ${statusClass}">
                ${item.success ? '✅' : '❌'} ${status} ${similarity}
            </div>
        `;
        
        historyContainer.appendChild(historyItem);
    });
}

// Update face button click
updateFaceBtn.addEventListener('click', () => {
    updateFaceModal.style.display = 'block';
    initCamera();
});

// Delete account button click
deleteAccountBtn.addEventListener('click', async () => {
    const confirmed = confirm('Are you sure you want to delete your account? This action cannot be undone.');
    
    if (confirmed) {
        try {
            const response = await fetch('/api/delete-account', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert('Account deleted successfully. You will be redirected to the home page.');
                window.location.href = '/';
            } else {
                alert('Failed to delete account: ' + data.message);
            }
        } catch (error) {
            alert('Error deleting account: ' + error.message);
        }
    }
});

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
        showUpdateMessage('Error accessing webcam: ' + error.message, 'error');
        console.error('Camera error:', error);
    }
}

// Capture image from video
captureBtn.addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    let ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    
    // Get image data as base64
    capturedImageData = canvas.toDataURL('image/jpeg', 0.95);
    
    // Show preview
    previewImage.src = capturedImageData;
    previewContainer.style.display = 'block';
    
    // Hide video, show recapture and confirm buttons
    video.style.display = 'none';
    captureBtn.style.display = 'none';
    recaptureBtn.style.display = 'inline-block';
    confirmUpdateBtn.style.display = 'inline-block';
});

// Recapture button click
recaptureBtn.addEventListener('click', () => {
    // Reset UI
    video.style.display = 'block';
    captureBtn.style.display = 'inline-block';
    recaptureBtn.style.display = 'none';
    confirmUpdateBtn.style.display = 'none';
    previewContainer.style.display = 'none';
    capturedImageData = null;
    hideUpdateMessage();
});

// Confirm update button click
confirmUpdateBtn.addEventListener('click', async () => {
    if (!capturedImageData) {
        showUpdateMessage('Please capture an image first', 'error');
        return;
    }
    
    confirmUpdateBtn.disabled = true;
    confirmUpdateBtn.textContent = '⏳ Updating...';
    
    try {
        const response = await fetch('/api/update-face', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: capturedImageData
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showUpdateMessage(data.message, 'success');
            
            // Close modal after 2 seconds
            setTimeout(() => {
                closeUpdateModal();
                loadProfileData(); // Reload profile
            }, 2000);
        } else {
            showUpdateMessage(data.message, 'error');
            confirmUpdateBtn.disabled = false;
            confirmUpdateBtn.textContent = '✅ Confirm Update';
        }
    } catch (error) {
        showUpdateMessage('Error: ' + error.message, 'error');
        confirmUpdateBtn.disabled = false;
        confirmUpdateBtn.textContent = '✅ Confirm Update';
    }
});

function closeUpdateModal() {
    updateFaceModal.style.display = 'none';
    
    // Stop camera
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    
    // Reset UI
    video.style.display = 'block';
    captureBtn.style.display = 'inline-block';
    recaptureBtn.style.display = 'none';
    confirmUpdateBtn.style.display = 'none';
    previewContainer.style.display = 'none';
    capturedImageData = null;
    hideUpdateMessage();
    confirmUpdateBtn.disabled = false;
    confirmUpdateBtn.textContent = '✅ Confirm Update';
}

function showUpdateMessage(message, type) {
    updateMessage.textContent = message;
    updateMessage.className = `message ${type}`;
    updateMessage.style.display = 'block';
}

function hideUpdateMessage() {
    updateMessage.style.display = 'none';
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    if (event.target === updateFaceModal) {
        closeUpdateModal();
    }
});
