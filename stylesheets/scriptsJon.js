$( document ).ready(function() {
	$('div#l_menu ul li a:not(aSelected)').bind('click', function(){
		$('div#l_menu ul li a.aSelected').removeClass('aSelected');
		$(this).addClass('aSelected');
	});

	$('.fadeDesc').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});

	$('.fadeInp').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});
	
	$('.fadeAlg').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});
	
	$('.fadeRef').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});
	
	$('.fadeQAQC').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});
	
	$('.fadeBat').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});

	$('.fadeOut').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});
	
});

var pathArray = window.location.pathname.split( '/' );
var pathLink = pathArray[1];
var pathSlice = pathLink.slice(0, -5);