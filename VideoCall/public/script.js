const socket = io('/')
const videoGrid = document.getElementById('video-grid')
const messages = document.getElementById('wait-message')
const myPeer = new Peer(undefined, {
    host: '/',
    port: '3001',
})
var peerPresent = false
const myVideo = document.createElement('video')
myVideo.muted = true
const peers = {}
navigator.mediaDevices.getUserMedia({
    video: true,
    audio: true
}).then(stream => {
    addVideoStream(myVideo, stream)

    let myPromise = new Promise(function(myResolve, myReject) {
        setTimeout(function() { myResolve("Todos los vendedores se encuentran ocupados"); }, 5000);
    });

    myPromise.then(function(value) {
        document.getElementById("wait-message").innerHTML = value;
    }).then(() => {
        if (peerPresent) {
            document.getElementById("wait-message").innerHTML = "";
        }
    })


    myPeer.on('call', call => {
        peerPresent = true
        document.getElementById("wait-message").innerHTML = ""
        call.answer(stream)
        const video = document.createElement('video')
        call.on('stream', userVideoStream => {
            addVideoStream(video, userVideoStream)
        })
    })

    socket.on('user-connected', userId => {
        connectToNewUser(userId, stream)
    })
})

socket.on('user-disconnected', userId => {
    console.log(userId)
})

myPeer.on('open', id => {
    socket.emit('join-room', ROOM_ID, id)
})

socket.on('user-connected', userId => {
    if (peers[userId]) peers[userId].close()
})

function connectToNewUser(userId, stream) {
    const call = myPeer.call(userId, stream)
    const video = document.createElement('video')
    call.on('stream', userVideoStream => {
        peerPresent = true
        document.getElementById("wait-message").innerHTML = "";
        addVideoStream(video, userVideoStream)
    })
    call.on('close', () => {
        video.remove()
    })

    peers[userId] = call
}

function addVideoStream(video, stream) {
    video.srcObject = stream
    video.addEventListener('loadedmetadata', () => {
        video.play()
    })
    videoGrid.append(video)
    
}
