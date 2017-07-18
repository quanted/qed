$( document ).ready(function() { 
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

