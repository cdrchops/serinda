var canvas = document.getElementById("renderCanvas");

var engine = null;
var scene = null;
var sceneToRender = null;
var createDefaultEngine = function() { return new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true,  disableWebGL2Support: false}); };

var createScene = function () {
    var scene = createCerebroScene();

    setTimeout(function() {
        engine.stopRenderLoop();

        engine.runRenderLoop(function () {
            scene.render();
        });
    }, 500);

    return scene;
};

function createCerebroScene() {
    var scene = new BABYLON.Scene(engine);
    scene.clearColor = BABYLON.Color3.Black();
    // var camera = new BABYLON.ArcRotateCamera("Camera", 5.6, 1.4, 80, BABYLON.Vector3.Zero(), scene)
    var camera = new BABYLON.ArcRotateCamera("cam", -Math.PI / 2, Math.PI / 2, 10, BABYLON.Vector3.Zero());
    var anchor = new BABYLON.TransformNode("");


    camera.wheelDeltaPercentage = 0.1;
    camera.setTarget(BABYLON.Vector3.Zero());
    camera.attachControl(canvas, true);
    var light = new BABYLON.HemisphericLight("hemi", new BABYLON.Vector3(0, 1, 0), scene)

    // Create the 3D UI manager
    var manager = new BABYLON.GUI.GUI3DManager(scene);

    var showInput = false;
    var smallerMargin = true;
    var panelMargin = 0.2;
    var panelCount = 60;
    var panel1Location = 100;
    var panel2Location = 260;
    var panel3Location = 279.97;

    if (smallerMargin) {
        panelMargin = 0.06;
        panelCount = 30;
        panel2Location = 259.5;
    }

    var input = "";

    createPanel(manager, anchor, panel1Location, panelCount, "panel1", input, showInput, panelMargin);
    createPanel(manager, anchor, panel2Location, panelCount, "panel2", input, showInput, panelMargin);
    //todo: fix the third panel so the last 3 columns aren't displayed - ie make each row only 7 wide.
    createPanel(manager, anchor, panel3Location, panelCount, "panel3", input, showInput, panelMargin);

    var button = document.createElement("button");
    button.style.top = "100px";
    button.style.right = "30px";
    button.textContent = "click";
    button.style.width = "100px"
    button.style.height = "20px"

    button.setAttribute = ("id", "but");
    button.style.position = "absolute";
	button.style.color = "black";

    document.body.appendChild(button);

    button.addEventListener("click", () => {
        // alert('yeah baby yeah');
        camera.position = new BABYLON.Vector3(camera.position.x, camera.position.y, camera.position.z + 10);
        // alert(camera.position);
    })

    return scene;
}

//from the arc button panel example
function createPanel(manager, anchor, rotation, panelCount, panelName, input, showInput, panelMargin) {
    var panel = new BABYLON.GUI.SpherePanel();
    panel.margin = panelMargin;

    manager.addControl(panel);
    panel.linkToTransformNode(anchor);
    panel.position.z = 1.5;

    // Adapted from here: https://github.com/BabylonJS/Babylon.js/blob/master/gui/src/3D/controls/spherePanel.ts#L60-L69
    //https://www.babylonjs-playground.com/#HB4C01#377
    panel._sphericalMapping = function (source) {
        let newPos = new BABYLON.Vector3(0, 0, this._radius);

        let xAngle = (source.y / this._radius);
        let yAngle = (source.x / this._radius);

        BABYLON.Matrix.RotationYawPitchRollToRef(yAngle, xAngle, 0, BABYLON.TmpVectors.Matrix[0]);

        return BABYLON.Vector3.TransformNormal(newPos, BABYLON.TmpVectors.Matrix[0]);
    };

    // Let's add some buttons!
    var addButton = function(trueFalse) {
        var button = new BABYLON.GUI.HolographicButton("orientation");
        panel.addControl(button);

        button.text = panelName + panel.children.length;

        if (trueFalse) {
            button.onPointerUpObservable.add(function() {
                showInput = !showInput;
            });
        }
    }

    panel.blockLayout = true;
    for (var index = 0; index < panelCount; index++) {
        // if (panelName === "panel3") {
            addButton(false);
        // } else {
            // if (index === 0) {
            //     addButton(true);
            // } else {
                addButton(false);
            // }
        // }
    }

    panel.blockLayout = false;
    panel.node.rotation.y += rotation;
}
