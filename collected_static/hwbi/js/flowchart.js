
var height = 75,
    width = 1000;

var svg = d3.select("#flowchart").append("svg")
        .attr("height", height)
        .attr("width", width)




//DROP Shadow
//// filters go in defs element
//var defs = svg.append("defs");
//
//// create filter with id #drop-shadow
//// height=130% so that the shadow is not clipped
//var filter = defs.append("filter")
//    .attr("id", "drop-shadow")
//    .attr("height", "130%");
//
//// SourceAlpha refers to opacity of graphic that this filter will be applied to
//// convolve that with a Gaussian with standard deviation 3 and store result
//// in blur
//filter.append("feGaussianBlur")
//    .attr("in", "SourceAlpha")
//    .attr("stdDeviation", 2)
//    .attr("result", "blur");
//
//// translate output of Gaussian blur to the right and downwards with 2px
//// store result in offsetBlur
//filter.append("feOffset")
//    .attr("in", "blur")
//    .attr("dx", 2)
//    .attr("dy", 2)
//    .attr("result", "offsetBlur");
//
//// overlay original SourceGraphic over translated blurred opacity by using
//// feMerge filter. Order of specifying inputs is important!
//var feMerge = filter.append("feMerge");
//
//feMerge.append("feMergeNode")
//    .attr("in", "offsetBlur")
//feMerge.append("feMergeNode")
//    .attr("in", "SourceGraphic")
//feMerge.append("feMergeNode")
//    .attr("in", "SourceGraphic")
//;




var rectangles = [
{ Rect: '22 Services', url: "http://www.epa.gov", x: '10'},
{ Rect: '8 Domains', url: "http://www.epa.gov", x: '10'},
{ Rect: 'Relative Importance Values', url: "http://www.epa.gov", x: '10'}
];


//services rectangle
var rect = svg.append("a")
    .attr("transform", "translate(1,10)")
    .attr("xlink:href", "http://www.epa.gov")
    .append("rect")
    .attr("height", 54)
    .attr("width", 75)
    .attr("rx", 10)
    .attr("ry", 10)
    .attr("fill", "#DEE7EF") //#bccede
    //.attr("stroke", "gray");
    //.attr("stroke-width", 1)
    //.style("filter", "url(#drop-shadow)")
    //.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

svg.append("svg:text")
          .style("pointer-events", "none")
    .attr("transform", "translate(0,9)")
  .attr("class", "score")
  .attr("dy", 34)
  .attr("dx", 37)
  .attr("text-anchor", "middle")
  .attr("font-size", "12px")
  .attr("font-family", "Verdana, Geneva, sans-serif")
  .text("22 Services");

//domains rectangle
var rect = svg.append("a")
    .attr("transform", "translate(97,10)")
    .attr("xlink:href", "http://www.epa.gov")
    .append("rect")
    .attr("height", 54)
    .attr("width", 75)
    .attr("rx", 10)
    .attr("ry", 10)
    .attr("fill", "#DEE7EF")
    //.attr("stroke", "gray");

svg.append("svg:text")
      .style("pointer-events", "none")
      .attr("transform", "translate(89,9)")
      .attr("class", "score")
      .attr("dy", 34)
      .attr("dx", 45)
      .attr("text-anchor", "middle")
      .attr("font-size", "12px")
      .attr("font-family", "Verdana, Geneva, sans-serif")
      .text("8 Domains");

//RIV rectangle
var rect = svg.append("a")
    .attr("transform", "translate(192,10)")
    .attr("xlink:href", "http://www.epa.gov")
    .append("rect")
    .attr("height", 54)
    .attr("width", 75)
    .attr("rx", 10)
    .attr("ry", 10)
    .attr("fill", "#DEE7EF")
    //.attr("stroke", "gray");

svg.append("svg:text")
    .style("pointer-events", "none")
    .attr("transform", "translate(184,9)")
  .attr("class", "score")
  .attr("dy", 18)
  .attr("dx", 45)
  .attr("text-anchor", "middle")
  .attr("font-size", "12px")
  .attr("font-family", "Verdana, Geneva, sans-serif")
  .text("Relative");

svg.append("svg:text")
          .style("pointer-events", "none")
    .attr("transform", "translate(184,9)")
  .attr("class", "score")
  .attr("dy", 35)
  .attr("dx", 45)
  .attr("text-anchor", "middle")
  .attr("font-size", "11.5px")
  .attr("font-family", "Verdana, Geneva, sans-serif")
  .text("Importance");

