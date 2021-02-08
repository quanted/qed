// Placeholder object for User changed values
var dragVal = {};

//import data from a json file and run drawSliders function onPageLoad
d3.json("/static_qed/hwbi/json/baseline.json", function (data) {
    dragVal = data.outputs;
    data.outputs.services.forEach(drawSliders);  // Call drawSliders() after parsing JSON, passing in "each" element
});


//draw sliders function
function drawSliders(data, index) {
    //append an svg to cirSlide div

    //set scale for slider. domain is input min max. range is slider translated min max (same)
    var x = d3.scale.linear()
        .domain((function () {
            if (data.name == "capitalInvestment") { return [56.31683197, 61.75389692]; }
            if (data.name == "consumption") { return [47.42882423, 54.04916975]; }
            if (data.name == "employment") { return [33.13814798, 72.57176231]; }
            if (data.name == "finance") { return [31.42250002, 61.56578545]; }
            if (data.name == "innovation") { return [25.89488723, 65.3289721]; }
            if (data.name == "production") { return [45.11697104, 51.67193166]; }
            if (data.name == "redistribution") { return [23.51316313, 68.92691912]; }
            if (data.name == "airQuality") { return [10, 90]; }
            if (data.name == "foodFiberAndFuel") { return [32.62908483, 48.49178319]; }
            if (data.name == "greenspace") { return [36.11207908, 62.03906984]; }
            if (data.name == "waterQuality") { return [15.95637509, 88.22033237]; }
            if (data.name == "waterQuantity") { return [21.70976841, 72.83447998]; }
            if (data.name == "activism") { return [25.85945275, 73.66346154]; }
            if (data.name == "communication") { return [33.10020486, 68.98955269]; }
            if (data.name == "communityAndFaith") { return [12.21375305,	90]; }
            if (data.name == "education") { return [33.24429069,	56.47803694]; }
            if (data.name == "emergencyPreparedness") { return [19.78920564, 76.07510118]; }
            if (data.name == "familyServices") { return [42.66833596, 73.35259094]; }
            if (data.name == "healthcare") { return [29.63020433, 62.25876617]; }
            if (data.name == "justice") { return [31.22560175, 71.78167536]; }
            if (data.name == "labor") { return [36.52332879, 53.29715035]; }
            if (data.name == "publicWorks") { return [33.53645478, 66.4893089]; }
        })()
    )
    .range([1, 99])
    //make scale *always* abide by range
    .clamp(true);

    var svgslide = d3.select("#cirSlide").append("svg")
        .attr("width", 155)
        .attr("height", 40);


    //append an empty group element to the svg for x axis slider bar
    svgslide.append("g")
        //set g element with attribute "x axis" (html attribute used for css styling)
        .attr("class", "x axis")
        //move g element over 25px to create margin
        .attr("transform", "translate(" + 10 + "," + 25 + ")")
        // introduce x-axis and give scale and no ticks
        .call(d3.svg.axis()
            .scale(x)
            .tickSize(0)
            .tickPadding(0))
        //select the axis domain (min max range)
        .select(".domain")
        //set axis with attribute halo to use as slider bar
        .attr("class", "halo");


    //append service name text to svg variables
    var name = svgslide.append("text")
        .text(function () {
            return data.description
        })
        .attr('y', 12)
        .attr('x', 10);

    //define brush attributes
    var brush = d3.svg.brush()
        //set scale of brush to match d3 calculated scale
        .x(x)
        //set the input value using imported data score value
        .extent([data.score, data.score])
        //set listener where on mousemove = function brushed
        .on("brush", brushed);

    //create a slider variable and append new g element
    var slider = svgslide.append("g")
        //give new g element class "slider"
        .attr("class", "slider")
        //call the brush variable attributes
        .call(brush)
        .attr("transform", "translate(" + 10 + "," + 0 + ")");

    //set the vertical range of slider background for selection/drag
    slider.select(".background")
        .attr("height", 100);

    //append handle to slider element
    var handle = slider.append("g")
        .attr("class", "handle"+index);

    //append circle to the slider handle
    handle.append("circle")
    //give the circle element class "handle"
    .attr("class", "handle")
    .attr("transform", "translate(0," + 25 + ")")
    .attr("r", 10)
    .attr("fill", (function () {
        if (data.serviceTypeName == "economic") { return "#b86361"; }
        if (data.serviceTypeName == "ecosystem") { return "#61b88e"; }
        if (data.serviceTypeName == "social") { return "#618bb8"; }
    }));

    //append text to the handle
    handle.append('text')
        .attr("class", "cirTex"+index)
        //assign text using data score and convert to whole number
        .text(data.score)
        .attr("transform", "translate(" + (-8) + " ," + 29 + ")");

    //for slider variable, call brush variable's "brushed" event property (mousemove)
    slider
        .call(brush.event)
        .attr("transform", "translate(" + 10 + "," + 0 + ")");

    //create brushed function
    function brushed() {
        //create variable based on brush extent (x value)
        var value = brush.extent()[0];
        //if the brush mousemove isn't a programmatic event... 
        if (d3.event.sourceEvent) {
            //...select the handle text
            handle.select('text');
            //set new value. constrain to domain value for x axis.
            //set value using mouse position relative to a specified container (0)
            value = x.invert(d3.mouse(this)[0]);
            //set brush extent to only use value (not a broad range)
            brush.extent([value, value]);
        }

        //move the starting handle to the value on x axis
        handle.attr("transform", "translate(" + x(value) + ",0)");
        //round text value down
        handle.select("text").text(Math.floor(value));
        
        dragVal.services[index].score = value;
    }
}


