(
function($){
	$.fn.shuffle = function() {
		return this.each(function(){
			var items = $(this).children();

			return (items.length)
				? $(this).html($.shuffle(items,$(this)))
			: this;
		});
	}
//                $.fn.validate_1 = function() {
//                    var res = false;
//                    this.each(function(){
//                        var arr = $(this).children();
//                        res = 	((arr[0].innerHTML=="1")&&
//                            (arr[1].innerHTML=="2")&&
//                            (arr[2].innerHTML=="3")&&
//                            (arr[3].innerHTML=="4")&&
//                            (arr[4].innerHTML=="5")&&
//                            (arr[5].innerHTML=="6")); 	
//							
//						res1 =arr.text()
//
//                    });
//                    return [res, res1];
//
//                }
	$.shuffle = function(arr,obj) {
		for(
		var j, x, i = arr.length; i;
		j = parseInt(Math.random() * i),
		x = arr[--i], arr[i] = arr[j], arr[j] = x
	);
		if(arr[0].innerHTML=="1") obj.html($.shuffle(arr,obj))
		else return arr;
	}
})(jQuery);