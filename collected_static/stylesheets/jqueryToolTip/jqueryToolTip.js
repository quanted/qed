(function($){
	$.fn.jqueryToolTip = function(toolTipOptions){
	
		// default settings for the plugin
		var toolTipDefaults = {
			position:"bottom"
		},
		
		// extending default settings
		toolTipSettings = $.extend({}, toolTipDefaults, toolTipOptions);
		
		// html markup for tooltip plugin
		var toolTipTemplate = '<div id="jqueryToolTip_wrapper"><span class="jqueryToolTip_text"></span><span class="jqueryToolTip_arrow"></span></div><!-- end jqueryToolTip -->';
		
		// appending the markup
		$('body').append(toolTipTemplate);

		$(this).each(function(){
			// on hover function
			$(this).hover(function(){
				var toolTipTitle = $(this).attr("title"); // getting current link title
				$(this).attr("title","");
				var toTop = $(this).offset().top; // getting current link Y axis
				var toLeft = $(this).offset().left; // getting current link X axis
				var toolTipHeight = $('#jqueryToolTip_wrapper').css("height"); // getting toolTip Height
				var itemHeight = $(this).css("height"); // getting link Height
				
				if(toolTipSettings.position == 'top')
				{
					$('#jqueryToolTip_wrapper').find('.jqueryToolTip_arrow').addClass('arrow_down');
					var topFinal = parseInt(toTop) - parseInt(toolTipHeight) - 10;
				}
				else
				{
					$('#jqueryToolTip_wrapper').find('.jqueryToolTip_arrow').removeClass('arrow_down');
					var topFinal = parseInt(toTop) + parseInt(itemHeight) + 10;
				}

				$('.jqueryToolTip_text').html(toolTipTitle); // changing tooltip text to current link title
				$('#jqueryToolTip_wrapper').css("display","block"); // setting tooltip display to block
				$('#jqueryToolTip_wrapper').css({   // setting tooltip left and top position to the current link position
					top: topFinal,
					left: toLeft
				});
			},function(){
				$('#jqueryToolTip_wrapper').css("display","none");  // hiding tooltip after hover is done
				$(this).attr("title",$('.jqueryToolTip_text').html());
			});
		});
}
})(jQuery);
