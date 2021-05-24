// Define size and radius of pie chart
var width = 300,
    height = 300,
    radius = (Math.min(width, height) / 2)-4,
    innerRadius = 0.3 * radius;


//import data from a json file and run drawPieChart function onPageLoad
d3.json('/static_qed/hwbi/json/baseline.json', function (error, data) {
    drawPieChart("", data.outputs.domains);
});

//create svg element in the page "#pie" div and append g to the SVG
var svg1 = d3.selectAll("#pie")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    //append another g element with class "slice" to svg
    svg1.append("g")
      .attr("class", "slice");


//create rivData variable to update Pie using RIV weights
var rivData;


//function to update pie data based on RIV weights
function useRIVWeights() {
        //create empty array to store domain weights
        var domainWeights = [];
        //get value of each RIV p input and store in array
        $('#riv p input').each(function (i, elem) {
            domainWeights.push(parseInt($(elem).val()))
        });

    //to populate rivData array, grab Domain Weights values iteratively
        var i = 0;

        rivData.forEach(function (domain) {
            domain.weight = domainWeights[i];
            i++;
        });


        //call function to draw pie chart taking updated rivData
        updatePieRivs("", rivData);
    }



//function to update pie data based on county scores
function updateDomainScores(domainScores) {
        updatePieChart("", domainScores);
    }



//draw pie chart on page load
function drawPieChart(error, data) {

        rivData = data; ////give rivData updated data


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
    svg1.call(tip);

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
    var path = svg1.selectAll(".solidArc")
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
    svg1.selectAll(".outlineArc")
        .data(pie(data))
        .enter().append("path")
        .attr("fill", "none")
        .attr("stroke", "gray")
        .attr("class", "outlineArc")
        .attr("d", outlineArc);

    // calculate the weighted mean HWBI score
    var score =
        data.reduce(function (a, b) {
            return a + ((b.score) * b.weight);
        }, 0) /
        data.reduce(function (a, b) {
            return a + b.weight;
        }, 0);

    //display HWBI score
    svg1.append("svg:text")
        .attr("class", "scoreTex")
        .attr("dy", ".35em")
        .attr("text-anchor", "middle")
        .attr("font-size", "35px")
        .style("font-weight", "bold")
        .text(Math.round(score));

    //display word "HWBI" under the score value
    svg1.append("svg:text")
        .attr("dy", "1.95em")
        .attr("text-anchor", "middle")
        .attr("font-size", "15px")
        .style("font-weight", "bold")
        .text("HWBI");
}




//update pie chart function
function updatePieChart(error, data) {
    rivData = data; //give rivData updated data

    //use d3 to create the pie chart layout     
    var pie = d3.layout.pie()
        .sort(null)
        .value(function (d) { return d.weight; });



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
    svg1.selectAll(".solidArc")
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
        .attr("d", arc);

    //create variable outerPath that appends an outlineArc to svg     
    svg1.selectAll(".outlineArc")
        .data(pie(data))
        .transition()
        .attr("fill", "none")
        .attr("stroke", "gray")
        .attr("class", "outlineArc")
        .attr("d", outlineArc);

    // calculate the weighted mean HWBI score
    var score =
        data.reduce(function (a, b) {
            return a + ((b.score) * b.weight);
        }, 0) /
        data.reduce(function (a, b) {
            return a + b.weight;
        }, 0)
    ;


    console.log(score);

    //display HWBI score
    d3.select("text.scoreTex")
        .transition()
        .duration(3000)
        .text(Math.round(score));
}



//update pie chart function
function updatePieRivs(error, data) {
    console.log(data);
    //use d3 to create the pie chart layout     
    var pie = d3.layout.pie()
        .sort(null)
        .value(function (d) { return d.weight; });



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
    svg1.selectAll(".solidArc")
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
        .attr("d", arc);


    //create variable outerPath that appends an outlineArc to svg     
    svg1.selectAll(".outlineArc")
        .data(pie(data))
        .transition()
        .attr("fill", "none")
        .attr("stroke", "gray")
        .attr("class", "outlineArc")
        .attr("d", outlineArc);

    // calculate the weighted mean HWBI score
    var score1 =
        data.reduce(function (a, b) {
            return a + ((b.score) * b.weight);
        }, 0) /
        data.reduce(function (a, b) {
            return a + b.weight;
        }, 0)
    ;
        console.log(score1);

    //display HWBI score
    d3.select("text.scoreTex")
        .transition()
        .duration(3000)
        .text(Math.round(score1));
}