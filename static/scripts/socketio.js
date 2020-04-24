document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    let room="General";
    joinRoom("General");


    socket.on('message', data => {

        // Display current message
        if (data.msg) {
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br')
            // Display user's own message
            if (data.username == username) {
                    p.setAttribute("class", "my-msg");

                    // Username
                    span_username.setAttribute("class", "my-username");
                    span_username.innerText = data.username;

                    // Timestamp
                    span_timestamp.setAttribute("class", "timestamp");
                    span_timestamp.innerText = data.time_stamp;

                    // HTML to append
                    p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

                    //Append
                    document.querySelector('#message-section').append(p);
            }
            // Display other users' messages
            else if (typeof data.username !== 'undefined') {
                p.setAttribute("class", "others-msg");

                // Username
                span_username.setAttribute("class", "other-username");
                span_username.innerText = data.username;

                // Timestamp
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = data.time_stamp;

                // HTML to append
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

                //Append
                document.querySelector('#message-section').append(p);
            }
            // Display system message
            else {
                printSystemMessage(data.msg);
            }


        }
        scrollDownChatWindow();
    });

    document.querySelector('#send-message').onclick = () => {
        socket.send({'msg': document.querySelector('#user-message').value, 'username': username, 'room': room });
        document.querySelector('#user-message').value = '';
    }

    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let nRoom = p.innerHTML;
            if(nRoom == room){
                msg = `You are already in ${room} room.`
                printSystemMessage(msg);
            }
            else {
                leaveRoom(room);
                joinRoom(nRoom);
                room = nRoom;
            }
        }
    })

    document.querySelector('#logout-btn').onclick = () => {
        leaveRoom(room);
    }

    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});

        document.querySelectorAll('.select-room').forEach(p => {
            p.style.removeProperty("background-color");
            p.style.color="#3e71d6";
        });
    }

    function joinRoom(room){
        socket.emit('join', {'username': username, 'room': room});

        document.querySelector('#' + CSS.escape(room)).style.color = "#f0f1f5";
        document.querySelector('#' + CSS.escape(room)).style.backgroundColor = "#081540";

        document.querySelector('#message-section').innerHTML = '';
        document.querySelector('#user-message').focus();
    }

    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }


    function printSystemMessage(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#message-section').append(p);
        scrollDownChatWindow();

        // Autofocus on text box
        document.querySelector("#user-message").focus();
    }
})