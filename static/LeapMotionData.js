var ws;
var paused = false;
var pauseOnGesture = false;
var focusListener;
var blurListener;
// hand's palm position
var palmPosX = 10;
var palmPosY = 0;
var palmPosZ = 3;
var rotationValue = 0; //made this global variable for the sake of control bablyon object


// Support both the WebSocket and MozWebSocket objects
if ((typeof (WebSocket) == 'undefined') &&
    (typeof (MozWebSocket) != 'undefined')) {
    WebSocket = MozWebSocket;
}

// Create the socket with event handlers
function init() {
    // Create and open the socket
    ws = new WebSocket("ws://localhost:6437/v6.json");

    // On successful connection
    ws.onopen = function (event) {
        var enableMessage = JSON.stringify({enableGestures: true});
        ws.send(enableMessage); // Enable gestures
        ws.send(JSON.stringify({focused: true})); // claim focus

        focusListener = window.addEventListener('focus', function (e) {
            ws.send(JSON.stringify({focused: true})); // claim focus
        });

        blurListener = window.addEventListener('blur', function (e) {
            ws.send(JSON.stringify({focused: false})); // relinquish focus
        });

        // document.getElementById("main").style.visibility = "visible";
        // document.getElementById("connection").innerHTML = "WebSocket connection open!";
    };

    // On message received
    ws.onmessage = function (event) {
        if (!paused) {
            var obj = JSON.parse(event.data);
            if (obj !== undefined && obj.hands !== undefined && obj.hands[0] !== undefined) {
                //update palmPosX,Y,Z variable values from the JSON feed from the WebSocket
                var objRotation = obj.hands[0].armBasis[1];
                palmPosX = obj.hands[0].palmPosition[0]; // x-dimension of palm position
                palmPosY = obj.hands[0].palmPosition[1]; // y-dimension of palm position
                palmPosZ = obj.hands[0].palmPosition[2]; // z-dimension of palm position

                console.log("PalmX: ", palmPosX);
                console.log("PalmY: ", palmPosY);
                console.log("PalmZ: ", palmPosZ);
            }
        }
    };

    // On socket close
    ws.onclose = function (event) {
        ws = null;
        window.removeListener("focus", focusListener);
        window.removeListener("blur", blurListener);
        document.getElementById("main").style.visibility = "hidden";
        document.getElementById("connection").innerHTML = "WebSocket connection closed";
    }

    // On socket error
    ws.onerror = function (event) {
        alert("Received error");
    };
}

function togglePause() {
    paused = !paused;

    if (paused) {
        document.getElementById("pause").innerText = "Resume";
    } else {
        document.getElementById("pause").innerText = "Pause";
    }
}

function pauseForGestures() {
    if (document.getElementById("pauseOnGesture").checked) {
        pauseOnGesture = true;
    } else {
        pauseOnGesture = false;
    }
}