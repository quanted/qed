// jQuery
$(document).ready(function() {
	// Home
	$('#home').hover(
		function() {
		    $('#home_text').stop().animate({width: '3.5em' }, {duration: 500, queue: false}).fadeTo(500,1);
		},
		function () {
		    $('#home_text').stop().animate({width:0}, {duration: 500, queue: false}).fadeTo(500,0);
		}
		).mousedown(function() {
			$(this).addClass('textshadow');
		}).mouseup(function() {
			$(this).removeClass('textshadow');
		}).mouseleave(function() {
			$(this).removeClass('textshadow');
	});
	// About
	$('#about').hover(
		function() {
		    $('#about_text').stop().animate({width: '3.5em' }, {duration: 500, queue: false}).fadeTo(500,1);
		},
		function () {
		    $('#about_text').stop().animate({width:0}, {duration: 500, queue: false}).fadeTo(500,0);
		}
	);
	$('.articles a').hover(function(){
		$(this).stop().animate({ color:'#A31E39' },500);
	}, function(){
		$(this).stop().animate({ color:'#485C5A' },500);
	});
	$('#l_menu a, .logreg').click(function(e) {
		e.preventDefault();
		var destination = $(this).attr('href');
		setTimeout(function() { window.location.href = destination; }, 500);
		$('#topheader_pic_main, #topheader_p_main').animate({
				height:'120px'
		}, 500);
		$('#topheader_p_main p, .logreg').fadeOut(500);
	});
});