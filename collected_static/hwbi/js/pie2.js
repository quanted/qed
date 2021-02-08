// Define size and radius of pie chart
var width = 300,
    height = 300,
    radius = (Math.min(width, height) / 2)-4,
    innerRadius = 0.3 * radius;


//import data from a json file and run drawPieChart function onPageLoad
d3.json('/static_qed/hwbi/json/baseline.json', function (error, data) {
    drawPie2Chart("", data.outputs.domains);
});

//create svg element in the page "#pie" div and append g to the SVG
var svg2 = d3.selectAll("#pie2")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    //append another g element with class "slice" to svg
    svg2.append("g")
      .attr("class", "slice");



//function to update pie data based on county scores
function updateDomainScores2(domainScores) {
        updatePie2Chart("", domainScores);
    };

//draw pie chart on page load
function drawPie2Chart(error, data) {



    //use d3 to create the pie chart layout
    var pie = d3.layout.pie()
        .sort(null)
        .value(function (d) { return d.weight; });

    //hover over pie slice for label using d3 tooltip
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([50, 0])
        .html(function (d) {
            return d.data.description + ": <span style='color:orangered'>" + Math.round(d.data.score) + "</span>"
        })
        ;

    //call the hover tip utility
    svg2.call(tip);

    //use d3 to calculate size of arcs/angles
    var arc = d3.svg.arc()
        .innerRadius(innerRadius)
        .outerRadius(function (d) {
          return (radius - innerRadius) * (d.data.score/100) + innerRadius;
        });

    //use d3 to calculate size of outline arcs
    var outlineArc = d3.svg.arc()
        .innerRadius(innerRadius)
        .outerRadius(radius);

    //create variable path that appends a solidArc to the svg
    //"path" is any irregular SVG shape (pie slice)
    var path = svg2.selectAll(".solidArc")
        .data(pie(data))
        .enter().append("path")
        //assign colors to solidArc slice based on domain name
        .attr("fill", (function (d) {
            if (d.data.description == "Connection To Nature") { return "#569c83"; }
            if (d.data.description == "Cultural Fulfillment") { return "#325481"; }
            if (d.data.description == "Education") { return "#5E4EA1"; }
            if (d.data.description == "Health") { return "#9E0041"; }
            if (d.data.description == "Leisure Time") { return "#E1514B"; }
            if (d.data.description == "Living Standards") { return "#FB9F59"; }
            if (d.data.description == "Safety And Security") { return "#FAE38C"; }
            if (d.data.description == "Social Cohesion") { return "#EAF195"; }
        }))

        .attr("class", "solidArc")
        .attr("stroke", "gray")
        .attr("d", arc)
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    //create variable outerPath that appends an outlineArc to svg
    var outerPath = svg2.selectAll(".outlineArc")
        .data(pie(data))
        .enter().append("path")
        .attr("fill", "none")
        .attr("stroke", "gray")
        .attr("class", "outlineArc")
        .attr("d", outlineArc);

    // calculate the weighted mean HWBI score
    var score2 =
        data.reduce(function (a, b) {
            return a + ((b.score) * b.weight);
        }, 0) /
        data.reduce(function (a, b) {
            return a + b.weight;
        }, 0);

    //display HWBI score
    scoreText2 = svg2.append("svg:text")
        .attr("class", "scoreTex2")
        .attr("dy", ".35em")
        .attr("text-anchor", "middle")
        .attr("font-size", "35px")
        .style("font-weight", "bold")
        .text(Math.round(score2));

    //display word "HWBI" under the score value
    svg2.append("svg:text")
        .attr("dy", "1.95em")
        .attr("text-anchor", "middle")
        .attr("font-size", "15px")
        .style("font-weight", "bold")
        .text("HWBI");
}



//update pie chart function
function updatePie2Chart(error, data) {

    //use d3 to create the pie chart layout
    var pie = d3.layout.pie()
        .sort(null)
        .value(function (d) { return d.weight; });

    //hover over pie slice for label using d3 tooltip
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([50, 0])
        .style("pointer-events", "none")
        .html(function (d) {
            return d.data.description + ": <span style='color:orangered'>" + (d.data.score) + "</span>";
        });

    //call the hover tip utility
    svg2.call(tip);

    //use d3 to calculate size of arcs/angles
    var arc = d3.svg.arc()
        .innerRadius(innerRadius)
        .outerRadius(function (d) {
            return (radius - innerRadius) * (d.data.score/100) + innerRadius;
        });

    //use d3 to calculate size of outline arcs
    var outlineArc = d3.svg.arc()
        .innerRadius(innerRadius)
        .outerRadius(radius);

    //create variable path that appends a solidArc to the svg
    //"path" is any irregular SVG shape (pie slice)
    var path = svg2.selectAll(".solidArc")
        .data(pie(data))
         .transition()
         .duration(1500)
        //assign colors to solidArc slice based on domain name
        .attr("fill", (function (d) {
            if (d.data.description == "Connection To Nature") { return "#569c83"; }
            if (d.data.description == "Cultural Fulfillment") { return "#325481"; }
            if (d.data.description == "Education") { return "#5E4EA1"; }
            if (d.data.description == "Health") { return "#9E0041"; }
            if (d.data.description == "Leisure Time") { return "#E1514B"; }
            if (d.data.description == "Living Standards") { return "#FB9F59"; }
            if (d.data.description == "Safety And Security") { return "#FAE38C"; }
            if (d.data.description == "Social Cohesion") { return "#EAF195"; }
        }))
        .attr("class", "solidArc")
        .attr("stroke", "gray")
        .attr("d", arc)
        //.on('mouseover', tip.show)
        //.on('mouseout', tip.hide);

    //create variable outerPath that appends an outlineArc to svg
    var outerPath = svg2.selectAll(".outlineArc")
        .data(pie(data))
        .transition()
        .attr("fill", "none")
        .attr("stroke", "gray")
        .attr("class", "outlineArc")
        .attr("d", outlineArc);

    // calculate the weighted mean HWBI score
    var score2 =
        data.reduce(function (a, b) {
            return a + ((b.score) * b.weight);
        }, 0) /
        data.reduce(function (a, b) {
            return a + b.weight;
        }, 0)
    ;


    //display HWBI score
    d3.select("text.scoreTex2")
        .transition()
        .duration(3000)
        .text(Math.round(score2));
}
