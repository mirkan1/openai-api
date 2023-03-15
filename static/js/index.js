function startConversation() {
    const message = document.getElementById("message").value;
    const role = document.getElementById("role").value;
    axios({
        method: 'POST',
        url:"/api/start_conversation",
        data: {
            message: message,
            role: role
        },
        responseType: 'json',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
        }
    }).then((response) => {
        const chatbot_response = response.data.response;
        const id = response.data.id;
        window.location.pathname = "/chat/" + id;
    }).catch((error) => {
        console.error(error);
    })
}

function sendMessage() {
    const message = document.getElementById("message").value;
    const role = document.getElementById("role").value;
    const chat = document.querySelector(".chat");
    const newMessageDiv = document.createElement("div");
    newMessageDiv.classList.add("message");
    newMessageDiv.innerHTML = markdownToHtml(message)
    const newRoleDiv = document.createElement("div");
    newRoleDiv.classList.add("role");
    newRoleDiv.classList.add(role);
    newRoleDiv.innerHTML = role
    chat.appendChild(newRoleDiv);
    chat.appendChild(newMessageDiv);
    waitingAnimation("start");
    axios({
        method: 'POST',
        url:"/api/add_message",
        data: {
            id:  chat.id,
            message: message,
            role: role,
        },
        responseType: 'json',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
        }  
    }).then((response) => {
        const chatbot_response = response.data;
        //
        const newMessageDiv = document.createElement("div");
        newMessageDiv.classList.add("message");
        newMessageDiv.innerHTML = markdownToHtml(chatbot_response)
        const newRoleDiv = document.createElement("div");
        newRoleDiv.classList.add("role");
        newRoleDiv.classList.add("bot");
        newRoleDiv.innerHTML = "bot"
        chat.appendChild(newRoleDiv);
        chat.appendChild(newMessageDiv);
    }).catch((error) => {
        console.error(error);
    });
}

function deleteChat(id) {
    axios({
        method: 'POST',
        url:"/api/delete_chat",
        data: {
            id: id,
        },
        responseType: 'json',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
        }  
    }).then((response) => {
        const status = response.data.status;
        if (status == "success") {
            window.location.pathname = "/";
        } else {
            alert("Error deleting chat");
        }
    }).catch((error) => {
        console.error(error);
    });
}
function waitingAnimation(state) {
    if (state="start") {
        console.log("TODO started animation") 
    } else {
        console.log("TODO stopped animation") 
    }
}
var converter;
function markdownToHtml(text) {
    return converter.makeHtml(text);
}

$( document ).ready(function() {
    converter = new showdown.Converter();
    const messages = document.querySelectorAll(".message");
    messages.forEach((message) => {
        message.innerHTML = markdownToHtml(message.innerHTML.trim());
    });
});

const messageSendButton = document.getElementById("send-message-button");

messageSendButton.addEventListener("keypress", function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});