var width = 960,
    height = 600;

//d3.select("").style("height", height + "px");

var projection = d3.geo.albersUsa()
    .scale(1100)
    .translate([width / 2, height / 2]);

var path = d3.geo.path()
    .projection(projection);

var svg = d3.select("#map-container").append("svg")
    .attr("width", width)
    .attr("height", height);

var g = svg.append("g");

g.append( "rect" )
  .attr("width",width)
  .attr("height",height)
  .attr("fill","white")
  .attr("opacity",0)
  .on("mouseover",function(){
    hoverData = null;
    if ( probe ) probe.style("display","none");
  })

var map = g.append("g")
    .attr("id","map");

var probe,
    hoverData;

var dateScale, sliderScale, slider;

var format = d3.format(",");

var months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    months_full = ["January","February","March","April","May","June","July","August","September","October","November","December"],
    orderedColumns = [],
    currentFrame = 0,
    interval,
    frameLength = 500,
    isPlaying = false;

var sliderMargin = 65;

function circleSize(d){
  return Math.sqrt( .0001 * Math.abs(d) );
};


d3.json("/static_qed/cyan/data/states.json", function(error, us) {
  map.selectAll("path")
      .data(topojson.feature(us, us.objects.states).features)
      .enter()
      .append("path")
      .attr("vector-effect","non-scaling-stroke")
      .attr("class","land")
      .attr("d", path);

   map.append("path")
       .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
       .attr("class", "state-boundary")
       .attr("vector-effect","non-scaling-stroke")
       .attr("d", path);

  probe = d3.select("#map-container").append("div")
    .attr("id","probe");

  d3.select("body")
    .append("div")
    .attr("id","loader")
    .style("top",d3.select("#play").node().offsetTop + "px")
    .style("height",d3.select("#date").node().offsetHeight + d3.select("#map-container").node().offsetHeight + "px")

  d3.csv("/static_qed/cyan/data/lakes_1431.csv",function(data){
    var first = data[0];
    // get columns
    for ( var mug in first ){
      if ( mug != "LAKE" && mug != "LAT" && mug != "LON" ){
        orderedColumns.push(mug);
      }
    }

    orderedColumns.sort( sortColumns );

    // draw city points 
    for ( var i in data ){
      var projected = projection([ parseFloat(data[i].LON), parseFloat(data[i].LAT) ])
      map.append("circle")
        .datum( data[i] )
        .attr("cx",projected[0])
        .attr("cy",projected[1])
        .attr("r",1)
        .attr("vector-effect","non-scaling-stroke")
        .on("mousemove",function(d){
          hoverData = d;
          setProbeContent(d);
          probe
            .style( {
              "display" : "block",
              "top" : (d3.event.pageY - 80) + "px",
              "left" : (d3.event.pageX + 10) + "px"
            })
        })
        .on("mouseout",function(){
          hoverData = null;
          probe.style("display","none");
        })
    }

    createLegend();

    dateScale = createDateScale(orderedColumns).range([0,500]);
    
    createSlider();

    d3.select("#play")
      .attr("title","Play animation")
      .on("click",function(){
        if ( !isPlaying ){
          isPlaying = true;
          d3.select(this).classed("pause",true).attr("title","Pause animation");
          animate();
        } else {
          isPlaying = false;
          d3.select(this).classed("pause",false).attr("title","Play animation");
          clearInterval( interval );
        }
      });

    drawMonth( orderedColumns[currentFrame] ); // initial map

    window.onresize = resize;
    resize();

    d3.select("#loader").remove();

  })

});

function drawMonth(m,tween){
  var circle = map.selectAll("circle")
    .sort(function(a,b){
      // catch nulls, and sort circles by size (smallest on top)
      if ( isNaN(a[m]) ) a[m] = 0;
      if ( isNaN(b[m]) ) b[m] = 0;
      return Math.abs(b[m]) - Math.abs(a[m]);
    })
    .attr("class",function(d){
      return d[m] > 0 ? "gain" : "loss";
    })
  if ( tween ){
    circle
      .transition()
      .ease("linear")
      .duration(frameLength)
      .attr("r",function(d){
        return circleSize(d[m])
      });
  } else {
    circle.attr("r",function(d){
      return circleSize(d[m])
    });
  }

  d3.select("#date p#month").html( monthLabel(m) );

  if (hoverData){
    setProbeContent(hoverData);
  }
}

function animate(){
  interval = setInterval( function(){
    currentFrame++;

    if ( currentFrame == orderedColumns.length ) currentFrame = 0;

    d3.select("#slider-div .d3-slider-handle")
      .style("left", 100*currentFrame/orderedColumns.length + "%" );
    slider.value(currentFrame)

    drawMonth( orderedColumns[ currentFrame ], true );

    if ( currentFrame == orderedColumns.length - 1 ){
      isPlaying = false;
      d3.select("#play").classed("pause",false).attr("title","Play animation");
      clearInterval( interval );
      return;
    }

  },frameLength);
}

