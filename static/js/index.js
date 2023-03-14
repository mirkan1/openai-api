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
    var newDiv = document.createElement("div");
    newDiv.classList.add("message");
    newDiv.classList.add(role);
    newDiv.innerHTML = role + ">>" + message;
    chat.appendChild(newDiv);
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
        newDiv = document.createElement("div");
        newDiv.classList.add("message");
        newDiv.classList.add("chatbot_response");
        newDiv.innerHTML = chatbot_response;
        chat.appendChild(newDiv);
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
