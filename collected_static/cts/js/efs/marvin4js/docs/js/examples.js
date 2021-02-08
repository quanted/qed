$(function() {

	if (serviceConfig && serviceConfig.contextPath !== '${baseUrl}') {
		var serviceUrl = serviceConfig.contextPath + serviceConfig.serviceLocation;
		$("#baseurl").val(serviceUrl);
	}

	var baseurl;
	$("#baseurl").on("keyup", function() {
		baseurl = $(this).val();

		$("input[data-baseurl]").each(function() {
			var self = $(this);
			var value = self.val();

			if (typeof self.data("original-value") == "undefined") {
				self.data("original-value", value);
			} else {
				value = self.data("original-value");
			}
			self.val(baseurl + value);
		});
	}).keyup();

	$("form").on("submit", function() {
		$("input[type='button']:first").click();
		return false;
	});


	var indentAmount = 4;


	$('.GET').on("click", function(evt) {
		evt.preventDefault();

		var form = $(this).parents("form");

		$.ajax({
			url: $.trim(encodeURI($(".url", form).val())),
			type: 'GET'
		}).done(function(response, status, xhr) {
			var resptext = JSON.stringify(response, null, indentAmount);
			$('.output', form).val(resptext);

			if ($('.result', form)[form.attr("id")]) {
				$('.result', form)[form.attr("id")](response);	
			}
		}).fail(function(response, status, xhr) {
			console.log(response);
		});
	});


	$('.POST').on("click", function(evt) {
		evt.preventDefault();

		var form = $(this).parents("form");

		var params = $('.params', form).val();

		$.ajax({
			url: $(".url", form).val(),
			type: 'POST',
			data: params,
			dataType: $(".output", form).is(".text") ? "text" : "json",
			contentType: 'application/json'
		}).done(function(response, status, xhr) {

			var resptext = JSON.stringify(response, null, indentAmount);
			$('.output', form).val(resptext);

			if ($('.result', form)[form.attr("id")]) {
				$('.result', form)[form.attr("id")](response);
			}
		})
		.fail(function(response, status, xhr) {
			$('.output', form).val(response.statusText);
		});
	});


	//get a molecule from the database
	$.fn.example1 = function(image) {
		$(this).html($("<div/>").css({
			width: image.width,
			height: image.height,
			background: "url(data:image/png;base64," + image.image + ")"
		}));
	};

	//display a search result
	$.fn.example2 = function(searchresults) {
		var image = searchresults.data[0].image;

		$(this).html($("<div/>").css({
			width: image.width,
			height: image.height,
			background: "url(data:image/png;base64," + image.image + ")"
		}));
	};

	//displaying calculation results
	$.fn.example3 = function(calcdata) {
		var image = calcdata.pKa.result.image;

		$(this).html($("<div/>").css({
			width: image.width,
			height: image.height,
		}).html(image.image));
	};

	//displaying a structure table
	$.fn.example4 = function(searchresults) {
		$(this).empty();
		var result = $("<table />").appendTo(this);


		searchresults.data.forEach(function(row, i) {

			//table head
			if (i == 0) {
				var head = '<tr>';
				for (prop in row) {
					head += '<th>' + prop + '</th>';
				}
				head += '</tr>';
				result.append(head);
			}


			var html = '<tr>';
			for (prop in row) {
				if (prop == 'image') {
					if (row[prop].type == 'svg') {
						html += '<td>' + row[prop].image + '</td>';
					} else {
						html += '<td><div style="width:' + row[prop].image.width + 'px; height:' + row[prop].image.height + 'px; background-image:url(' + row[prop].image +')"></div></td>';
					}
				} else {
					html += '<td>' + row[prop] + '</td>';
				}
			}
			html += '</tr>';
			result.append(html);
		});
	};


});