function createSlider(){

  sliderScale = d3.scale.linear().domain([0,orderedColumns.length-1]);

  var val = slider ? slider.value() : 0;

  slider = d3.slider()
    .scale( sliderScale )
    .on("slide",function(event,value){
      if ( isPlaying ){
        clearInterval(interval);
      }
      currentFrame = value;
      drawMonth( orderedColumns[value], d3.event.type != "drag" );
    })
    .on("slideend",function(){
      if ( isPlaying ) animate();
      d3.select("#slider-div").on("mousemove",sliderProbe)
    })
    .on("slidestart",function(){
      d3.select("#slider-div").on("mousemove",null)
    })
    .value(val);

  d3.select("#slider-div").remove();

  d3.select("#slider-container")
    .append("div")
    .attr("id","slider-div")
    .style("width",dateScale.range()[1] + "px")
    // .on("mousemove",sliderProbe)
    // .on("mouseout",function(){
    //   d3.select("#slider-probe").style("display","none");
    // })
    .call( slider );

  d3.select("#slider-div a").on("mousemove",function(){
    d3.event.stopPropagation();
  })

  var sliderAxis = d3.svg.axis()
    // .scale( dateScale )
    // .tickValues( dateScale.ticks(orderedColumns.length).filter(function(d,i){
    //   // ticks only for beginning of each year, plus first and last
    //   return d.getMonth() == 0 || i == 0 || i == orderedColumns.length-1;
    // }))
    // .tickFormat(function(d){
    //   // abbreviated year for most, full month/year for the ends
    //   if ( d.getMonth() == 0 ) return "'" + d.getFullYear().toString().substr(2);
    //   return months[d.getMonth()] + " " + d.getFullYear();
    // })
    // .tickSize(10)

  d3.select("#axis").remove();

  d3.select("#slider-container")
    .append("svg")
    .attr("id","axis")
    .attr("width",dateScale.range()[1] + sliderMargin*2 )
    .attr("height",25)
    .append("g")
      .attr("transform","translate(" + (sliderMargin+1) + ",0)")
      // .call(sliderAxis);

  d3.select("#axis > g g:first-child text").attr("text-anchor","end").style("text-anchor","end");
  d3.select("#axis > g g:last-of-type text").attr("text-anchor","start").style("text-anchor","start");
}

function createLegend(){
  var legend = g.append("g").attr("id","legend").attr("transform","translate(560,10)");

  // legend.append("circle").attr("class","gain").attr("r",5).attr("cx",-167).attr("cy",9)

  // legend.append("text").text("Monthly max cyanobacteria concentration").attr("x",-160).attr("y",13);

format = d3.format("0,000")

  var sizes = [ 100000, 1000000  ]; //pulled out the 250000
  for ( var i in sizes ){
    legend.append("circle")
      .attr("class","gain")
      .attr( "r", circleSize( sizes[i] ) )
      .attr( "cx", 80 + circleSize( sizes[sizes.length-1] ) )
      .attr( "cy", 2.5 * circleSize( sizes[sizes.length-1] ) - 2.5 * (circleSize( sizes[i] )) )
      .attr("vector-effect","non-scaling-stroke");
    legend.append("text")
      .text( (format(sizes[i] / 1)) + " cells/ml" + (i == sizes.length-1 ? "" : "") )
      .attr( "text-anchor", "middle" )
      .attr( "x", 142 + circleSize( sizes[sizes.length-1] ) )
      .attr( "y", 2 * ( circleSize( sizes[sizes.length-1] ) - circleSize( sizes[i] ) ) - 7.5 )
      .attr( "dy", 13)
  }
}

function setProbeContent(d){
  var val = d[ orderedColumns[ currentFrame ] ],
      m_y = getMonthYear( orderedColumns[ currentFrame ] ),
      month = months_full[ months.indexOf(m_y[0]) ];
  var html = "<strong>" + d.LAKE + "</strong><br/>" +
            format( Math.abs( val ) ) + "  " + ( val < 0 ? "lost" : " km² HAB" ) + "<br/>" +
            "<span>" + month + " " + m_y[1] + "</span>";
  probe
    .html( html );
}

function sliderProbe(){
  var d = dateScale.invert( ( d3.mouse(this)[0] ) );
  // d3.select("#slider-probe")
  //   .style( "left", d3.mouse(this)[0] + sliderMargin + "px" )
  //   .style("display","block")
  //   .select("p")
  //   .html( months[d.getMonth()] + " " + d.getFullYear() )
}

function resize(){
  var w = d3.select("#container").node().offsetWidth,
      h = window.innerHeight - 80;
  var scale = Math.max( 1, Math.min( w/width, h/height ) );
  svg
    .attr("width",width*scale)
    .attr("height",height*scale);
  g.attr("transform","scale(" + scale + "," + scale + ")");

  d3.select("#map-container").style("width",width*scale + "px");

  dateScale.range([0,500 + w-width]);
  
  createSlider();
}

function sortColumns(a,b){
  // [month,year]
  var monthA = a.split("-"),
      monthB = b.split("-");
  // Y2K !!!
  // 99 becomes 9; 2000+ becomes 11+
  if ( monthA[1] < 90 ) monthA[1] = parseInt(monthA[1]) + 11;
  else monthA[1] = parseInt(monthA[1]) - 90;
  if ( monthB[1] < 90 ) monthB[1] = parseInt(monthB[1]) + 11;
  else monthB[1] = parseInt(monthB[1]) - 90;

  // turn year+month into a sortable number
  return ( 100*parseInt(monthA[1]) + months.indexOf(monthA[0]) ) - ( 100*parseInt(monthB[1]) + months.indexOf(monthB[0]) );
}

function createDateScale( columns ){
  var start = getMonthYear( columns[0] ),
      end = getMonthYear( columns[ columns.length-1 ] );
  return d3.time.scale()
    .domain( [ new Date( start[1], months.indexOf( start[0] ) ), new Date( end[1], months.indexOf( end[0] ) ) ] );
}

function getMonthYear(column){
  var m_y = column.split("-");
  var year = parseInt( m_y[1] );
  if ( year > 90 ) year += 1900;
  else year += 2000;
  return [ m_y[0], year ];
}

function monthLabel( m ){
  var m_y = getMonthYear(m);
  return "<span>" + m_y[0].toUpperCase() + "</span> " + m_y[1];
}