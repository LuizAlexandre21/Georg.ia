document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");
    const chatInput = document.getElementById("chat-input");
    const chatBox = document.getElementById("chat-box");
    const panelContainer = document.getElementById("panel-container");

    const toggleSidebar = () => {
        sidebar.classList.toggle("hidden");
        content.classList.toggle("expanded");
    };

    const sendMessage = async () => {
        const message = chatInput.value.trim();
        if (!message) return;

        panelContainer.style.display = "none";

        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message");
        messageElement.textContent = message;

        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
        chatInput.value = "";

        try {
            const response = await fetch("https://sua-api.com/mensagem", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ mensagem: message })
            });
            
            if (!response.ok) {
                console.error("Erro ao enviar mensagem", response.statusText);
            }
        } catch (error) {
            console.error("Erro ao conectar à API", error);
        }
    };

    chatInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    document.querySelector('.toggle-btn').addEventListener('click', toggleSidebar);
    document.querySelector('.chat-input button').addEventListener('click', sendMessage);
});
