var cubeRotation = 0.0;
// will set to true when video can be copied to texture
var copyVideo = false;

//main();

//
// Start here
//
function main() {
  const canvas = document.getElementById('webgl-draw');
  const gl = canvas.getContext('webgl');
  // If we don't have a GL context, give up now

  if (!gl) {
    alert('Unable to initialize WebGL. Your browser or machine may not support it.');
    return;
  }

  // Vertex shader program

  const vsSource = `
    attribute vec4 aVertexPosition;
    attribute vec3 aVertexColor;
    attribute vec2 aTextureCoord;

    uniform vec2 u_resolution;
    uniform float uVertexEnable;
    uniform mat4 uModelViewMatrix;

    varying highp vec2 vTextureCoord;
    varying highp vec3 fVertexColor;
    varying mediump float uFragmentEnable;

    void main(void) {
        // convert the position from pixels to 0.0 to 1.0
        vec2 zeroToOne = vec2(aVertexPosition.x, aVertexPosition.y) / u_resolution;
    
        // convert from 0->1 to 0->2
        vec2 zeroToTwo = zeroToOne * 2.0;
    
        // convert from 0->2 to -1->+1 (clipspace)
        vec2 clipSpace = zeroToTwo - 1.0;

        gl_Position = vec4(clipSpace * vec2(1.0, -1.0), aVertexPosition.z, 1.0);
        
      vTextureCoord = aTextureCoord;
      fVertexColor = aVertexColor;
      uFragmentEnable = uVertexEnable;
    }
  `;

  // Fragment shader program

  const fsSource = `
    varying highp vec2 vTextureCoord;
    varying highp vec3 fVertexColor;

    uniform sampler2D uSampler;
    varying mediump float uFragmentEnable;

    void main(void) {
      highp vec4 texelColor = texture2D(uSampler, vTextureCoord);
      
      if (uFragmentEnable == 1.0) {
        gl_FragColor = vec4(texelColor.rgb, 1.0);
      } else {
        gl_FragColor = vec4(fVertexColor.rgb, 1.0);
      }
    }
  `;

  // Initialize a shader program; this is where all the lighting
  // for the vertices and so forth is established.
  const shaderProgram = initShaderProgram(gl, vsSource, fsSource);

  // Collect all the info needed to use the shader program.
  // Look up which attributes our shader program is using
  // for aVertexPosition, aVertexNormal, aTextureCoord,
  // and look up uniform locations.
  const programInfo = {
    program: shaderProgram,
    attribLocations: {
      vertexPosition: gl.getAttribLocation(shaderProgram, 'aVertexPosition'),
      vertexColor: gl.getAttribLocation(shaderProgram, 'aVertexColor'),
      textureCoord: gl.getAttribLocation(shaderProgram, 'aTextureCoord'),
    },
    uniformLocations: {
      uSampler: gl.getUniformLocation(shaderProgram, 'uSampler'),
      resolution: gl.getUniformLocation(shaderProgram, 'u_resolution'),
      enable: gl.getUniformLocation(shaderProgram, 'uVertexEnable')
    },
  };

  // Here's where we call the routine that builds all the
  // objects we'll be drawing.
  let buffers = initBuffers(gl);

  const texture = initTexture(gl);

  const video = setupVideo(document.getElementById('videoInput').srcObject);

  var then = 0;

  // Draw the scene repeatedly
  function render(now) {
    now *= 0.001;  // convert to seconds
    const deltaTime = now - then;
    then = now;

    if (copyVideo) {
      updateTexture(gl, texture, video);
    }

    if (copyCorners) {
      buffers = initBuffers(gl, markerCorner, rvec, tvec);
      drawScene(gl, programInfo, buffers, texture, deltaTime, markerId);
    } else {
      drawScene(gl, programInfo, buffers, texture, deltaTime);
    }

    requestAnimationFrame(render);
  }
  requestAnimationFrame(render);
}

function setupVideo(src) {
  const video = document.createElement('video');

  var playing = false;
  var timeupdate = false;

  // Waiting for these 2 events ensures
  // there is data in the video

  video.addEventListener('playing', function() {
     playing = true;
     checkReady();
  }, true);

  video.addEventListener('timeupdate', function() {
     timeupdate = true;
     checkReady();
  }, true);

  //video.src = url;
  video.srcObject = src;
  video.play();

  function checkReady() {
    if (playing && timeupdate) {
      copyVideo = true;
    }
  }

  return video;
}

