function submitForm() {
    document.getElementById('loading-message').style.display = 'block';
}

function showNotification() {
    const notification = document.getElementById('notification');
    notification.style.display = 'block';
    // Hide notification after 3 seconds
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

var copyBtn = document.getElementById('copyBtn');
if (copyBtn) {
    copyBtn.addEventListener('click', function() {
        const textarea = document.getElementById('answer');
        navigator.clipboard.writeText(textarea.value)
        .then(() => {
            showNotification();
        })
        .catch(err => {
            console.error('Failed to copy text: ', err);
            alert('Failed to copy code!');
        });
    });
}