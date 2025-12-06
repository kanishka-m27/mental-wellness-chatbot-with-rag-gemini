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

  sendButton.addEventListener("click", () => {
    const message = userInput.value.trim();
    if (!message) return;

    // Shows the user message
    addMessage("user", message);
    userInput.value = "";

    // Send to the Flask backend
    fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: message })
    })
      .then(response => response.json())
      .then(data => {
        addMessage("bot", data.reply);
      })
      .catch(error => {
        console.error("Error:", error);
        addMessage("bot", "Sorry, something went wrong. Please try again.");
      });
  });

  userInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      sendButton.click();
    }
  });
});