//
// initBuffers
//
// Initialize the buffers we'll need. For this demo, we just
// have one object -- a simple three-dimensional cube.
//
function initBuffers(gl, markerCorner = [0, 0, 0, 0, 0, 0, 0, 0], rvec = 1, tvec = 1) {

  // Create a buffer for the cube's vertex positions.

  const positionBuffer = gl.createBuffer();

  // Select the positionBuffer as the one to apply buffer
  // operations to from here out.

  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

  // Now create an array of positions for the cube.

  const positions = [
    // Front face
    // x, y, z        r, g, b
    0, 0, 1.0,        1.0, 1.0, 1.0,
    640, 0, 1.0,      1.0, 1.0, 1.0,
    640, 480, 1.0,    1.0, 1.0, 1.0,
    0, 480, 1.0,      1.0, 1.0, 1.0
  ];

  // Now pass the list of positions and colors into WebGL to build the
  // shape. We do this by creating a Float32Array from the
  // JavaScript array, then use it to fill the current buffer.

  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);

  // Now set up the texture coordinates for the faces.

  const textureCoordBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, textureCoordBuffer);

  const textureCoordinates = [
    // Front
    0.0,  0.0,
    1.0,  0.0,
    1.0,  1.0,
    0.0,  1.0
  ];

  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(textureCoordinates),
                gl.STATIC_DRAW);

  // Build the element array buffer; this specifies the indices
  // into the vertex arrays for each face's vertices.

  const indexBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);

  // This array defines each face as two triangles, using the
  // indices into the vertex array to specify each triangle's
  // position.

  const indices = [
    0,  1,  2,      0,  2,  3,    // front
  ];

  // Now send the element array to GL

  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,
      new Uint16Array(indices), gl.STATIC_DRAW);

  // Create a buffer for triangle object

  const squareBuffer = gl.createBuffer();

  // Select the triangleBuffer as the one to apply buffer
  // operations to from here out.

  gl.bindBuffer(gl.ARRAY_BUFFER, squareBuffer);


  // Create an array of positions for the triangle
  
  // Starts top left, then goes clockwise.
  // Flip z value when rotating around the cube
  const squarePosition = [
    // x, y, z                                                            r, g, b
    // Front face
    markerCorner[6], markerCorner[7],  -1.0,                              1.0, 0.0, 0.0,
    markerCorner[6], markerCorner[7] - ( 120 / tvec / rvec ),  -1.0,      1.0, 0.0, 0.0,
    markerCorner[4], markerCorner[5] - ( 120 / tvec / rvec ),  -1.0,      1.0, 0.0, 0.0,
    markerCorner[4], markerCorner[5],  -1.0,                              1.0, 0.0, 0.0,  

    // Back face
    markerCorner[0], markerCorner[1],  -1.0,                              1.0, 0.0, 0.0,
    markerCorner[0], markerCorner[1] - ( 120 / tvec / rvec ),  -1.0,      1.0, 0.0, 0.0,
    markerCorner[2], markerCorner[3] - ( 120 / tvec / rvec ),  -1.0,      1.0, 0.0, 0.0,
    markerCorner[2], markerCorner[3],  -1.0,                              1.0, 0.0, 0.0,

    // Top face
    markerCorner[0], markerCorner[1] - ( 120 / tvec / rvec ),  -1.0,      1.0, 0.0, 0.0,
    markerCorner[2], markerCorner[3] - ( 120 / tvec / rvec ),  -1.0,      1.0, 0.0, 0.0,
    markerCorner[4], markerCorner[5] - ( 120 / tvec / rvec ),  -1.0,      1.0, 0.0, 0.0,
    markerCorner[6], markerCorner[7] - ( 120 / tvec / rvec ),  -1.0,      1.0, 0.0, 0.0,

     // Bottom face
     markerCorner[0], markerCorner[1],  1.0,                              1.0, 0.0, 0.0,
     markerCorner[2], markerCorner[3],  1.0,                              1.0, 0.0, 0.0,
     markerCorner[4], markerCorner[5],  1.0,                              1.0, 0.0, 0.0,
     markerCorner[6], markerCorner[7],  1.0,                              1.0, 0.0, 0.0,

     // Right face
     markerCorner[0], markerCorner[1], -1.0,                              1.0, 0.0, 0.0,
     markerCorner[0], markerCorner[1] - ( 120 / tvec / rvec ), -1.0,      1.0, 0.0, 0.0,
     markerCorner[6], markerCorner[7] - ( 120 / tvec / rvec ),  -1.0,     1.0, 0.0, 0.0,
     markerCorner[6], markerCorner[7],  -1.0,                             1.0, 0.0, 0.0,

    // Left face
    markerCorner[2], markerCorner[3], -1.0,                               1.0, 0.0, 0.0,
    markerCorner[2], markerCorner[3] - ( 120 / tvec / rvec ),  -1.0,      1.0, 0.0, 0.0,
    markerCorner[4], markerCorner[5] - ( 120 / tvec / rvec ),  -1.0,      1.0, 0.0, 0.0,
    markerCorner[4], markerCorner[5], -1.0,                               1.0, 0.0, 0.0

  ];

  // Pass the list of positions and colors into WebGL

  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(squarePosition), gl.STATIC_DRAW);

  // Build the element array buffer; this specifies the indices
  // into the vertex arrays for each face's vertices.

  const squareIndexBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, squareIndexBuffer);

  // This array defines each face as two triangles, using the
  // indices into the vertex array to specify each triangle's
  // position.

  const squareIndices = [
    0,  1,  2,      0,  2,  3,    // front
    4,  5,  6,      4,  6,  7,    // back
    8,  9,  10,     8,  10, 11,   // top
    12, 13, 14,     12, 14, 15,   // bottom
    16, 17, 18,     16, 18, 19,   // right
    20, 21, 22,     20, 22, 23,   // left
  ];

  // Now send the element array to GL

  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,
      new Uint16Array(squareIndices), gl.STATIC_DRAW);

  return {
    position: positionBuffer,
    textureCoord: textureCoordBuffer,
    indices: indexBuffer,
    square: squareBuffer,
    squareIndices: squareIndexBuffer
  };
}

