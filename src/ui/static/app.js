const messages = document.getElementById("messages");
const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const statusEl = document.getElementById("status");
const sampleButton = document.getElementById("sampleButton");
const downloadLink = document.getElementById("downloadLink");
const observationsLink = document.getElementById("observationsLink");

let sessionId = null;

function addMessage(role, content) {
  const item = document.createElement("div");
  item.className = `message ${role}`;
  item.setAttribute("role", "listitem");
  item.textContent = content;
  messages.appendChild(item);
  messages.scrollTop = messages.scrollHeight;
}

function setBusy(isBusy) {
  input.disabled = isBusy;
  form.querySelector("button").disabled = isBusy;
  form.setAttribute("aria-busy", String(isBusy));
  if (isBusy) {
    statusEl.textContent = "Working";
    statusEl.dataset.state = "working";
  } else if (statusEl.textContent === "Working" || statusEl.textContent === "Starting") {
    statusEl.textContent = "Ready";
    statusEl.dataset.state = "ready";
  }
}

async function startSession() {
  setBusy(true);
  const response = await fetch("/api/sessions", { method: "POST" });
  if (!response.ok) {
    throw new Error("Could not create session");
  }
  const data = await response.json();
  sessionId = data.session_id;
  observationsLink.href = `/api/observations/${sessionId}`;
  observationsLink.classList.remove("hidden");
  addMessage("agent", data.message);
  setBusy(false);
  input.focus();
}

async function sendMessage(message) {
  addMessage("user", message);
  setBusy(true);
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text);
  }
  const data = await response.json();
  addMessage("agent", data.message);
  if (data.download_url) {
    downloadLink.href = data.download_url;
    downloadLink.classList.remove("hidden");
  }
  statusEl.textContent = `${data.state} | ${data.question_count}/5`;
  statusEl.dataset.state = data.state;
  setBusy(false);
  input.focus();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  try {
    await sendMessage(message);
  } catch (error) {
    addMessage("agent", "Something went wrong. Please refresh and try again.");
    setBusy(false);
  }
});

sampleButton.addEventListener("click", () => {
  input.value = "Box 1 40000, Box 2 2400, Box 4 40000, Box 6 40000";
  input.focus();
});

startSession().catch(() => {
  addMessage("agent", "The app could not start a session. Please refresh.");
  setBusy(false);
});
