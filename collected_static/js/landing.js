$( document ).ready(function() {
	$(function() {
        // $(".rslides").responsiveSlides();
        $(".rslides").responsiveSlides({
            auto: true,             // Boolean: Animate automatically, true or false
            speed: 3000,            // Integer: Speed of the transition, in milliseconds
            timeout: 6000,          // Integer: Time between slide transitions, in milliseconds
            pager: false,           // Boolean: Show pager, true or false
            nav: false,             // Boolean: Show navigation, true or false
            random: false,          // Boolean: Randomize the order of the slides, true or false
            pause: false,           // Boolean: Pause on hover, true or false
            pauseControls: true,    // Boolean: Pause when hovering controls, true or false
            prevText: "Previous",   // String: Text for the "previous" button
            nextText: "Next",       // String: Text for the "next" button
            maxwidth: "",           // Integer: Max-width of the slideshow, in pixels
            navContainer: "",       // Selector: Where controls should be appended to, default is after the 'ul'
            manualControls: "",     // Selector: Declare custom pager navigation
            namespace: "rslides",   // String: Change the default namespace used
            before: function(){},   // Function: Before callback
            after: function(){}     // Function: After callback
        });
    });
	$("ul li").hover(function() {
		var e = this;
		$(e).find("a").stop().animate({ marginTop: "-10px" }, 350, function() {
			$(e).find("a").animate({ marginTop: "-6px" }, 350);
		});
	},function(){
		var e = this;
		$(e).find("a").stop().animate({ marginTop: "4px" }, 250, function() {
			$(e).find("a").animate({ marginTop: "0px" }, 250);
		});
	});

	$("#eco").mousedown(function() {
		$(this).css( "box-shadow","inset 0 0 30px #CCC");
	});
	$("#eco").mouseup(function() {
		$(this).css( "box-shadow","none" );
	});
	$("#eco").mouseleave(function() {
		$(this).css( "box-shadow","none" );
	});

	$("#hh").mousedown(function() {
		$(this).css( "box-shadow","inset 0 0 30px #999");
	});
	$("#hh").mouseup(function() {
		$(this).css( "box-shadow","none" );
	});
	$("#hh").mouseleave(function() {
		$(this).css( "box-shadow","none" );
	});
	
	$("#pop").mousedown(function() {
		$(this).css( "box-shadow","inset 0 0 30px #888");
	});
	$("#pop").mouseup(function() {
		$(this).css( "box-shadow","none" );
	});
	$("#pop").mouseleave(function() {
		$(this).css( "box-shadow","none" );
	});
	
});

