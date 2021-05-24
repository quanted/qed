$( document ).ready(function() {

	$("#landing_links ul li").hover(function() {
		var e = $(this).find("a");
    $(e).stop().animate({ marginTop: "-10px" }, 350, function() {
      $(e).animate({ marginTop: "-6px" }, 350);
    });
		},function(){
    var e = $(this).find("a");
    $(e).stop().animate({ marginTop: "4px" }, 250, function() {
      $(e).animate({ marginTop: "0px" }, 250);
    });
	});

	$("#eco").mousedown(function() {
		$(this).css( "box-shadow","inset 0 0 30px #222");
	});
	$("#eco").mouseup(function() {
		$(this).css( "box-shadow","none" );
	});
	$("#eco").mouseleave(function() {
		$(this).css( "box-shadow","3px 3px 15px #222" );
	});

	$("#hh").mousedown(function() {
		$(this).css( "box-shadow","inset 0 0 30px #999");
	});
	$("#hh").mouseup(function() {
		$(this).css( "box-shadow","none" );
	});
	$("#hh").mouseleave(function() {
		$(this).css( "box-shadow","3px 3px 15px #222" );
	});

	$("#cts").mousedown(function() {
		$(this).css( "box-shadow","inset 0 0 30px #888");
	});
	$("#cts").mouseup(function() {
		$(this).css( "box-shadow","none" );
	});
	$("#cts").mouseleave(function() {
		$(this).css( "box-shadow","3px 3px 15px #222" );
	});
	
});

