var canvas = document.getElementById("renderCanvas");

var engine = null;
var scene = null;
var sceneToRender = null;
var createDefaultEngine = function() { return new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true,  disableWebGL2Support: false}); };

let hudElements = new Map();

var AMGR = null;
var DRAG = null;
var camera = null;
var OBJ = {
        colors              : {},
        materials           : {},
        colors				: {},
        colorDiffuse		: null,
        colorSpecular		: null,
        itemMove            : null,
        items               : [],
        actions             : {}
    }

var
    x =
    y =
    z = 0, matBox, cmd;

var createScene = function () {
    scene = createCerebroScene();

    // https://www.babylonjs-playground.com/#ER6T4W#58
    DRAGXY = new BABYLON.PointerDragBehavior({dragPlaneNormal: new BABYLON.Vector3(0, -1, 0)});
	DRAGXY.updateDragPlane = false;
	DRAGXY.useObjectOrienationForDragging = false;

    AMGR = new BABYLON.ActionManager(scene);

    _init();

    setTimeout(function() {
        engine.stopRenderLoop();

        engine.runRenderLoop(function () {
            scene.render();
        });
    }, 500);

    return scene;
};

function removeOCVData(label) {
    if (hudElements.has(label)) {
        var tmpItem = hudElements.get(label);
        tmpItem.removeChild(tmpItem.__bottom);
        tmpItem.__bottom.dispose();
        scene.removeMesh(hudElements.get(label));
        hudElements.delete(label);
    }
}

function setOCVData(data, label) {
    //TODO: this is the part to work on
    // - determine what is detected and then adding the item to a map
    // - if the item is not detected then the panel is removed
    // - if multiple items are detected then they'll all be added to the map

    if (hudElements.has(label)) {
        var element = hudElements.get(label);
        element.position.x = data.x/8;// - data.x;
        element.position.y = data.y/8;// - data.y;
        element.position.z = data.width;
    } else {
        var tmpElement = createFaceHUD(data, label);
        hudElements.set(label, tmpElement);
    }
}

function _init() {
	OBJ.colorDiffuse						= new BABYLON.Color3(0.1, 0.1, 0.1);
	OBJ.colorSpecular						= new BABYLON.Color3(0.1, 0.1, 0.1);

	OBJ.colors.red							= new BABYLON.Color3(0.8, 0.2, 0.2);
	OBJ.colors.green						= new BABYLON.Color3(0.1, 0.6, 0.1);
	OBJ.colors.blue							= new BABYLON.Color3(0.1, 0.2, 0.8);
	OBJ.colors.orange						= new BABYLON.Color3(0.8, 0.5, 0.1);
	OBJ.colors.purple						= new BABYLON.Color3(0.8, 0.2, 0.8);

	OBJ.actions.pickUp						= new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickUpTrigger, _pick_up);
	OBJ.actions.pickDown					= new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickDownTrigger, _pick_down);

	for (var i in OBJ.actions) {
        AMGR.registerAction(OBJ.actions[i]);
    }
}

function _pick_down(a) {
    camera.detachControl(canvas, true)
	if (a.sourceEvent.button == 0) {
		OBJ.itemMove = a.source;
		DRAGXY.attach(OBJ.itemMove);
	}
}

function _pick_up(a) {
    camera.attachControl(canvas, true)
    //debugger
	if (a.source == OBJ.itemMove) {
		DRAGXY.detach(OBJ.itemMove);
        DRAGXY.releaseDrag();
		OBJ.itemMove = null;
	}
}

function createCerebroScene() {
    var scene = new BABYLON.Scene(engine);
    scene.clearColor = BABYLON.Color3.Black();
    // camera = new BABYLON.ArcRotateCamera("Camera", 5.6, 1.4, 80, BABYLON.Vector3.Zero(), scene)
    camera = new BABYLON.ArcRotateCamera("cam", -Math.PI / 2, Math.PI / 2, 10, BABYLON.Vector3.Zero(), scene);
    // camera = new BABYLON.UniversalCamera("UniversalCamera", new BABYLON.Vector3(0, 0, -10), scene);
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

    // createPanel(manager, anchor, panel1Location, panelCount, "panel1", input, showInput, panelMargin);
    // createPanel(manager, anchor, panel2Location, panelCount, "panel2", input, showInput, panelMargin);
    //todo: fix the third panel so the last 3 columns aren't displayed - ie make each row only 7 wide.
    // createPanel(manager, anchor, panel3Location, panelCount, "panel3", input, showInput, panelMargin);

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

function createFaceHUD(data, label) {
    matBox = new BABYLON.StandardMaterial('matBox'+label, scene);

    z = 20;

    matBox.diffuseColor     = OBJ.colorDiffuse;
    matBox.specularColor    = OBJ.colorSpecular;
    matBox.emissiveColor    = new BABYLON.Color3(.3, .3, .3);
    matBox.alpha            = .6;

    cmd = [
            "\uf044",
            "\uf1e3"
        ];

    // Main item (BLUE BOX)
    var m = BABYLON.MeshBuilder.CreatePlane(
        label,
        {
            width: 12,
            height: 5
        },
        scene
    );

    m.position.x = data.x - data.x;
    m.position.y = data.y - data.y;
    m.position.z = data.width;
    m.isPickable = true;
    m.billboardMode = BABYLON.Mesh.BILLBOARDMODE_ALL;

    // Main item's material (BLUE)
    var mat = new BABYLON.StandardMaterial('mat-' + label, scene);
    mat.diffuseColor = OBJ.colorDiffuse;
    mat.specularColor = OBJ.colorSpecular;
    mat.emissiveColor = new BABYLON.Color3().copyFrom(OBJ.colors.blue);
    m.material = mat;

    m.hoverCursor = 'pointer';
    m.actionManager = AMGR;

    m.__DTX = new BABYLON.DynamicTexture('DTX-' + label, {width: 12 * 64, height: 5 * 64}, scene);
    m.material.emissiveTexture = m.__DTX;
    m.__DTX.drawText(label, null, null, 'bold 96px Arial', 'white', null, true, true);

    // Item's control box
    m.__bottom = BABYLON.MeshBuilder.CreatePlane(m.id + '-CTL-' + label, {width: 12, height: 4}, scene);
    m.__bottom.parent = m;
    m.__bottom.position.y = -4.5;
    m.__bottom.material = matBox;

    // Controls
    /*for (var k in cmd) {
        var b = BABYLON.MeshBuilder.CreatePlane(m.id + '-CMD-' + k, {size: 4}, scene);
        b.parent = m.__bottom;
        b.position.x = 4 - k * 4;
        b.position.z = -.1;
        b.hoverCursor = 'pointer';

        b.material = new BABYLON.StandardMaterial(m.id + '-MAT-BTN-' + k, scene)
        b.material.diffuseColor = OBJ.colorDiffuse;
        b.material.specularColor = OBJ.colorSpecular;
        b.material.emissiveColor = new BABYLON.Color3(.3, .3, .3);
        b.material.alpha = .6;

        b.material.emissiveTexture = new BABYLON.DynamicTexture(m.id + '-DTX-' + k + '-dtx', {
            width: 4 * 64,
            height: 4 * 64
        }, scene);

        b.material.emissiveTexture.drawText(cmd[k], null, null, 'normal 168px FontAwesome', 'white', null, true, true);
    }*/

    return m;
}

