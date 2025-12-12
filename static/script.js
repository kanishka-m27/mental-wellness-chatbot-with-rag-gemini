document.addEventListener("DOMContentLoaded", function () {
  const sendButton = document.querySelector("button");
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  function addMessage(role, text) {
    const msg = document.createElement("div");
    msg.classList.add(role === "user" ? "user-message" : "bot-message");
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function showTypingIndicator() {
    const typing = document.createElement("div");
    typing.classList.add("typing-indicator");
    typing.textContent = "⏳ MindConnect is typing...";
    typing.setAttribute("id", "typing");
    chatBox.appendChild(typing);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function removeTypingIndicator() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
  }

  sendButton.addEventListener("click", () => {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage("user", message);
    userInput.value = "";

    showTypingIndicator();

    fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: message })
    })
      .then(response => response.json())
      .then(data => {
        removeTypingIndicator();
        addMessage("bot", data.reply);
      })
      .catch(error => {
        removeTypingIndicator();
        addMessage("bot", "Sorry, something went wrong. Please try again.");
      });
  });

  userInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      sendButton.click();
    }
  });
});
