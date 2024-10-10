document.addEventListener("DOMContentLoaded", function () {
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");
    const chatBody = document.getElementById("chatBody");

    sendBtn.addEventListener("click", function () {
        const userMessage = chatInput.value.trim();
        if (userMessage) {
            addMessageToChat("user-message", userMessage);
            fetchChatbotResponse(userMessage);
            chatInput.value = "";  // Clear the input field
        }
    });

    // Send message on 'Enter' key press
    chatInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            sendBtn.click();
        }
    });

    function addMessageToChat(className, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add(className);
        const messageContent = document.createElement("div");
        messageContent.classList.add("message-content");
        messageContent.textContent = message;
        messageDiv.appendChild(messageContent);
        chatBody.appendChild(messageDiv);
        chatBody.scrollTop = chatBody.scrollHeight;  // Scroll to bottom
    }

    function fetchChatbotResponse(userMessage) {
        fetch("/get", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ "msg": userMessage })
        })
        .then(response => response.json())
        .then(data => {
            addMessageToChat("bot-message", data.response);
        })
        .catch(error => {
            console.error("Error:", error);
            addMessageToChat("bot-message", "Sorry, something went wrong.");
        });
    }
});
