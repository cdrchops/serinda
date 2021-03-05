//determine the devices on the system
navigator.mediaDevices.enumerateDevices()
.then(function(devices) {
    devices.forEach(function(device) {
        console.log(device.kind + ": " + device.label + " id = " + device.deviceId);
    });
})
.catch(function(err) {
    console.log(err.name + ": " + err.message);
});