/**************************************************************
 * Simple tooltip which becomes visible above the item clicked
 *
 * Created on 2/7/12 -- SJC
 *
 * Ex css styling:
 *   .tip {
 *     width: 212px;
 *     overflow: hidden;
 *     display: none;
 *     position: absolute;
 *     z-index: 500;
 *   }
 *   .tipTop {background: transparent url(static/images/tipTop.png) no-repeat top; height:37px;}
 *   .tipMid {background: transparent url(static/images/tipMid.png) repeat-y; padding: 0 25px 0px 25px;}
 *   .tipBtm {background: transparent url(static/images/tipBtm.png) no-repeat bottom; height: 32px;}
 *
 *
 * Ex Use:
 *   $('.items').tooltip({}, function(el){
 *     return "data?ID=" + el.html()
 *   });
 *   Or with display options:
 *   $('#some_id').tooltip({speed: 100, delay: 50}, function(el){
 *     return "data?ID=" + el.html()
 *   });
 **************************************************************/

jQuery.noConflict();
(function($) {

	/*************************************************************************
	 * callback is expected to return the url to be used in the ajax request.
	 * The ajax request returned data will be used to populate the tooltip
	 *************************************************************************/
	$.fn.tooltip = function(options, tip_callback) {

		/* Setup the options for the tooltip that can be
		 accessed from outside the plugin              */
		var defaults = {
			speed : 200,
			delay : 0
		};

		var options = $.extend(defaults, options);

		var tip_func = tip_callback;

		/* Create a function that builds the tooltip
		 markup. Then, prepend the tooltip to the body */
		getTip = function() {
			var tTip = '<div class="tip">' + '<div class="tipTop">' + '<a class="hideTip" href="#"><img alt="close" src="/static/images/Button Close.png" border="0"></a>' + '<a class="add_ref" href="#"><img alt="add new reference" src="/static/images/Button Add.png" border="0"></a>' + '</div>' + '<div class="tipMid">' + '<div class="inner" />' + '</div>' + '<div class="tipBtm">' + '</div>' + '</div>';
			return tTip;
		}
		if ($(".tip").length < 1) {
			$("body").prepend(getTip());
		}

		/* Give each item with the class associated with
		 the plugin the ability to call the tooltip    */
		$(this).each(function() {

			var $this = $(this);
			var tip = $('.tip');
			var tipInner = $('.tip .tipMid .inner');

			/* Mouse over and out functions*/
			$this.unbind('click').click(function() {
				var url = $this.attr("href");

				$.ajax({
					type : "POST",
					url : url,
					//dataType: "html",
					success : function(data) {
						tip_func(data, tipInner);
						setTip($this.offset().top, $this.offset().left);
						setTipTimer();
					}
				});
				return false;
			});
			$('.hideTip').unbind('click').click(function() {
				stopTipTimer();
				tip.animate({
					"opacity" : "hide"
				}, defaults.speed);
				return false;
			});

			/* Delay the fade-in animation of the tooltip */
			setTipTimer = function() {
				$this.showTipTimer = setInterval("showTip()", defaults.delay);
			}
			stopTipTimer = function() {
				clearInterval($this.showTipTimer);
			}
			/* Position the tooltip relative to the class
			 associated with the tooltip                */
			setTip = function(top, left) {
				var topOffset = tip.height();
				var xTip = (left + 30)
				var yTip = (top - topOffset - 30)
				var visibleWidth = $(window).width();
				if (xTip > visibleWidth - tip.width())
					xTip = visibleWidth - tip.width();
				tip.css({
					'top' : yTip + "px",
					'left' : xTip + "px"
				});
			}
			/* This function stops the timer and creates the
			 fade-in animation                          */
			showTip = function() {
				stopTipTimer();
				tip.hide();
				tip.animate({
					"top" : "+=20px",
					"opacity" : "show"
				}, defaults.speed);
			}
		});
	};
})(jQuery);