//POST request to calc endpoint
function useServiceValues() {

    var postData = {
        "scores" : {
            "capitalInvestment": dragVal.services[0].score,
            "consumption": dragVal.services[1].score,
            "employment": dragVal.services[2].score,
            "finance": dragVal.services[3].score,
            "innovation": dragVal.services[4].score,
            "production": dragVal.services[5].score,
            "redistribution": dragVal.services[6].score,
            "airQuality": dragVal.services[7].score,
            "foodFiberAndFuel": dragVal.services[8].score,
            "greenspace": dragVal.services[9].score,
            "waterQuality": dragVal.services[10].score,
            "waterQuantity": dragVal.services[11].score,
            "activism": dragVal.services[12].score,
            "communication": dragVal.services[13].score,
            "communityAndFaith": dragVal.services[14].score,
            "education": dragVal.services[15].score,
            "emergencyPreparedness": dragVal.services[16].score,
            "familyServices": dragVal.services[17].score,
            "healthcare": dragVal.services[18].score,
            "justice": dragVal.services[19].score,
            "labor": dragVal.services[20].score,
            "publicWorks": dragVal.services[21].score
        },
        "domainWeights" : {
            "connectionToNature": dragVal.domains[0].weight,
            "culturalFulfillment": dragVal.domains[1].weight,
            "education": dragVal.domains[2].weight,
            "health": dragVal.domains[3].weight,
            "leisureTime": dragVal.domains[4].weight,
            "livingStandards": dragVal.domains[5].weight,
            "safetyAndSecurity": dragVal.domains[6].weight,
            "socialCohesion": dragVal.domains[7].weight
        }
    };

    console.log(postData);

    $.post('https://qedinternal.epa.gov/hwbi/rest/calc/run',
        // 'https://134.67.114.8/hwbi/rest/hwbi/calc/run',   // old REST API url
        // '/hwbi/rest/hwbi/calc/run',                      // another old REST API url
        JSON.stringify(postData),                   // data (as JS object)
        function(data) {                            // success (callback) function
            $.unblockUI();
            updateDomainScores(data.outputs.domains);
            updateRIVWeights(dragVal.domains);
    },
    "json");                                        // data type returned from server
}





//function to update RIV domain weight values
function updateRIVWeights(domains) {
    $('#connectionToNature').val(domains[0].weight);
    $('#culturalFulfillment').val(domains[1].weight);
    $('#education').val(domains[2].weight);
    $('#health').val(domains[3].weight);
    $('#leisureTime').val(domains[4].weight);
    $('#livingStandards').val(domains[5].weight);
    $('#safetyAndSecurity').val(domains[6].weight);
    $('#socialCohesion').val(domains[7].weight);
}


