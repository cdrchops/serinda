// Hand and gesture handling extracted from main2.html
// This module expects the following globals to already exist in the page:
// - video, scene, BABYLON
// - mapToScene(x, y), distance(p1, p2), distanceXY(x1,y1,x2,y2)
// - getNearestObject(cursorVec3, maxDist)
// - objects (Map), activeObjectId (let), currentGesture (let), isGrabbing (let), wasGrabbing (let)
// - videoWidth, videoHeight
// - MediaPipe scripts loaded: Camera, Hands

(function(){
  function ensureDeps() {
    const missing = [];
    if (typeof BABYLON === 'undefined') missing.push('BABYLON');
    if (typeof Hands === 'undefined') missing.push('Hands');
    if (typeof Camera === 'undefined') missing.push('Camera');
    if (typeof video === 'undefined') missing.push('video');
    if (typeof scene === 'undefined') missing.push('scene');
    if (typeof mapToScene === 'undefined') missing.push('mapToScene');
    if (typeof distance === 'undefined') missing.push('distance');
    if (typeof distanceXY === 'undefined') missing.push('distanceXY');
    if (typeof getNearestObject === 'undefined') missing.push('getNearestObject');
    if (typeof objects === 'undefined') missing.push('objects');
    if (typeof videoWidth === 'undefined') missing.push('videoWidth');
    if (typeof videoHeight === 'undefined') missing.push('videoHeight');
    if (missing.length) {
      console.error('hand_gestures.js missing dependencies:', missing);
      return false;
    }
    return true;
  }

  function detectGesture(landmarks) {
    const wrist = landmarks[0];
    const fingers = [
      { base: 2, tip: 4 }, // Thumb (use IP joint as base)
      { base: 5, tip: 8 }, // Index
      { base: 9, tip: 12 }, // Middle
      { base: 13, tip: 16 }, // Ring
      { base: 17, tip: 20 } // Pinky
    ];
    const states = fingers.map(f => {
      const base = landmarks[f.base];
      const tip = landmarks[f.tip];
      const dist_base_wrist = distance(wrist, base);
      const dist_tip_wrist = distance(wrist, tip);
      return dist_tip_wrist > dist_base_wrist * 1.2 ? 'extended' : 'curled';
    });
    const extendedCount = states.filter(s => s === 'extended').length;
    if (extendedCount === 0) return 'fist';
    if (extendedCount >= 4) return 'open';
    if (states[1] === 'extended' && states[2] === 'extended' && states[0] === 'curled' && states[3] === 'curled' && states[4] === 'curled') {
      return 'two_fingers';
    }
    return 'none';
  }

  // Local state for hand rendering
  let connections, handLines, hands, cameraFeed;

  function initHands() {
    if (!ensureDeps()) return;

    // Define connections for hand wireframe
    connections = [
      [0,1], [1,2], [2,3], [3,4],      // Thumb
      [0,5], [5,6], [6,7], [7,8],      // Index
      [0,9], [9,10], [10,11], [11,12], // Middle
      [0,13], [13,14], [14,15], [15,16], // Ring
      [0,17], [17,18], [18,19], [19,20]  // Pinky
    ];

    // Create hand wireframe lines
    handLines = connections.map((_, i) => {
      const line = BABYLON.MeshBuilder.CreateLines(`handLine${i}`, {
        points: [new BABYLON.Vector3(0, 0, 0), new BABYLON.Vector3(0, 0, 0)],
        updatable: true,
        color: new BABYLON.Color3(1, 0, 0)
      }, scene);
      line.isVisible = false;
      return line;
    });

    function onResults(results) {
      if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        const landmarks = results.multiHandLandmarks[0];
        // update global gesture state
        if (typeof currentGesture !== 'undefined') {
          currentGesture = detectGesture(landmarks);
        }

        // Update hand lines
        connections.forEach((conn, i) => {
          const p1 = landmarks[conn[0]];
          const p2 = landmarks[conn[1]];
          const [x1, y1] = mapToScene(p1.x * videoWidth, p1.y * videoHeight);
          const [x2, y2] = mapToScene(p2.x * videoWidth, p2.y * videoHeight);
          const points = [
            new BABYLON.Vector3(x1, y1, 0),
            new BABYLON.Vector3(x2, y2, 0)
          ];
          BABYLON.MeshBuilder.CreateLines(`handLine${i}`, {
            points,
            updatable: true,
            instance: handLines[i]
          }, scene);
          handLines[i].isVisible = true;
        });

        // Compute pinch between thumb tip (4) and index tip (8)
        const thumbTip = landmarks[4];
        const indexTip = landmarks[8];
        const pinchPx = distanceXY(
          thumbTip.x * videoWidth, thumbTip.y * videoHeight,
          indexTip.x * videoWidth, indexTip.y * videoHeight
        );
        const pinchThresholdPx = 35;

        if (typeof wasGrabbing !== 'undefined') wasGrabbing = typeof isGrabbing !== 'undefined' ? isGrabbing : false;
        if (typeof isGrabbing !== 'undefined') isGrabbing = pinchPx < pinchThresholdPx;

        // Cursor in scene coords from index tip
        const [cursorX, cursorY] = mapToScene(indexTip.x * videoWidth, indexTip.y * videoHeight);
        const cursor = new BABYLON.Vector3(cursorX, cursorY, 0);

        // On grab start: choose nearest visible object to the cursor
        if (typeof isGrabbing !== 'undefined' && typeof wasGrabbing !== 'undefined' && isGrabbing && !wasGrabbing) {
          const candidateId = getNearestObject(cursor, 1.5);
          if (candidateId) {
            if (typeof activeObjectId !== 'undefined') activeObjectId = candidateId;
            const entry = objects.get(activeObjectId);
            entry.grabOffset = entry.mesh.position.subtract(cursor);
            // Initialize rotation tracking based on index finger direction (5 -> 8)
            const indexMCP = landmarks[5];
            const vX = (indexTip.x - indexMCP.x);
            const vY = (indexTip.y - indexMCP.y);
            entry.lastAngle = Math.atan2(vY, vX);
            entry.mesh.isVisible = true;
          } else {
            if (typeof activeObjectId !== 'undefined') activeObjectId = null;
          }
        }

        // While grabbing: move and rotate active object
        if (typeof isGrabbing !== 'undefined' && isGrabbing && typeof activeObjectId !== 'undefined' && activeObjectId && objects.has(activeObjectId)) {
          const entry = objects.get(activeObjectId);
          entry.mesh.position = cursor.add(entry.grabOffset);
          const indexMCP = landmarks[5];
          const vX = (indexTip.x - indexMCP.x);
          const vY = (indexTip.y - indexMCP.y);
          const angle = Math.atan2(vY, vX);
          if (entry.lastAngle !== null) {
            const delta = angle - entry.lastAngle;
            entry.mesh.rotation.z += delta;
          }
          entry.lastAngle = angle;
        } else {
          // On release: reset rotation tracker and clear active if not grabbing
          if (typeof wasGrabbing !== 'undefined' && wasGrabbing && typeof activeObjectId !== 'undefined' && activeObjectId && objects.has(activeObjectId)) {
            const entry = objects.get(activeObjectId);
            entry.lastAngle = null;
          }
          if (typeof isGrabbing !== 'undefined' && !isGrabbing && typeof activeObjectId !== 'undefined') {
            activeObjectId = null;
          }
        }
      } else {
        if (typeof currentGesture !== 'undefined') currentGesture = 'none';
        if (handLines) handLines.forEach(line => line.isVisible = false);
        if (typeof wasGrabbing !== 'undefined' && typeof isGrabbing !== 'undefined') {
          wasGrabbing = isGrabbing;
          isGrabbing = false;
        }
        if (typeof activeObjectId !== 'undefined') activeObjectId = null;
      }
    }

    // MediaPipe Hands setup
    const cacheBust = Date.now();
    hands = new Hands({ locateFile: (file) => `/static/js/${file}?v=${cacheBust}` });
    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    });
    hands.onResults(onResults);

    cameraFeed = new Camera(video, {
      onFrame: async () => await hands.send({ image: video }),
      width: 640,
      height: 480
    });
    cameraFeed.start();
  }

  // Expose initializer to global scope
  window.initHands = initHands;
})();
