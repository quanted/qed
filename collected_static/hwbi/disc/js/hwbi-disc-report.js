// This file is bundled using npm browserify, requires installing all required packages with npm in this directory then bundling after edits
var PDFDocument = require('pdfkit');
var blobStream = require('blob-stream');
require('buffer');

window.generateReport = function () {

    var reportDoc = new PDFDocument();
    var stream = reportDoc.pipe(blobStream());
    // Add stuff to report here
    // Graphics: Can add svg path http://pdfkit.org/docs/vector.html#svg_paths
    // Images: Had a lot of issues attempting to load images, both local and external images into the pdf.
    // Text:
    reportDoc.text('The content of the report will go here.');

    reportDoc.end();
    var saveData = (function () {
        var a = document.createElement("a");
        document.body.appendChild(a);
        a.style = "display: none";
        return function (blob, fileName) {
            var url = window.URL.createObjectURL(blob);
            a.href = url;
            a.download = fileName;
            a.target = "_black";
            a.click();
            setTimeout(function () {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }, 300);
            return false;
        };
    }());

    stream.on('finish', function () {
        var blob = stream.toBlob('application/pdf');
        saveData(blob, "DISC-report.pdf");
    });
}