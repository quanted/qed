$(document).ready(function() {

var doneDiv = document.getElementById("popup");

	$('#ajaxTest').click(function(){
		$(document).ajaxStart(function(){
			alert('Ajax Start');
		});

		$(document).ajaxStop(function(){
			alert('Ajax Stop');
			$("popup_ajaxTest").show();
		});

		$.ajax({

			type: "get",
			url: "/ajaxtest.html",
			data: $('#id_body_weight_of_bird').serialize(),
			dataType: "text",

		   success: function(data) {
        		alert('Ajax Done');

			}

		});

	});

});
