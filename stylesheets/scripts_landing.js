$( document ).ready(function() { 
	$("#row1 div").hover(function() {
		$(this).stop().animate({ top: "38px" }, 350, function() {
			$(this).animate({ top: "42px" }, 350);
		});
	},function(){
		$(this).stop().animate({ top: "52px" }, 250, function() {
			$(this).animate({ top: "48px" }, 250);
		});
	});

	$("#row2 div").hover(function() {
		$(this).stop().animate({ top: "390px" }, 350, function() {
			$(this).animate({ top: "394px" }, 350);
		});
	},function(){
		$(this).stop().animate({ top: "404px" }, 250, function() {
			$(this).animate({ top: "400px" }, 250);
		});
	});
	
	$("#eco, #hh, #d4em, #cts").mousedown(function() {
		$(this).css( "box-shadow","inset 0 0 30px #CCC");
	});
	$("#eco, #hh, #d4em, #cts").mouseup(function() {
		$(this).css( "box-shadow","none" );
	});
	$("#eco, #hh, #d4em, #cts").mouseleave(function() {
		$(this).css( "box-shadow","none" );
	});
	
	$("#pop, #unter").mousedown(function() {
		$(this).css( "box-shadow","inset 0 0 30px #888");
	});
	$("#pop, #unter").mouseup(function() {
		$(this).css( "box-shadow","none" );
	});
	$("#pop, #unter").mouseleave(function() {
		$(this).css( "box-shadow","none" );
	});
	
});

