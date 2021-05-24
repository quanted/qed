var doneDiv = document.getElementById("popup");

$(document).ready(function () {

	function parseOutput() {
		// var doneDiv = $('#popup');
		var jq_html = $('<div />').append($("div.articles_output").children('table[class*=out_], div[class*=out_], H3[class*=out_], H4[class*=out_]:not(div#chart1,table:hidden)').clone()).html();
		var n_plot_1 = $('div[id^="chart"]').size();
		var n_plot_2 = $('img[id^="chart"]').size();
		var n_plot = n_plot_1 + n_plot_2;

		console.log(n_plot);

		var i=1;

		var imgData = [];
		var options = {
			x_offset : 30,
			y_offset : 30
		};

		while(i <= n_plot){
			try {
				imgData.push($('#chart'+i).jqplotToImageStr(options));
				i++;
				// console.log('a')
			}
			catch(e){
				imgData.push($('#chart'+i).attr('src'));
				i++;
				// console.log('b')
			}
		}

		var imgData_json = JSON.stringify(imgData, null, '\t');
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

	}

	$('#pdfExport').click(function () {
		parseOutput();
		$('form').attr('action', 'pdf').submit();
	});

	$('#htmlExport').click(function () {
		parseOutput();
		$('form').attr('action', 'html').submit();
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