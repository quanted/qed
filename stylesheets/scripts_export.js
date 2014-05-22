var doneDiv = document.getElementById("popup");

$(document).ready(function () {
// var doneDiv = $('#popup');
var jq_html = $('<div />').append($("div.articles_output").children('table[class*=out_], div[class*=out_], H3[class*=out_], H4[class*=out_]:not(div#chart1,table:hidden)').clone()).html();
var n_plot_1 = $('div[id^="chart"]').size();
var n_plot_2 = $('img[id^="chart"]').size();
n_plot = n_plot_1 + n_plot_2

// console.log(n_plot);

i=1;

var imgData = [];
var options = {
    x_offset : 30,
    y_offset : 30
};

while(i <= n_plot){
	try{
    imgData.push($('#chart'+i).jqplotToImageStr(options));
    i=i+1    
    // console.log('a')

    }
    catch(e){
	imgData.push($('#chart'+i).attr('src'));
    i=i+1    
    // console.log('b')
    }
}


imgData_json = JSON.stringify(imgData)
// console.log(imgData_json);

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

    $('#pdfExport').click(function () {
		$(document).ajaxStart(function(){
			$.blockUI({
				css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "60px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
				message: '<h2 class="popup_header">Generating PDF Document...</h2><br><img src="/images/loader.gif" style="margin-top:-16px">',
				fadeIn:  500
			});
		});

        $(document).ajaxStop(function(){
	        // $.blockUI( { message: null, fadeIn: 0 } );
	        $("#export_link,.exit_button").fadeIn(500);
	        $("#popup_link").css({ "top":""+wintop+"", "left":""+winleft+"" });
	        $(".exit_button").click(function (){
	        	$("#popup").hide();
	        	$.unblockUI();
	        });
		});
        eror_msg = '<div id="popup_link"><img src="/images/export/exit_button.png" class="exit_button"><h2 class="popup_header">Something Went Wrong</h2></div>' 

		$.ajax({
			type: "POST",
			url: "/pdf.html",
			data: $("#pdf_post").serialize(),
			dataType: "html",
		    success: function(data) {
		    	$("#popup").show();
            	doneDiv.innerHTML = data;
            	// alert(data);
            	// console.log(data)
			},
			error: function() { 
		    	$("#popup").show();
            	doneDiv.innerHTML = eror_msg;
	        }   
		});
	});

	$('#htmlExport').click(function () {
		$(document).ajaxStart(function(){
			$.blockUI({
				css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "60px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
				message: '<h2 class="popup_header">Generating HTML Document...</h2><br><img src="/images/loader.gif" style="margin-top:-16px">',
				fadeIn:  500
			});
		});

        $(document).ajaxStop(function(){
	        $.blockUI( { message: null, fadeIn: 0 } );
	        $("#popup").show();
	        $("#export_link,.exit_button").fadeIn(500);
	        $("#popup_link").css({ "top":""+wintop+"", "left":""+winleft+"" });
	        $(".exit_button").click(function (){
	        	$("#popup").hide();
	        	$.unblockUI();
	        });

		});

		$.ajax({
				type: "post",
				url: "/html.html",
				data: $("#pdf_post").serialize(),
				dataType: "html",
			    success: function(data) {
		    		$("#popup").show();
            		doneDiv.innerHTML = data;
				},
				error: function() { 
			    	$("#popup").show();
	            	doneDiv.innerHTML = eror_msg;
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

	// $('#fadeExport_doc').append('<span class="hover"></span>').each(function () {
	// 	var $span = $('> span.hover', this).css('opacity', 0);
	// 	$(this).hover(function () {
	// 		$span.stop().fadeTo(500, 1);
	// 	}, function () {
	// 		$span.stop().fadeTo(500, 0);
	// 	});
	// });

});

