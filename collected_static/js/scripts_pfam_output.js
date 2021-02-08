$(document).ready(function(){
   	var noa_out = $.parseJSON($('#noa_out').text());
   	var mm_out = $.parseJSON($('#mm_out').attr('data-val'));
   	var dd_out = $.parseJSON($('#dd_out').attr('data-val'));
   	var ma_out = $.parseJSON($('#ma_out').attr('data-val'));
   	var sr_out = $.parseJSON($('#sr_out').attr('data-val'));
		var i=1;
		while (i <= noa_out){
	  // $('<tr><td>Application method</td><tr>').appendTo('.out_application');
    $('<tr><td width=50>App'+i+'</td><td width=50>'+mm_out[i-1]+'</td><td width=50>'+dd_out[i-1]+'</td><td width=50>'+ma_out[i-1]+'</td><td width=50>'+sr_out[i-1]+'</td></tr>').appendTo('.out_application');

		var i=i+1;
		}
		
   	var nof_out = $.parseJSON($('#nof_out').text());
   	var nod_out = $.parseJSON($('#nod_out').attr('data-val'));
   	var fl_out = $.parseJSON($('#fl_out').attr('data-val'));
   	var wl_out = $.parseJSON($('#wl_out').attr('data-val'));
   	var ml_out = $.parseJSON($('#ml_out').attr('data-val'));
   	var to_out = $.parseJSON($('#to_out').attr('data-val'));
		var k=1;
		while (k <= nof_out){
	  $('<tr><td width=50>Event'+k+'</td><td width=50>'+nod_out[k-1]+'</td><td width=50>'+fl_out[k-1]+'</td><td width=50>'+wl_out[k-1]+'</td><td width=50>'+ml_out[k-1]+'</td><td width=50>'+to_out[k-1]+'</td></tr>').appendTo('.out_floods');
		var k=k+1;
		}

    /////collect data for figures////////
    var x_date1 = $.parseJSON($('#x_date1').attr('data-val'));
    var x_re_v_f = $.parseJSON($('#x_re_v_f').attr('data-val'));
    var x_re_c_f = $.parseJSON($('#x_re_c_f').attr('data-val'));
    var x_date1_len=x_date1.length;
    var paired5 = [];
    var paired6 = [];
    // for (var i=0; i<=x_date1_len; i+=1){
    //     paired5.push([x_date1[i],x_re_v[i]]);
    //     paired6.push([x_date1[i],x_re_c[i]]);
    // }

    var x_date2 = $.parseJSON($('#x_date2').attr('data-val'));
    var x_water = $.parseJSON($('#x_water').attr('data-val'));
    var x_water_level = $.parseJSON($('#x_water_level').attr('data-val'));
    var x_ben_tot = $.parseJSON($('#x_ben_tot').attr('data-val'));
    var x_ben_por = $.parseJSON($('#x_ben_por').attr('data-val'));
    var x_date2_len=x_date2.length;
    var paired = [];
    var paired2 = [];
    var paired3 = [];
    var paired4 = [];
    for (var i=0; i<=x_date2_len; i+=1){
        paired.push([x_date2[i],x_water[i]]);
        paired2.push([x_date2[i],x_water_level[i]]);
        paired3.push([x_date2[i],x_ben_tot[i]]);
        paired4.push([x_date2[i],x_ben_por[i]]);
        paired5.push([x_date2[i],x_re_v_f[i]]);
        paired6.push([x_date2[i],x_re_c_f[i]]);
    }

    //Create time slider 1 for figure 1////
    var months = ["", "", "", "", "", "", "", "", "", "", "", ""];
    var date_low_bound_1 = x_date2[0].split("/");
    var date_up_bound_1 = x_date2[x_date2_len-1].split("/");

    $("#date_range_slider_1").dateRangeSlider({
      bounds: {
              min: new Date(date_low_bound_1[2], date_low_bound_1[0]-1, date_low_bound_1[1]), 
              max: new Date(date_up_bound_1[2], date_up_bound_1[0]-1, date_up_bound_1[1])
              },
       defaultValues: {
              min: new Date(date_low_bound_1[2], date_low_bound_1[0]-1, date_low_bound_1[1]), 
              max: new Date(date_up_bound_1[2], date_up_bound_1[0]-1, date_up_bound_1[1])
               },
      scales: [{
        first: function(value){ return value; },
        end: function(value) {return value; },
        next: function(value){
          var next = new Date(value);
          return new Date(next.setMonth(value.getMonth() + 1));
        },
        label: function(value){
          //return months[value.getMonth()];
        }
      }]
    });

    var values_min = $("#date_range_slider_1").dateRangeSlider("values").min;
    var values_max = $("#date_range_slider_1").dateRangeSlider("values").max;
    var range_interval = $("#display_interval_1").val();
    
    createplot1(paired, paired2, values_min, values_max, range_interval);
    createplot2(paired3, paired4, values_min, values_max, range_interval);
    createplot3(paired5, paired6, values_min, values_max, range_interval);


    $('#calc1').click(function () {
      var values_min = $("#date_range_slider_1").dateRangeSlider("values").min;
      var values_max = $("#date_range_slider_1").dateRangeSlider("values").max;
      var range_interval = $("#display_interval_1").val();

      var raw_min = String(values_min);
      var raw_min_s = raw_min.split(" ");
      var new_min_s = raw_min_s.slice(1,4);
      var mydate_min = $D(new_min_s.join(" "));

      var raw_max = String(values_max);
      var raw_max_s = raw_max.split(" ");
      var new_max_s = raw_max_s.slice(1,4);
      var mydate_max = $D(new_max_s.join(" "));

      var month_map_pool = [" 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", "11", "12"];
      var date_map_pool = [" 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"];

      var month_map_min = month_map_pool[mydate_min.getMonth()];
      var date_map_min = date_map_pool[mydate_min.getDate()-1];
      var str_min = month_map_min + '/' + date_map_min+ '/' + mydate_min.getFullYear();
      var mydate_min_ind = $.inArray(str_min, x_date2);

      var month_map_max = month_map_pool[mydate_max.getMonth()];
      var date_map_max = date_map_pool[mydate_max.getDate()-1];
      var str_max = month_map_max + '/' + date_map_max+ '/' + mydate_max.getFullYear();
      var mydate_max_ind = $.inArray(str_max, x_date2);

      //console.log(new_min_s, str_min, $.inArray(str_min, x_date2), str_max, $.inArray(str_max, x_date2))
      //console.log(x_date[0])
      //console.log(String(values_min))
      //console.log($.inArray(String(values_min), x_date))

      createplot1(paired.slice(mydate_min_ind, mydate_max_ind+1), paired2.slice(mydate_min_ind, mydate_max_ind+1), values_min, values_max, range_interval);
      createplot2(paired3.slice(mydate_min_ind, mydate_max_ind+1), paired4.slice(mydate_min_ind, mydate_max_ind+1), values_min, values_max, range_interval);
      createplot3(paired5.slice(mydate_min_ind, mydate_max_ind+1), paired6.slice(mydate_min_ind, mydate_max_ind+1), values_min, values_max, range_interval);
    });

    function createplot1(data1, data2, range_min, range_max, range_interval) {
  		$.jqplot.config.enablePlugins = true;
        $('#chart1').empty();
        $.jqplot('chart1', [data1, data2], {
            title: "Water Concentrations & Depth",
            seriesDefaults: {
                showMarker: false,
                pointLabels: {show: false}
            },
            series:[
                {label:'Water Concentrations'},
                {label:'Water Depth', yaxis:'y2axis'}
            ],
            axes: {
                xaxis: {
                    renderer:$.jqplot.DateAxisRenderer,
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                    tickOptions:{formatString:'%#m/%#d/%Y',
                                 angle: -30
                                },
                    min: range_min,
                    max: range_max,
                    //tickInterval: range_interval,//'3 month',
                    label: 'Date',
                    pad: 0
                },
                yaxis: {
                    label: 'Water Total (μg/L)',
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                    pad: 0
                },
                y2axis:{
                  label: 'Water Depth (m)',
                  labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                  tickOptions:{showGridline:false},
                  pad: 0
                },
            },
            legend: {
                show: true,
                location: 'ne',
                placement: 'inside',
                fontSize: '11px'
            }
        });
    }
    function createplot2(data1, data2, range_min, range_max, range_interval) {
      $.jqplot.config.enablePlugins = true;
        $('#chart2').empty();
        $.jqplot('chart2', [data1, data2], {
            title: "Benthic Total and Pore Concentrations",
            seriesDefaults: {
                showMarker: false,
                pointLabels: {show: false}
            },
            series:[
                {label:'Benthic Total'},
                {label:'Benthic Pore', yaxis:'y2axis'}
            ],
            axes: {
                xaxis: {
                    renderer:$.jqplot.DateAxisRenderer,
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                    tickOptions:{formatString:'%#m/%#d/%Y',
                                 angle: -30
                                },
                    min: range_min,
                    max: range_max,
                    //tickInterval: range_interval,//'3 month',
                    label: 'Date',
                    pad: 0
                },
                yaxis: {
                    label: 'Benthic Total Concentrations (μg/L)',
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                    pad: 0
                },
                y2axis:{
                  label: 'Benthic Pore Concentrations (μg/L)',
                  labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                  tickOptions:{showGridline:false},
                  pad: 0
                },
            },
            legend: {
                show: true,
                location: 'ne',
                placement: 'inside',
                fontSize: '11px'
            }
        });
    }
    function createplot3(data1, data2, range_min, range_max, range_interval) {
      $.jqplot.config.enablePlugins = true;
        $('#chart3').empty();
        $.jqplot('chart3', [data1, data2], {
            title: "Released Volumn and Concentrations",
            seriesDefaults: {
                showMarker: false,
                pointLabels: {show: false}
            },
            series:[
                {label:'Released Volumn'},
                {label:'Released Concentration', yaxis:'y2axis'}
            ],
            axes: {
                xaxis: {
                    renderer:$.jqplot.DateAxisRenderer,
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                    tickOptions:{formatString:'%#m/%#d/%Y',
                                 angle: -30
                                },
                    min: range_min,
                    max: range_max,
                    //tickInterval: range_interval,//'3 month',
                    label: 'Date',
                    pad: 0
                },
                yaxis: {
                    label: 'Released Volumn (m³)',
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                    pad: 0
                },
                y2axis:{
                  label: 'Released Concentration (μg/L)',
                  labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                  tickOptions:{showGridline:false},
                  pad: 0
                },
            },
            legend: {
                show: true,
                location: 'nw',
                placement: 'inside',
                fontSize: '11px'
            }
        });
    }
});