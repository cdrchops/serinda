"use strict";
// Copyright 2023 The MediaPipe Authors.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//      http://www.apache.org/licenses/LICENSE-2.0
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// @ts-ignore - Allow CDN ESM import in TS for browser-only demo
var tasks_vision_0_10_3_1 = require("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3");
var demosSection = document.getElementById("demos");
var gestureRecognizer;
var runningMode = "IMAGE";
var enableWebcamButton;
var webcamRunning = false;
var videoHeight = "360px";
var videoWidth = "480px";
// Before we can use HandLandmarker class we must wait for it to finish
// loading. Machine Learning models can be large and take a moment to
// get everything needed to run.
var createGestureRecognizer = function () { return __awaiter(void 0, void 0, void 0, function () {
    var vision;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, tasks_vision_0_10_3_1.FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm")];
            case 1:
                vision = _a.sent();
                return [4 /*yield*/, tasks_vision_0_10_3_1.GestureRecognizer.createFromOptions(vision, {
                        baseOptions: {
                            modelAssetPath: "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
                            delegate: "GPU"
                        },
                        runningMode: runningMode
                    })];
            case 2:
                gestureRecognizer = _a.sent();
                if (demosSection) {
                    demosSection.classList.remove("invisible");
                }
                return [2 /*return*/];
        }
    });
}); };
createGestureRecognizer();
/********************************************************************
// Demo 1: Detect hand gestures in images
********************************************************************/
var imageContainers = document.getElementsByClassName("detectOnClick");
for (var i = 0; i < imageContainers.length; i++) {
    imageContainers[i].children[0].addEventListener("click", handleClick);
}
function handleClick(event) {
    return __awaiter(this, void 0, void 0, function () {
        var target, parent, allCanvas, i, n, results, p, categoryName, categoryScore, handedness, canvas, canvasCtx_1, drawingUtils, _i, _a, landmarks;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    if (!gestureRecognizer) {
                        alert("Please wait for gestureRecognizer to load");
                        return [2 /*return*/];
                    }
                    if (!(runningMode === "VIDEO")) return [3 /*break*/, 2];
                    runningMode = "IMAGE";
                    return [4 /*yield*/, gestureRecognizer.setOptions({ runningMode: "IMAGE" })];
                case 1:
                    _b.sent();
                    _b.label = 2;
                case 2:
                    target = event.target;
                    parent = target && target.parentNode;
                    allCanvas = parent.getElementsByClassName("canvas");
                    for (i = allCanvas.length - 1; i >= 0; i--) {
                        n = allCanvas[i];
                        n.parentNode.removeChild(n);
                    }
                    results = gestureRecognizer.recognize(target);
                    // View results in the console to see their format
                    console.log(results);
                    if (results && results.gestures && results.gestures.length > 0) {
                        p = parent.childNodes[3];
                        p.setAttribute("class", "info");
                        categoryName = results.gestures[0][0].categoryName;
                        categoryScore = parseFloat(results.gestures[0][0].score * 100).toFixed(2);
                        handedness = results.handednesses[0][0].displayName;
                        p.innerText = "GestureRecognizer: ".concat(categoryName, "\n Confidence: ").concat(categoryScore, "%\n Handedness: ").concat(handedness);
                        p.style.cssText =
                            "left: 0px;" +
                                "top: " +
                                target.height +
                                "px; " +
                                "width: " +
                                (target.width - 10) +
                                "px;";
                        canvas = document.createElement("canvas");
                        canvas.setAttribute("class", "canvas");
                        canvas.setAttribute("width", target.naturalWidth + "px");
                        canvas.setAttribute("height", target.naturalHeight + "px");
                        canvas.style.cssText =
                            "left: 0px;" +
                                "top: 0px;" +
                                "width: " +
                                target.width +
                                "px;" +
                                "height: " +
                                target.height +
                                "px;";
                        parent.appendChild(canvas);
                        canvasCtx_1 = canvas.getContext("2d");
                        drawingUtils = new tasks_vision_0_10_3_1.DrawingUtils(canvasCtx_1);
                        for (_i = 0, _a = results.landmarks; _i < _a.length; _i++) {
                            landmarks = _a[_i];
                            drawingUtils.drawConnectors(landmarks, tasks_vision_0_10_3_1.GestureRecognizer.HAND_CONNECTIONS, {
                                color: "#00FF00",
                                lineWidth: 5
                            });
                            drawingUtils.drawLandmarks(landmarks, {
                                color: "#FF0000",
                                lineWidth: 1
                            });
                        }
                    }
                    return [2 /*return*/];
            }
        });
    });
}
/********************************************************************
// Demo 2: Continuously grab image from webcam stream and detect it.
********************************************************************/
var video = document.getElementById("webcam");
var canvasElement = document.getElementById("output_canvas");
var canvasCtx = canvasElement.getContext("2d");
var gestureOutput = document.getElementById("gesture_output");
// Check if webcam access is supported.
function hasGetUserMedia() {
    return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}
