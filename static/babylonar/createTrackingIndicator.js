function createTrackingIndicator(scene, tracker, plane) {
    // Create the tracking indicator
    var indicator = BABYLON.MeshBuilder.CreatePlane("indicator", {}, scene);
    indicator.position.z = -0.1;
    indicator.scaling.x = 0.1;
    indicator.scaling.y = 0.1;
    var indicatorMaterial = new BABYLON.PBRMaterial("indicatorMaterial", scene);
    indicatorMaterial.unlit = true;
    indicatorMaterial.transparencyMode = 3;
    var indicatorTexture = new BABYLON.Texture("/static/babylonar/examples/image-template-tracker-resources/texture.png", scene, true, false);
    indicatorTexture.onLoadObservable.add(() => {
        indicatorTexture.vScale = -1;
        indicatorMaterial.albedoTexture = indicatorTexture;

        indicator.position.x = 1.1 * indicator.scaling.x;
        indicator.scaling.x *= 2;
    });
    indicator.material = indicatorMaterial;

    var indicatorParent = new BABYLON.TransformNode("indicatorParent", scene);
    indicator.parent = indicatorParent;
    indicatorParent.setEnabled(false);

    var texSize;
    tracker.onTrackingUpdatedObservable.add((point) => {
        if (point === null) {
            indicatorParent.setEnabled(false);
        } else {
            indicatorParent.setEnabled(true);

            indicatorParent.position.x = point.x;
            indicatorParent.position.y = point.y;

            texSize = plane.material.albedoTexture.getSize();
            indicatorParent.position.x -= (texSize.width / 2);
            indicatorParent.position.y -= (texSize.height / 2);

            indicatorParent.position.x /= texSize.height;
            indicatorParent.position.y /= -texSize.height;
        }
    });

    return tracker;
}