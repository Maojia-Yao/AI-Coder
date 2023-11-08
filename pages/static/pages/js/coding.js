// Function to display a loading message when a form is submitted
function submitForm() {
    // Access the element with id 'loading-message' and change its display style to 'block', making it visible
    document.getElementById('loading-message').style.display = 'block';
}

// Function to show a notification on the coding page
function showNotification() {
    const notification = document.getElementById('notification');
    notification.style.display = 'block';

    // Set a timer to hide the notification after 3 seconds
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

// Access the button element with id 'copyBtn'
var copyBtn = document.getElementById('copyBtn');
if (copyBtn) {
    copyBtn.addEventListener('click', function() {
        const textarea = document.getElementById('answer');
        // Use the Clipboard API to copy the value of the textarea
        navigator.clipboard.writeText(textarea.value)
        .then(() => {
            // If the copy operation succeeds, show a notification
            showNotification();
        })
        .catch(err => {
            // If the copy operation fails, log the error to the console and alert the user
            console.error('Failed to copy text: ', err);
            alert('Failed to copy code!');
        });
    });
}