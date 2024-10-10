document.addEventListener("DOMContentLoaded", function () {
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");
    const chatBody = document.getElementById("chatBody");
    const typingIndicator = document.createElement("div"); // Create a typing indicator element
    typingIndicator.classList.add("typing-indicator");
    typingIndicator.textContent = "Typing..."; // Text for the typing indicator

    sendBtn.addEventListener("click", function () {
        const userMessage = chatInput.value.trim();
        if (userMessage) {
            addMessageToChat("user-message", userMessage);
            chatInput.value = ""; // Clear the input field
            fetchChatbotResponse(userMessage);
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
        messageContent.innerHTML = formatResponse(message); // Use innerHTML for formatted response
        messageDiv.appendChild(messageContent);
        chatBody.appendChild(messageDiv);
        chatBody.scrollTop = chatBody.scrollHeight; // Scroll to bottom
    }

    function fetchChatbotResponse(userMessage) {
        // Show typing indicator
        chatBody.appendChild(typingIndicator);
        typingIndicator.style.display = "block"; // Show the typing indicator

        fetch("/get", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ "msg": userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Hide typing indicator
            typingIndicator.style.display = "none"; // Hide the typing indicator
            addMessageToChat("bot-message", data.response);
        })
        .catch(error => {
            console.error("Error:", error);
            typingIndicator.style.display = "none"; // Hide typing indicator on error
            addMessageToChat("bot-message", "Sorry, something went wrong.");
        });
    }

    function formatResponse(response) {
        // Replace double asterisks with strong tags
        response = response.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>'); 
        // Replace single asterisks with list items
        const bulletPoints = response.match(/\* (.*?)(?=\n|\*$)/g); // Capture bullet points
        if (bulletPoints) {
            response = response.replace(/\* (.*?)(?=\n|\*$)/g, '<li>$1</li>'); // Replace with <li> tags
            response = `<ul>${response}</ul>`; // Wrap all <li> in a <ul>
        }
        // Replace newlines with <br> for line breaks
        return response.replace(/\n/g, '<br>');
    }
});
