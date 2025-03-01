const chatIcon = document.getElementById('chat-icon');
const chatBox = document.getElementById('chat-box');
const chatClose = document.getElementById('chat-close');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');

// Open Chat & Blur Background
chatIcon.addEventListener('click', () => {
    chatBox.classList.add('active');
    document.body.classList.add('blurred');
});

// Close Chat & Remove Blur
chatClose.addEventListener('click', () => {
    chatBox.classList.remove('active');
    document.body.classList.remove('blurred');
});

// Send Message when Clicking Send Button
chatSend.addEventListener('click', sendMessage);

// Send Message on Enter Key Press
chatInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault(); 
        sendMessage();
    }
});

// Send Message Function
async function sendMessage() {
    const message = chatInput.value.trim();
    if (message) {
        addMessage(message); // Show user message
        chatInput.value = '';

        // Send to Backend
        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            addMessage(data.reply, false); // Show bot response
        } catch (error) {
            console.error("Error:", error);
            addMessage("Error: Could not connect to the AI server.", false);
        }
    }
}

// Add Message to Chat Box
function addMessage(message, isUser = true) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', isUser ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);

    // Add a line break between messages
    chatMessages.appendChild(document.createElement('br'));

    chatMessages.scrollTop = chatMessages.scrollHeight;
}
