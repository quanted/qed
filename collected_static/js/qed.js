// Method to center a div on-screen
$.fn.center = function () {
	var cssTop = ( $(window).height() - this.height() ) / 2;
	var cssLeft = ( $(window).width() - this.width() ) / 2;
	this.css("top", (cssTop > 0 ? cssTop : 0) + "px");
	this.css("left", (cssLeft > 0 ? cssLeft : 0) + "px");
	return this;
};