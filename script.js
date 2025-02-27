/* POLY.js */
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

chatSend.addEventListener('click', () => {
    const message = chatInput.value.trim();
    if (message) {
        addMessage(message);
        chatInput.value = '';
        // send the message to your backend and receive a response.
        setTimeout(() => {
            addMessage("This is a dummy response.", false);
        }, 500);
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