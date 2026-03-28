const API_URL = "http://localhost:8000";
const chatContainer = document.getElementById("chatContainer");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

let conversationHistory = [];
let userLat = null;
let userLng = null;
let userLocation = "";

// Request geolocation on load
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      userLat = pos.coords.latitude;
      userLng = pos.coords.longitude;
      userLocation = `${userLat.toFixed(4)}, ${userLng.toFixed(4)}`;
      const indicator = document.getElementById("locationIndicator");
      if (indicator) {
        indicator.textContent = "📍 Location detected";
        indicator.style.color = "#22c55e";
      }
    },
    () => {
      const indicator = document.getElementById("locationIndicator");
      if (indicator) {
        indicator.textContent = "📍 Location unavailable";
        indicator.style.color = "#94a3b8";
      }
    }
  );
}

document.querySelectorAll(".cat-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    userInput.value = btn.getAttribute("data-query");
    sendMessage();
  });
});

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userInput.value = "";
  sendBtn.disabled = true;

  const typingEl = showTyping();

  try {
    const res = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        conversation_history: conversationHistory,
        user_location: userLocation,
        user_lat: userLat,
        user_lng: userLng,
      }),
    });

    const data = await res.json();
    typingEl.remove();
    addMessage(data.reply, "bot");

    conversationHistory.push({ role: "user", content: message });
    conversationHistory.push({ role: "assistant", content: data.reply });

    if (conversationHistory.length > 20) {
      conversationHistory = conversationHistory.slice(-20);
    }
  } catch (err) {
    typingEl.remove();
    addMessage(
      "Sorry, I'm having trouble connecting right now. Please try again, or call 211 for immediate help.",
      "bot"
    );
    console.error("Error:", err);
  }

  sendBtn.disabled = false;
  userInput.focus();
}

function addMessage(text, sender) {
  const msgDiv = document.createElement("div");
  msgDiv.className = `message ${sender}-message`;

  const content = document.createElement("div");
  content.className = "message-content";

  if (sender === "bot") {
    content.innerHTML = `<strong>ATL Connect</strong>${formatResponse(text)}`;
  } else {
    content.innerHTML = `<p>${escapeHtml(text)}</p>`;
  }

  msgDiv.appendChild(content);
  chatContainer.appendChild(msgDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function formatResponse(text) {
  // Markdown links → <a> tags (safe: only allow http/https URLs)
  text = text.replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g, (_, label, url) => {
    const safeUrl = url.replace(/"/g, "%22");
    return `<a href="${safeUrl}" target="_blank" rel="noopener noreferrer">${label}</a>`;
  });
  text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  text = text.replace(/^(\d+)\.\s/gm, "<br><strong>$1.</strong> ");
  return text
    .split("\n\n")
    .map((p) => `<p>${p.replace(/\n/g, "<br>")}</p>`)
    .join("");
}

function showTyping() {
  const el = document.createElement("div");
  el.className = "message bot-message";
  el.innerHTML = `
    <div class="message-content">
      <strong>ATL Connect</strong>
      <div class="typing-indicator">
        <span></span><span></span><span></span>
      </div>
    </div>`;
  chatContainer.appendChild(el);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  return el;
}

function escapeHtml(text) {
  const d = document.createElement("div");
  d.textContent = text;
  return d.innerHTML;
}
