// Handles data requests loading screens.
// A model request/response submission (e.g., chemspec and gentrans single mode)
// will have a spinning loader and nothing else, while the websocket calc data requests
// use a progress bar and a spinning loader.

var BlockInterface = {

	div_height = "300px",
	div_width = "450px",
	winleft = null,
	wintop = null,
	loader_img = '<img src="/static_qed/cts/images/loader.gif" style="margin-top:-16px" id="load_wheel">',
	cancel_button = '<input onclick="cancelRequest()" type="button" value="Cancel" id="btn-pchem-cancel">',
	div_message = '<div id="pchem_wait"><h2 class="popup_header">Retrieving data...</h2><br>' +
					BlockInterface.loader_img + '<br><br><div id="progressbar"></div><br>' +
					BlockInterface.cancel_button + '<br></div>',

	init: function () {

		_browserWidth = $(window).width()
		_browserHeight = $(window).height()
		CTSLoader.winleft = (_browserWidth / 2) - 220 + "px"
		CTSLoader.wintop = (_browserHeight / 2) - 30 + "px"

		if (block) {
	        $.blockUI({
	            css: {
	                "top": "" + CTSLoader.wintop + "",
	                "left": "" + CTSLoader.winleft + "",
	                "padding": "30px 20px",
	                "width": CTSLoader.div_width,
	                "height": CTSLoader.div_height,
	                "border": "0 none",
	                "border-radius": "4px",
	                "-webkit-border-radius": "4px",
	                "-moz-border-radius": "4px",
	                "box-shadow": "3px 3px 15px #333",
	                "-webkit-box-shadow": "3px 3px 15px #333",
	                "-moz-box-shadow": "3px 3px 15px #333"
	            },
	            message: BlockInterface.div_message,
	            fadeIn: 500
	        });
	    }
	    else {
	    	$.unblockUI();
	    }	

	}

}