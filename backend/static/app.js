async function sendMessage(e) {
  e.preventDefault();

  const input = document.getElementById("userInput");
  const messages = document.getElementById("messages");
  const sendBtn = document.querySelector(".send-btn");

  const text = input.value.trim();
  if (!text) return;

  // USER MESSAGE
  const userMsg = document.createElement("div");
  userMsg.className = "message user";
  userMsg.textContent = text;
  messages.appendChild(userMsg);

  input.value = "";
  input.disabled = true;
  sendBtn.textContent = "⏹";

  messages.scrollTop = messages.scrollHeight;

  // BOT PLACEHOLDER
  const botMsg = document.createElement("div");
  botMsg.className = "message bot";
  botMsg.textContent = "Yazıyor...";
  messages.appendChild(botMsg);

  try {
    const res = await fetch("/ask",{
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    botMsg.textContent = data.answer || "Cevap alınamadı.";
  } catch (err) {
    botMsg.textContent = "Bir hata oluştu.";
  }

  input.disabled = false;
  sendBtn.textContent = "➤";
  input.focus();

  messages.scrollTop = messages.scrollHeight;
}