svg.append("svg:text")
          .style("pointer-events", "none")
    .attr("transform", "translate(184,9)")
  .attr("class", "score")
  .attr("dy", 52)
  .attr("dx", 45)
  .attr("text-anchor", "middle")
  .attr("font-size", "12px")
  .attr("font-family", "Verdana, Geneva, sans-serif")
  .text("Values");

//hwbi circle
var hwbicirc = svg.append("a")
    .attr("transform", "translate(279,0)")
    .attr("xlink:href", "http://www.google.com")
    .append("circle")
    .attr("r", 28)
    .attr("cx", 36)
    .attr("cy", 38)
    .attr("fill", "#DEE7EF")
    //.attr("stroke", "gray");

svg.append("svg:text")
  .style("pointer-events", "none")
  .attr("transform", "translate(279,0)")
  .attr("class", "score")
  .attr("dy", 44)
  .attr("dx", 36)
  .attr("text-anchor", "middle")
  .attr("font-size", "14px")
  .style("font-weight", "bold")
  .text("HWBI");


//arrow 1
var arrowYPosition = 38
var arrowXStartPosition = 76
var arrowXEndPosition = 96;

var labelLine = svg.append("line")
        .attr("x1", arrowXStartPosition)
        .attr("y1", arrowYPosition)
        .attr("x2", arrowXEndPosition)
        .attr("y2", arrowYPosition)
        .attr("stroke-width", 1.5)
        .attr("stroke", "#DEE7EF");

var right = svg.append("line")
        .attr("x1", arrowXEndPosition)
        .attr("y1", arrowYPosition)
        .attr("x2", arrowXEndPosition - 8)
        .attr("y2", arrowYPosition + 8)
        .attr("stroke-width", 1.5)
        .attr("stroke", "#DEE7EF");

var left = svg.append("line")
        .attr("x1", arrowXEndPosition)
        .attr("y1", arrowYPosition)
        .attr("x2", arrowXEndPosition - 8)
        .attr("y2", arrowYPosition - 8)
        .attr("stroke-width", 1.5)
        .attr("stroke", "#DEE7EF");

//arrow 2
var arrowYPosition = 40
var arrowXStartPosition = 171
var arrowXEndPosition = 191;

var labelLine = svg.append("line")
        .attr("x1", arrowXStartPosition)
        .attr("y1", arrowYPosition)
        .attr("x2", arrowXEndPosition)
        .attr("y2", arrowYPosition)
        .attr("stroke-width", 1.5)
        .attr("stroke", "#DEE7EF");

var right = svg.append("line")
        .attr("x1", arrowXEndPosition)
        .attr("y1", arrowYPosition)
        .attr("x2", arrowXEndPosition - 8)
        .attr("y2", arrowYPosition + 8)
        .attr("stroke-width", 1.5)
        .attr("stroke", "#DEE7EF");

var left = svg.append("line")
        .attr("x1", arrowXEndPosition)
        .attr("y1", arrowYPosition)
        .attr("x2", arrowXEndPosition - 8)
        .attr("y2", arrowYPosition - 8)
        .attr("stroke-width", 1.5)
        .attr("stroke", "#DEE7EF");

//arrow 3
var arrowYPosition = 40
var arrowXStartPosition = 266
var arrowXEndPosition = 286;

var labelLine = svg.append("line")
        .attr("x1", arrowXStartPosition)
        .attr("y1", arrowYPosition)
        .attr("x2", arrowXEndPosition)
        .attr("y2", arrowYPosition)
        .attr("stroke-width", 1.5)
        .attr("stroke", "#DEE7EF");

var right = svg.append("line")
        .attr("x1", arrowXEndPosition)
        .attr("y1", arrowYPosition)
        .attr("x2", arrowXEndPosition - 8)
        .attr("y2", arrowYPosition + 8)
        .attr("stroke-width", 1.5)
        .attr("stroke", "#DEE7EF");

var left = svg.append("line")
        .attr("x1", arrowXEndPosition)
        .attr("y1", arrowYPosition)
        .attr("x2", arrowXEndPosition - 8)
        .attr("y2", arrowYPosition - 8)
        .attr("stroke-width", 1.5)
        .attr("stroke", "#DEE7EF");