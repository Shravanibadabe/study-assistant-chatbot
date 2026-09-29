const input = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");

// Convert Gemini's Markdown response into formatted HTML.
function formatBotAnswer(text) {
    const escapeHtml = (value) =>
        value.replace(/[&<>"']/g, (char) => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        }[char]));

    // Format inline Markdown after escaping HTML.
    function formatInline(value) {
        return value
            .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
            .replace(/\*(.+?)\*/g, "<em>$1</em>")
            .replace(/`(.+?)`/g, "<code>$1</code>");
    }

    const lines = escapeHtml(String(text ?? "")).split(/\r?\n/);
    const output = [];
    let inList = false;

    function closeList() {
        if (inList) {
            output.push("</ul>");
            inList = false;
        }
    }

    for (const line of lines) {
        const trimmed = line.trim();

        if (!trimmed) {
            closeList();
            continue;
        }

        // Headings: #, ##, or ###
        const heading = trimmed.match(/^#{1,3}\s+(.+)$/);
        if (heading) {
            closeList();
            output.push(`<h3>${formatInline(heading[1])}</h3>`);
            continue;
        }

        // Bullets: - item or * item
        const bullet = trimmed.match(/^[-*]\s+(.+)$/);
        if (bullet) {
            if (!inList) {
                output.push("<ul>");
                inList = true;
            }

            output.push(`<li>${formatInline(bullet[1])}</li>`);
            continue;
        }

        // Numbered list items: 1. item
        const numbered = trimmed.match(/^\d+[.)]\s+(.+)$/);
        if (numbered) {
            closeList();
            output.push(`<p>${formatInline(numbered[0])}</p>`);
            continue;
        }

        closeList();
        output.push(`<p>${formatInline(trimmed)}</p>`);
    }

    closeList();
    return output.join("");
}

// Add a chat message to the conversation.
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

        // Render formatted answer for bot messages.
        bubble.innerHTML = formatBotAnswer(message);

        content.append(name, bubble);
        messageDiv.append(avatar, content);
    } else {
        const content = document.createElement("div");
        content.className = "message-content";

        const bubble = document.createElement("div");
        bubble.className = "bubble";

        // Keep user messages as plain text.
        bubble.textContent = message;

        content.appendChild(bubble);
        messageDiv.appendChild(content);
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send the student's message to Flask.
async function sendMessage() {
    const message = input.value.trim();

    if (!message || sendButton.disabled) {
        return;
    }

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

        addMessage(
            data.response || "I couldn't generate a response. Please try again.",
            "bot"
        );
    } catch (error) {
        console.error("Chat request error:", error);

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

// Fill the input with a suggested question and send it.
function sendSuggestion(message) {
    input.value = message;
    sendMessage();
}

// Press Enter to send (Shift+Enter can be used for a new line if input is a textarea).
input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});