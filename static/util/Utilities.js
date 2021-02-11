class Utilities {
    /*
     * copied from pinchToDraw.js
     * This function converts any finger or hand positions being passed
     * from the leap motion frame into a three.js vector3.
     * There are params to offsets the x,y,z position being passed. For
     * instance, if you want a cube to right of you palm you would pass in
     * a positive x value.
     */
    toVector3 (array, offset_x=0,offset_y=0, offset_z=0) {
        var a = new THREE.Vector3( 0, 0, 0 );
        let x = parseFloat(array[0]);
        let y = parseFloat(array[1]);
        let z = parseFloat(array[2]);

        a.x = x + offset_x;
        a.y = y + offset_y;
        a.z = z + offset_z;

        return a;
    }

    /*
     * copied from tritonPalm.js
     * This function converts any finger or hand positions being passed
     * from the leap motion frame into a three.js vector3.
     * There are params to offsets the x,y,z position being passed. For
     * instance, if you want a cube to right of you palm you would pass in
     * a positive x value.
     */
    checkPinch(hand) {
        if (hand.pinchStrength > 0.5 && hand.type === "right") {
            let indexFingerPos = hand.fingers[1].dipPosition;
            let thumbPos = hand.fingers[0].dipPosition;
            const midpoint = new THREE.Vector3();
            midpoint.add(this.toVector3(thumbPos));
            midpoint.add(this.toVector3(indexFingerPos));
            midpoint.multiplyScalar(0.5);
            return midpoint;
        }
    }
}

module.exports = new Utilities();