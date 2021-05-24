$(document).ready(function () {

	function parseOutput(file_type) {
		
        var elements, jq_html, imgData_json, n_plot;
        var workflow = getWorkflow(); // get current workflow name
        var options = { x_offset : 30, y_offset : 30 }; // jqplotToImage options
        var imgData = []; // jqplot images
        var jsonData = ""; // json data string (originally intended for metabolites)

        elements = collectDOM(workflow); // get relevant dom objects

        if (file_type == "pdf" || file_type == "html") {
       		if (workflow == "chemspec") {
	            try {
	                imgData.push($('#microspecies-distribution').jqplotToImageStr(options));
	                imgData.push($('#isoelectric-point').jqplotToImageStr(options));
	            }
	            catch(e) { console.log(e); }
	        }
	        else if (workflow == "gentrans") {
	            var nodeArray = buildMetabolitesArray(); // (cts_gentrans_tree)
	            jsonData = JSON.stringify(nodeArray); // spacetree data (cts_gentrans_tree)
	        }
			jq_html = $('<div />').append($(elements).clone()).html();
			var n_plot_1 = $('#microspecies-distribution').size();
			var n_plot_2 = $('#isoelectric-point').size();
			n_plot = n_plot_1 + n_plot_2;
			imgData_json = JSON.stringify(imgData, null, '\t');
        }

        else if (file_type == "csv") {
        	var json_obj = {};
        	if (workflow == "pchemprop") {
        		// todo: loop props, then calcs so the csv can be ordered by props
        		for (var calc in checkedCalcsAndProps) {
        			if (checkedCalcsAndProps.hasOwnProperty(calc)) {

        				json_obj[calc] = {};

        				for (var i = 0; i < checkedCalcsAndProps[calc].length; i++) {
        					// looping props of calc..
        					var calc_prop = checkedCalcsAndProps[calc][i];
							var data = $('.' + calc + '.' + calc_prop).html(); // get data from corresponding cell
							if (calc_prop == "ion_con") {
								data = pickOutPka(data);
							}
							if (data != null) {
								json_obj[calc][calc_prop] = data;
							}
        				}
        			}
        		}
        	}
        	else if (workflow == "gentrans") {
        		json_obj = buildMetabolitesArray();
        	}
        	console.log(json_obj);
        	jsonData = { "run_data": JSON.parse(sessionStorage.getItem("run_data")) };
        	// jsonData = JSON.stringify(jsonData);
        	return jsonData;
        }

        else { return; }

        // appendToRequestTable(jq_html, n_plot, imgData_json, jsonData); // append elements to request table

	}

	$('#pdfExport').click(function () {
		parseOutput('pdf');
		$('form').attr({'action': 'pdf', 'method': 'POST'}).submit();
	});

	$('#htmlExport').click(function () {
		parseOutput('html');
		$('form').attr({'action': 'html', 'method': 'POST'}).submit();
	});

	$('#csvExport').click(function () {
        var jsonData = parseOutput('csv');
       	// $('form').attr({'action': 'csv', 'method': 'POST'}).submit();
       	$.ajax({
            url: "/cts/chemspec/csv",
            type: "POST",
            dataType: "json",
            data: jsonData,
            success: function (data) {

            },
            error: function (jqXHR, textStatus, errorThrown) {
            	alert("Error creating CSV file");
            }
        });
	});


	$('#fadeExport_pdf').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});
	
	$('#fadeExport_html').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});

	$('#fadeExport_csv').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});

});


function buildMetabolitesArray() {
	// calls cts_gentrans_tree function getSpaceTree()
	var canvasNodes = getSpaceTree().graph.nodes;
    var nodeArray = [];
    for (var node in canvasNodes) {
        if (canvasNodes.hasOwnProperty(node)) {
            // var nodeItem = {
            //     'image': canvasNodes[node]['name'],
            //     'data': canvasNodes[node]['data']
            // };
            var nodeItem = canvasNodes[node]['data']
            nodeArray.push(nodeItem);
        }
    }
    return nodeArray;
}


function appendToRequestTable(jq_html, n_plot, imgData_json, jsonData) {
	
	var test = $('table.getpdf');

	$('table.getpdf').html("");
	
	$('<tr style="display:none"><td><input type="hidden" name="pdf_t"></td></tr>')
		.appendTo('.getpdf')
		.find('input')
		.val(jq_html);

	$('<tr style="display:none"><td><input type="hidden" name="pdf_nop"></td></tr>')
		.appendTo('.getpdf')
		.find('input')
		.val(n_plot);

	$('<tr style="display:none"><td><input type="hidden" name="pdf_p"></td></tr>')
		.appendTo('.getpdf')
		.find('input')
		.val(imgData_json);

    $('<tr style="display:none"><td><input type="hidden" name="pdf_json"></td></tr>')
		.appendTo('.getpdf')
		.find('input')
		.val(jsonData);
}


function collectDOM(workflow) {
	switch(workflow) {
		case "chemspec":
			elements = $("div.articles_output").children('h2[class="model_header"], div#timestamp, h3#userInputs');
	        elements = elements.add('table#inputsTable'); // user inputs
	        elements = elements.add('h4#pka, dl#pkaValues'); // pKa values
	        var parentTitle = $('table#msMain td:first h4');
	        var parentImage = $('#parent_div img'); // parent species
	        var parentTable = $('#parent_div table');
	        elements = elements.add(parentTitle).add(parentImage).add(parentTable);
	        var ms = $('table#msMain td#ms-cell').children().not($('div.chemspec_molecule'));
	        elements = elements.add(ms);
	        var majorMS = $('h4#majorMS, #majorMS_div img, #majorMS_div table');
	        elements = elements.add(majorMS);
	        var taut = $('h4#taut, p.taut-percent, #taut_div img, #taut_div table');
	        elements = elements.add(taut);
	        var stereo = $('h4#stereo, #stereo_div img, #stereo_div table');
	        elements = elements.add(stereo);
	        return elements;
	    case "pchemprop":
	    	elements = $('div.articles_output').children().not(':hidden, div#export_menu');
	    	return elements;
	   	case "gentrans":
	   		elements = $("div.articles_output").children('h2[class="model_header"], div#timestamp, h3#userInputs');
	        elements = elements.add('table#inputsTable'); // user inputs
	        elements = elements.add('h3#reactionPathways');
	        return elements;
	    default:
	    	elements = null;
	    	return elements;
	}
}


function getWorkflow() {
	var path = window.location.href;
	if (path.indexOf("chemspec") > -1) {
		return "chemspec";
	}
	else if (path.indexOf("pchemprop") > -1) {
		return "pchemprop";
	}
	else if (path.indexOf("gentrans") > -1) {
		return "gentrans";		
	}
	else { return null; }
}


function pickOutPka(html_string) {
	var pka_obj = {};
	var pkas = $.parseHTML(html_string);
	var pka_string = "";
	$(pkas).each(function () {
		var key_val_array = $(this).text().split(': '); // "pka0: 1.23"
		pka_obj[key_val_array[0]] = key_val_array[1];
	});
	return pka_obj;
}