//Socket.IO Connection
const socket = io();
const img = document.getElementById('video')
const fullscreenBtn = document.getElementById('fullscreen-btn')

//Receive frames
socket.on('video_frame', (data) => {
    img.src = 'data:image/jpeg;base64,' + data;
});

//Connection debug messages :D
socket.on('connect', () => console.log('Connected'))
socket.on('disconnect', () => console.log('Disonnected'))
socket.on('connect_error', () => console.log('Error', err))

//Fullscreen button
fullscreenBtn.addEventListener('click', () => {
    if (img.requestFullscreen) {
        img.requestFullscreen();
    }
});

