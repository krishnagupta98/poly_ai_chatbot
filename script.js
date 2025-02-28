const chatIcon = document.getElementById('chat-icon');
const chatBox = document.getElementById('chat-box');
const chatClose = document.getElementById('chat-close');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');

chatIcon.addEventListener('click', () => {
    chatBox.classList.add('active');
});

chatClose.addEventListener('click', () => {
    chatBox.classList.remove('active');
});

chatSend.addEventListener('click', async () => {
    const message = chatInput.value.trim();
    if (message) {
        addMessage(message);  // Display user message
        chatInput.value = '';

        // Send message to backend
        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            addMessage(data.reply, false);  // Display bot response
        } catch (error) {
            console.error("Error:", error);
            addMessage("Error: Could not connect to the AI server.", false);
        }
    }
});

function addMessage(message, isUser = true) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message');
    messageElement.classList.add(isUser ? 'user-message' : 'bot-message'); 
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight; 
}
