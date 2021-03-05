//Babylon main script code
window.addEventListener('DOMContentLoaded', function () {
    // All the following code is entered here.
    var canvas = document.getElementById('renderCanvas');
    var engine = new BABYLON.Engine(canvas, true);

    var createScene = function () {
        // Create a basic BJS Scene object.
        var scene = new BABYLON.Scene(engine);

        // Create a FreeCamera, and set its position to (x:0, y:5, z:-10).
        var camera = new BABYLON.FreeCamera('camera', new BABYLON.Vector3(0, 5, -10), scene);

        // Target the camera to scene origin.
        camera.setTarget(BABYLON.Vector3.Zero());

        // Attach the camera to the canvas.
        camera.attachControl(canvas, false);

        // Create a basic light, aiming 0,1,0 - meaning, to the sky.
        var light = new BABYLON.HemisphericLight('light1', new BABYLON.Vector3(0, 1, 0), scene);

        // Create a built-in "sphere" shape.
        var sphere = BABYLON.MeshBuilder.CreateSphere('sphere', {segments: 16, diameter: 2}, scene);

        // Initially set X, Y, Z position of Sphere
        sphere.position.x = palmPosX;
        sphere.position.y = palmPosY;
        sphere.position.z = -palmPosZ;

        // Create a built-in "ground" shape.
        // var ground = BABYLON.MeshBuilder.CreateGround('ground1', {height:6, width:6, subdivisions: 2}, scene);

        //adding plane for collision
        var plane = BABYLON.MeshBuilder.CreatePlane("plane", {width: 5, height: 5}, scene);

        engine.runRenderLoop(function () {
            // Update X, Y, Z position of Sphere
            sphere.position.x = palmPosY / 100;
            sphere.position.y = palmPosY / 100;
            sphere.position.z = -palmPosZ / 100;
            //create methods for updating variables and call methods here!!
            scene.render();
        });

        // Return the created scene.
        return scene;
    }

    var scene = createScene();

    window.addEventListener('resize', function () {
        engine.resize();
    });
});