// If webcam supported, add event listener to button for when user
// wants to activate it.
if (hasGetUserMedia()) {
    enableWebcamButton = document.getElementById("webcamButton");
    if (enableWebcamButton) {
        enableWebcamButton.addEventListener("click", enableCam);
    }
}
else {
    console.warn("getUserMedia() is not supported by your browser");
}
// Enable the live webcam view and start detection.
function enableCam(event) {
    if (!gestureRecognizer) {
        alert("Please wait for gestureRecognizer to load");
        return;
    }
    if (webcamRunning === true) {
        webcamRunning = false;
        enableWebcamButton.innerText = "ENABLE PREDICTIONS";
    }
    else {
        webcamRunning = true;
        enableWebcamButton.innerText = "DISABLE PREDICTIONS";
    }
    // getUsermedia parameters.
    var constraints = {
        video: true
    };
    // Activate the webcam stream.
    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        video.srcObject = stream;
        video.addEventListener("loadeddata", predictWebcam);
    });
}
var lastVideoTime = -1;
var results = undefined;
function predictWebcam() {
    return __awaiter(this, void 0, void 0, function () {
        var webcamElement, nowInMs, drawingUtils, _i, _a, landmarks, categoryName, categoryScore, handedness;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    webcamElement = document.getElementById("webcam");
                    if (!(runningMode === "IMAGE")) return [3 /*break*/, 2];
                    runningMode = "VIDEO";
                    return [4 /*yield*/, gestureRecognizer.setOptions({ runningMode: "VIDEO" })];
                case 1:
                    _b.sent();
                    _b.label = 2;
                case 2:
                    nowInMs = Date.now();
                    if (video.currentTime !== lastVideoTime) {
                        lastVideoTime = video.currentTime;
                        results = gestureRecognizer.recognizeForVideo(video, nowInMs);
                    }
                    canvasCtx.save();
                    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
                    drawingUtils = new tasks_vision_0_10_3_1.DrawingUtils(canvasCtx);
                    canvasElement.style.height = videoHeight;
                    webcamElement.style.height = videoHeight;
                    canvasElement.style.width = videoWidth;
                    webcamElement.style.width = videoWidth;
                    if (results === null || results === void 0 ? void 0 : results.landmarks) {
                        for (_i = 0, _a = results.landmarks; _i < _a.length; _i++) {
                            landmarks = _a[_i];
                            drawingUtils.drawConnectors(landmarks, tasks_vision_0_10_3_1.GestureRecognizer.HAND_CONNECTIONS, {
                                color: "#00FF00",
                                lineWidth: 5
                            });
                            drawingUtils.drawLandmarks(landmarks, {
                                color: "#FF0000",
                                lineWidth: 2
                            });
                        }
                    }
                    canvasCtx.restore();
                    if (results && results.gestures && results.gestures.length > 0) {
                        gestureOutput.style.display = "block";
                        gestureOutput.style.width = videoWidth;
                        categoryName = results.gestures[0][0].categoryName;
                        categoryScore = parseFloat(results.gestures[0][0].score * 100).toFixed(2);
                        handedness = results.handednesses[0][0].displayName;
                        gestureOutput.innerText = "GestureRecognizer: ".concat(categoryName, "\n Confidence: ").concat(categoryScore, " %\n Handedness: ").concat(handedness);
                    }
                    else {
                        gestureOutput.style.display = "none";
                    }
                    // Call this function again to keep predicting when the browser is ready.
                    if (webcamRunning === true) {
                        window.requestAnimationFrame(predictWebcam);
                    }
                    return [2 /*return*/];
            }
        });
    });
}