//function to update services on county selection
function updateServiceScores(servicesScores) {
    dragVal.services = servicesScores;
    servicesScores.forEach(updateSliders);
}


//update sliders chart function
function updateSliders(data, index) {

    //set scale for slider. domain is input min max. range is slider translated min max (same)
    var x = d3.scale.linear()
        .domain((function () {
            if (data.name == "capitalInvestment") { return [56.31683197, 61.75389692]; }
            if (data.name == "consumption") { return [47.42882423, 54.04916975]; }
            if (data.name == "employment") { return [33.13814798, 72.57176231]; }
            if (data.name == "finance") { return [31.42250002, 61.56578545]; }
            if (data.name == "innovation") { return [25.89488723, 65.3289721]; }
            if (data.name == "production") { return [45.11697104, 51.67193166]; }
            if (data.name == "redistribution") { return [23.51316313, 68.92691912]; }
            if (data.name == "airQuality") { return [10, 90]; }
            if (data.name == "foodFiberAndFuel") { return [32.62908483, 48.49178319]; }
            if (data.name == "greenspace") { return [36.11207908, 62.03906984]; }
            if (data.name == "waterQuality") { return [15.95637509, 88.22033237]; }
            if (data.name == "waterQuantity") { return [21.70976841, 72.83447998]; }
            if (data.name == "activism") { return [25.85945275, 73.66346154]; }
            if (data.name == "communication") { return [33.10020486, 68.98955269]; }
            if (data.name == "communityAndFaith") { return [12.21375305,	90]; }
            if (data.name == "education") { return [33.24429069,	56.47803694]; }
            if (data.name == "emergencyPreparedness") { return [19.78920564, 76.07510118]; }
            if (data.name == "familyServices") { return [42.66833596, 73.35259094]; }
            if (data.name == "healthcare") { return [29.63020433, 62.25876617]; }
            if (data.name == "justice") { return [31.22560175, 71.78167536]; }
            if (data.name == "labor") { return [36.52332879, 53.29715035]; }
            if (data.name == "publicWorks") { return [33.53645478, 66.4893089]; }
        })()
    )
    .range([1, 99])
    //make scale *always* abide by range
    .clamp(true);

    //define brush attributes
    var brush = d3.svg.brush()
        //set scale of brush to match d3 calculated scale
        .x(x)
        //set the input value using imported data Score value
        .extent([data.score, data.score])
        //set listener where on mousemove = function brushed
        .on("brush", brushed);


    //select handle to slider element
    var handle = d3.select("g.handle" + index)


    //select circle to the slider handle
    d3.select("handle.circle")
        //give the circle element class "handle"
        .attr("class", "handle")
        .attr("transform", "translate(0," + 25 + ")")
        .attr("r", 10)
        .attr("fill", (function () {
            if (data.serviceTypeName == "economic") { return "#b86361"; }
            if (data.serviceTypeName == "ecosystem") { return "#61b88e"; }
            if (data.serviceTypeName == "social") { return "#618bb8"; }
        }));

    //select text to the handle
    d3.select("text.cirTex" + [index])
        //assign text using data score and convert to whole number
        .text(data.score)
        .attr("transform", "translate(" + (-8) + " ," + 29 + ")");

    //for slider variable, call brush variable's "brushed" event property (mousemove)
    d3.select("g.slider")
        .call(brush.event)
        .attr("transform", "translate(" + 10 + "," + 0 + ")");

    //create brushed function
    function brushed() {
        //create variable based on brush extent (x value)
        var value = brush.extent()[0];
        //if the brush mousemove isn't a programmatic event... 
        if (d3.event.sourceEvent) {
            //...select the handle text
            handle.select("text.cirTex" + [index]);
            //set new value. constrain to domain value for x axis.
            //set value using mouse position relative to a specified container (0)
            value = x.invert(d3.mouse(this)[0]);
            //set brush extent to only use value (not a broad range)
            brush.extent([value, value]);
         }

    //move the starting handle to the value on x axis
    handle.attr("transform", "translate(" + x(value) + ",0)")
        .transition()
        .duration(3000);
        //round text value down
    handle.select("text.cirTex"+[index]).text(Math.floor(value))
    }
}
