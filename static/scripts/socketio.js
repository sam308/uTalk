document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    let room="General";
    joinRoom("General");

    socket.on('message', data => {
        const p = document.createElement('p');
        const br = document.createElement('br');
        const span_uname = document.createElement('span');
        const span_time = document.createElement('span');

        if(data.username) {
            span_uname.innerHTML = data.username;
            span_time.innerHTML = data.time_stamp; 
            p.innerHTML = span_uname.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time.outerHTML;
            document.querySelector('#message-section').append(p);
        }
        else {
            printSystemMessage(data.msg);
        }
        
    })

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

    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});
    }

    function joinRoom(room){
        socket.emit('join', {'username': username, 'room': room});

        document.querySelector('#message-section').innerHTML = '';
        document.querySelector('#user-message').focus();
    }

    function printSystemMessage(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#message-section').append(p);
    }
})