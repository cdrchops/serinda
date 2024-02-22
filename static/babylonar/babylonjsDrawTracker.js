function drawTracker(scene, canvas, camera, scale, plane, tracker) {
    // Run template tracking
    var norm = BABYLON.Vector2.Zero();
    var prtX;
    var ptrY;
    var tracking = false;
    var trackingPromise = Promise.resolve();
    scene.onPointerDown = () => {
        norm.x = 2 * scene.pointerX / canvas.width - 1;
        norm.y = 2 * scene.pointerY / canvas.height - 1;

        ratio = canvas.width / canvas.height;
        ptrX = camera.position.x + ratio * norm.x * scale / 2;
        ptrY = camera.position.y - norm.y * scale / 2;

        texSize = plane.material.albedoTexture.getSize();
        ptrX *= texSize.height;
        ptrY *= -texSize.height;

        ptrX += (texSize.width / 2);
        ptrY += (texSize.height / 2);

        if (tracking) {
            trackingPromise = trackingPromise.then(() => tracker.stopTrackingAsync());
        }

        trackingPromise.then(() => {
            tracker.startTracking(ptrX, ptrY);
            tracking = true;
        });
    }
}