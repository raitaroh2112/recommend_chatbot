document.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + window.location.hostname + ":" + window.location.port);

    const userIconUrl = '/static/images/user-icon.png'; 

    const getBotIconUrl = (emotion) => {
        switch (emotion) {
            case 'joy':
                return '/static/images/joy.png';
            case 'sadness':
                return '/static/images/sadness.png';
            case 'anticipation':
                return '/static/images/anticipation.png';
            case 'surprise':
                return '/static/images/surprise.png';
            case 'anger':
                return '/static/images/anger.png';
            case 'fear':
                return '/static/images/fear.png';
            case 'disgust':
                return '/static/images/disgust.png';
            case 'trust':
                return '/static/images/trust.png';
            default:
                return '/static/images/neutral.png';
        }
    };

    socket.on("bot_response", function (data) {
        const messageBox = document.getElementById("messages");
        const botIconUrl = getBotIconUrl(data.emotion); 

        messageBox.innerHTML += `
            <div class="chat-message bot">
                <img src="${botIconUrl}" alt="Bot Icon" class="icon">
                <div>
                    <div class="message-content bot">
                        <p>${data.response_message}</p>
                    </div>
                    <div class="message-time">${data.time}</div>
                </div>
            </div>
        `;
        messageBox.scrollTop = messageBox.scrollHeight;
    });

    document.getElementById("send-button").addEventListener("click", function () {
        const userMessage = document.getElementById("user-message").value;
        const messageBox = document.getElementById("messages");
        const submitTime = new Date().toLocaleString('ja-JP', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });

        if (userMessage.trim() !== "") {
            messageBox.innerHTML += `
                <div class="chat-message user">
                    <div>
                        <div class="message-content user">
                            <p>${userMessage}</p>
                        </div>
                        <div class="message-time">${submitTime}</div>
                    </div>
                    <img src="${userIconUrl}" alt="User Icon" class="icon">
                </div>
            `;
            messageBox.scrollTop = messageBox.scrollHeight;

            socket.emit("send_message", { message: userMessage });
            document.getElementById("user-message").value = "";
        }
    });
});
