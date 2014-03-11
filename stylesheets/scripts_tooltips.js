$(document).ready(function() {

	var testHeight = $("div[class^='articles']").outerHeight();
	$('.right_tt').css( "height", testHeight );
	
	var focusHolder = null, ttId;
	$('table textarea, table input, table select').hover(function() {
		ttId = "#"+$(this).attr('id').slice(3);
		// Check if input has tt
		if ( $('div.right_tt_placeholder').find($(ttId)).length !== 0 ) {
			if (focusHolder == null) {
				$('.tooltips').html($(ttId).clone());
				var ttPosition = $(this).position();
				$('.tooltips').css({
					top: (ttPosition.top - 196) + "px"
				}).stop(true).fadeTo(500, 1);
			}
		}
	}, function() {
		if (focusHolder == null) {
			$('.tooltips').stop(true).fadeTo(500, 0);
		}
	});
 
	$('table textarea, table input, table select').focus(function() {
		if (focusHolder !== $(this).attr('id')) {
			// Check if input has tt
			if ( $('div.right_tt_placeholder').find($(ttId)).length == 0 ) {
				$('.tooltips').hide();
			} // If input has tt
			else if (focusHolder == null) {
				$('.tooltips').html($(ttId).clone());
				var ttPosition = $(this).position();
				$('.tooltips').css({
					top: (ttPosition.top - 196) + "px"
				}).stop(true).fadeTo(500, 1);
			}
		}
		focusHolder = $(this).attr('id');
	});
	$('table textarea, table input, table select').focusout(function() {
		$('.tooltips').stop(true).fadeTo(500, 0);
		focusHolder = null;
	});

});