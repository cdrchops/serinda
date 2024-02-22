var runDemo = function () {
    // let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
    // let transparent = new cv.Mat(video.height, video.width, cv.CV_8UC4);
    // let dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);
    // let cap = new cv.VideoCapture(video);
    // console.log(video.height);
    // console.log(video.width);
    //
    // // let dictionary = new cv.Dictionary(cv.DICT_6X6_250);
    // let markerIds = new cv.Mat();
    // let markerCorners = new cv.MatVector();
    // let rvecs = new cv.Mat();
    // let tvecs = new cv.Mat();
    // let cameraMatrix = cv.matFromArray(3, 3, cv.CV_64F, [9.6635571716090658e+02, 0., 2.0679307818305685e+02, 0.,
    //     9.6635571716090658e+02, 2.9370020600555273e+02, 0., 0., 1.]);
    // let distCoeffs = cv.matFromArray(5, 1, cv.CV_64F, [-1.5007354215536557e-03, 9.8722389825801837e-01,
    //     1.7188452542408809e-02, -2.6805958820424611e-02, -2.3313928379240205e+00]);
    //
    // const FPS = 30;
    // function processVideo() {
    //     cap.read(src);
    //     let begin = Date.now();
    //
    //     // start processing
    //     faceCascade(src, dst);
    //
    //     //processAruco is just for Aruco markers
    //     // processAruco(src, dst, transparent, dictionary, markerCorners, markerIds, rvecs, tvecs, cameraMatrix, distCoeffs);
    //
    //     // schedule the next one.
    //     let delay = 1000 / FPS - (Date.now() - begin);
    //     setTimeout(processVideo, delay);
    // }
    //
    // processVideo();


    let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
    // let dst = new cv.Mat(video.height, video.width, cv.CV_8UC4);
    // let gray = new cv.Mat();
    // let cap = new cv.VideoCapture(video);
    // let faces = new cv.RectVector();
    // let classifier = new cv.CascadeClassifier();
    //
    // // load pre-trained classifiers
    // // classifier.load('http://localhost:5000/static/haarcascade_frontalface_default.xml');
    // // face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    // // classifier = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    // // eye_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')
    //
    // const FPS = 30;
    // function processVideo() {
    //     try {
    //         // if (!streaming) {
    //         //     // clean and stop.
    //         //     src.delete();
    //         //     dst.delete();
    //         //     gray.delete();
    //         //     faces.delete();
    //         //     classifier.delete();
    //         //     return;
    //         // }
    //         let begin = Date.now();
    //         // start processing.
    //         cap.read(src);
    //         src.copyTo(dst);
    //         cv.cvtColor(dst, gray, cv.COLOR_RGBA2GRAY, 0);
    //         // detect faces.
    //         classifier.detectMultiScale(gray, faces, 1.1, 3, 0);
    //         // // draw faces.
    //         // for (let i = 0; i < faces.size(); ++i) {
    //         //     let face = faces.get(i);
    //         //     let point1 = new cv.Point(face.x, face.y);
    //         //     let point2 = new cv.Point(face.x + face.width, face.y + face.height);
    //         //     cv.rectangle(dst, point1, point2, [255, 0, 0, 255]);
    //         // }
    //         cv.imshow('arucoCanvasOutput', dst);
    //         // schedule the next one.
    //         let delay = 1000/FPS - (Date.now() - begin);
    //         setTimeout(processVideo, delay);
    //     } catch (err) {
    //         console.log(err);
    //         // utils.printError(err);
    //     }
    // };
    //
    // // schedule the first one.
    // setTimeout(processVideo, 0);
}

// let video = document.getElementById('videoInput');



function faceCascade(src, dst) {

        let faces = new cv.RectVector();
        let classifier = new cv.CascadeClassifier();
        let gray = new cv.Mat();

        // load pre-trained classifiers
        classifier.load('/static/haarcascade_frontalface_default.xml');
        // classifier.load('/static/haarcascade_frontalface_alt2.xml');

        src.copyTo(dst);
        cv.cvtColor(dst, gray, cv.COLOR_RGBA2GRAY, 0);
        // detect faces.
        // classifier.detectMultiScale(gray, faces, 1.1, 3, 0);
        let msize = new cv.Size(0, 0);
        // classifier.detectMultiScale(gray, faces, 1.1, 3, 0, msize, msize);

        // // draw faces.
        // for (let i = 0; i < faces.size(); ++i) {
        //     let face = faces.get(i);
        //     let point1 = new cv.Point(face.x, face.y);
        //     let point2 = new cv.Point(face.x + face.width, face.y + face.height);
        //     cv.rectangle(dst, point1, point2, [255, 0, 0, 255]);
        //
        //     console.log(JSON.stringify(point1));
        //     console.log(JSON.stringify(point2));
        // }
        //
        // cv.imshow('canvasOutput', dst);
}

function processAruco(src, dst, transparent, dictionary, markerCorners, markerIds, rvecs, tvecs, cameraMatrix, distCoeffs) {
    cv.cvtColor(src, dst, cv.COLOR_RGBA2RGB, 0);

    cv.detectMarkers(dst, dictionary, markerCorners, markerIds);
    if (markerIds.rows > 0) {
        cv.estimatePoseSingleMarkers(markerCorners, 0.1, cameraMatrix, distCoeffs, rvecs, tvecs);

        for (let i = 0; i < markerIds.rows; ++i) {
            let rvec = cv.matFromArray(3, 1, cv.CV_64F, [rvecs.doublePtr(0, i)[0], rvecs.doublePtr(0, i)[1], rvecs.doublePtr(0, i)[2]]);
            let tvec = cv.matFromArray(3, 1, cv.CV_64F, [tvecs.doublePtr(0, i)[0], tvecs.doublePtr(0, i)[1], tvecs.doublePtr(0, i)[2]]);
            cv.drawAxis(dst, cameraMatrix, distCoeffs, rvec, tvec, 0.1);
            rvec.delete();
            tvec.delete();
        }
        // starts top left, then goes clockwise
        for (let j = 0; j < markerCorners.get(0).data32F.length; j += 2) {
            cv.circle(
                dst,
                new cv.Point(markerCorners.get(0).data32F[j], markerCorners.get(0).data32F[j + 1]),
                3,
                new cv.Scalar(255, 0, 0)
            );
        }
        copyCorners = true;
        markerId = markerIds.rows;
        markerCorner = markerCorners.get(0).data32F;
        tvec = tvecs.data64F[2]; // z distance

        // Normalize z rotation i.e. rvec
        if ((rvecs.data64F[0] > -1.5 && rvecs.data64F[0] < 0.0) || (rvecs.data64F[0] < 2.0 && rvecs.data64F[0] > 0.0))
            rvec = 2.0;
        else
            rvec = rvecs.data64F[0];
    } else {
        copyCorners = false;
        markerId = 0;
        markerCorner = [0, 0, 0, 0, 0, 0, 0, 0];
        tvec = 1;
        rvec = 1;
    }
}