//
// Initialize a texture.
//
function initTexture(gl) {
  const texture = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, texture);

  // Because video havs to be download over the internet
  // they might take a moment until it's ready so
  // put a single pixel in the texture so we can
  // use it immediately.
  const level = 0;
  const internalFormat = gl.RGBA;
  const width = 1;
  const height = 1;
  const border = 0;
  const srcFormat = gl.RGBA;
  const srcType = gl.UNSIGNED_BYTE;
  const pixel = new Uint8Array([0, 0, 255, 255]);  // opaque blue
  gl.texImage2D(gl.TEXTURE_2D, level, internalFormat,
                width, height, border, srcFormat, srcType,
                pixel);

  // Turn off mips and set  wrapping to clamp to edge so it
  // will work regardless of the dimensions of the video.
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);

  return texture;
}

//
// copy the video texture
//
function updateTexture(gl, texture, video) {
  const level = 0;
  const internalFormat = gl.RGBA;
  const srcFormat = gl.RGBA;
  const srcType = gl.UNSIGNED_BYTE;
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.texImage2D(gl.TEXTURE_2D, level, internalFormat,
                srcFormat, srcType, video);
}

function isPowerOf2(value) {
  return (value & (value - 1)) == 0;
}

//
// Draw the scene.
//
function drawScene(gl, programInfo, buffers, texture, deltaTime, markerId = 0) {
  gl.clearColor(0.0, 0.0, 0.0, 1.0);  // Clear to black, fully opaque
  gl.clearDepth(1.0);                 // Clear everything
  gl.enable(gl.DEPTH_TEST);           // Enable depth testing
  gl.depthFunc(gl.LEQUAL);            // Near things obscure far things

  // Clear the canvas before we start drawing on it.

  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

  // Tell WebGL how to pull out the positions from the position
  // buffer into the vertexPosition attribute
  {
    const numComponents = 3;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 6 * Float32Array.BYTES_PER_ELEMENT;
    const offset = 0;
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
    gl.vertexAttribPointer(
        programInfo.attribLocations.vertexPosition,
        numComponents,
        type,
        normalize,
        stride,
        offset);
    gl.enableVertexAttribArray(
        programInfo.attribLocations.vertexPosition);
  }

  // Tell WebGL how to pull out the colors from the position
  // buffer into the vColor attribute
  {
    const numComponents = 3;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 6 * Float32Array.BYTES_PER_ELEMENT;
    const offset = 3 * Float32Array.BYTES_PER_ELEMENT;
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
    gl.vertexAttribPointer(
        programInfo.attribLocations.vertexColor,
        numComponents,
        type,
        normalize,
        stride,
        offset);
    gl.enableVertexAttribArray(
        programInfo.attribLocations.vertexColor);
  }

  // Tell WebGL how to pull out the texture coordinates from
  // the texture coordinate buffer into the textureCoord attribute.
  {
    const numComponents = 2;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 0;
    const offset = 0;
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.textureCoord);
    gl.vertexAttribPointer(
        programInfo.attribLocations.textureCoord,
        numComponents,
        type,
        normalize,
        stride,
        offset);
    gl.enableVertexAttribArray(
        programInfo.attribLocations.textureCoord);
  }

  // Tell WebGL which indices to use to index the vertices
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.indices);

  // Tell WebGL to use our program when drawing

  gl.useProgram(programInfo.program);

  // Specify the texture to map onto the faces.

  // Tell WebGL we want to affect texture unit 0
  gl.activeTexture(gl.TEXTURE0);

  // Bind the texture to texture unit 0
  gl.bindTexture(gl.TEXTURE_2D, texture);

  // Tell the shader we bound the texture to texture unit 0
  gl.uniform2f(programInfo.uniformLocations.resolution, gl.canvas.width, gl.canvas.height);
  gl.uniform1i(programInfo.uniformLocations.uSampler, 0);
  gl.uniform1f(programInfo.uniformLocations.enable, 1.0);

  {
    const vertexCount = 6;
    const type = gl.UNSIGNED_SHORT;
    const offset = 0;
    gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
  }

  // Check if aruco marker is detected

  if (markerId > 0) {

    // Tell WebGL how to pull out the positions from the square
    // buffer into the vertexPosition attribute
    {
      const numComponents = 3;
      const type = gl.FLOAT;
      const normalize = false;
      const stride = 6 * Float32Array.BYTES_PER_ELEMENT;
      const offset = 0;
      gl.bindBuffer(gl.ARRAY_BUFFER, buffers.square);
      gl.vertexAttribPointer(
          programInfo.attribLocations.vertexPosition,
          numComponents,
          type,
          normalize,
          stride,
          offset);
      gl.enableVertexAttribArray(
          programInfo.attribLocations.vertexPosition);
    }

    // Tell WebGL how to pull out the colors from the square
    // buffer into the vColor attribute
    {
      const numComponents = 3;
      const type = gl.FLOAT;
      const normalize = false;
      const stride = 6 * Float32Array.BYTES_PER_ELEMENT;
      const offset = 3 * Float32Array.BYTES_PER_ELEMENT;
      gl.bindBuffer(gl.ARRAY_BUFFER, buffers.square);
      gl.vertexAttribPointer(
          programInfo.attribLocations.vertexColor,
          numComponents,
          type,
          normalize,
          stride,
          offset);
      gl.enableVertexAttribArray(
          programInfo.attribLocations.vertexColor);
    }

    // Tell WebGL which indices to use the index of the square vertices
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.squareIndices);

    {
      gl.disableVertexAttribArray(programInfo.attribLocations.textureCoord);
        gl.uniform1f(programInfo.uniformLocations.enable, 0.0);
    }

    {
      const vertexCount = 36;
      const type = gl.UNSIGNED_SHORT;
      const offset = 0;
      gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
    }
  } 
}

//
// Initialize a shader program, so WebGL knows how to draw our data
//
function initShaderProgram(gl, vsSource, fsSource) {
  const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource);
  const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource);

  // Create the shader program

  const shaderProgram = gl.createProgram();
  gl.attachShader(shaderProgram, vertexShader);
  gl.attachShader(shaderProgram, fragmentShader);
  gl.linkProgram(shaderProgram);

  // If creating the shader program failed, alert

  if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
    alert('Unable to initialize the shader program: ' + gl.getProgramInfoLog(shaderProgram));
    return null;
  }

  return shaderProgram;
}

//
// creates a shader of the given type, uploads the source and
// compiles it.
//
function loadShader(gl, type, source) {
  const shader = gl.createShader(type);

  // Send the source to the shader object

  gl.shaderSource(shader, source);

  // Compile the shader program

  gl.compileShader(shader);

  // See if it compiled successfully

  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    alert('An error occurred compiling the shaders: ' + gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
    return null;
  }

  return shader;
}

