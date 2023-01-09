// function testPlugin() {
//     alert('this worked');
// }
//
// document.getElementById("go_button").addEventListener("click", function (e) {
//     var url = document.getElementById("url").value;
//     runOCR(url);
// });
//
// function runOCR(url) {
//     console.log("inside here");
//     Tesseract.recognize(url)
//         .then(function (result) {
//             document.getElementById("ocr_results").innerText = result.text;
//         }).progress(function (result) {
//         document.getElementById("ocr_status").innerText = result["status"] + " (" + (result["progress"] * 100) + "%)";
//     });
// }
//
//
// // $('#tesseractjs').hide();