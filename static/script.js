
const input = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");

function addMessage(message, type) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${type}-message`;

    if (type === "bot") {
        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.textContent = "AI";

        const content = document.createElement("div");
        content.className = "message-content";

        const name = document.createElement("div");
        name.className = "name";
        name.textContent = "Study Assistant";

        const bubble = document.createElement("div");
        bubble.className = "bubble";
        bubble.textContent = message;

        content.append(name, bubble);
        messageDiv.append(avatar, content);
    } else {
        const content = document.createElement("div");
        content.className = "message-content";

        const bubble = document.createElement("div");
        bubble.className = "bubble";
        bubble.textContent = message;

        content.appendChild(bubble);
        messageDiv.appendChild(content);
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = input.value.trim();

    if (!message || sendButton.disabled) return;

    addMessage(message, "user");
    input.value = "";
    sendButton.disabled = true;

    const typing = document.createElement("div");
    typing.className = "typing";
    typing.textContent = "Study Assistant is typing...";
    chatBox.appendChild(typing);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.response || "Request failed");
        }

        addMessage(data.response, "bot");
    } catch (error) {
        addMessage(
            "I couldn't connect to the server. Please check that Flask is running and try again.",
            "bot"
        );
    } finally {
        typing.remove();
        sendButton.disabled = false;
        input.focus();
    }
}

function sendSuggestion(message) {
    input.value = message;
    sendMessage();
}

input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});