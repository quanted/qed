$(document).ready(function() {

	uberNavTabs(
		["Chemical", "Applications", "CropLand", "WaterBody"],
		{   "isSubTabs":true,
			"Chemical":['.tab_Chemical0','.tab_Chemical1']  }
	);

	// Menu Nav
	function uberNavTabs( modelTabs, subTabs ) {
		var tab_pool = [], liTabArray = [], noOfTabs = modelTabs.length;
		// Create 'tab_' & 'li.' arrays
		for (var i=0;i<noOfTabs;i++) {
			var addTabText = ".tab_"+modelTabs[i];
			tab_pool.push(addTabText);
			var addTabText_li = 'li.'+modelTabs[i];
			liTabArray.push(addTabText_li);
		}
		
		// Setup tab defaults
		var uptab_pool = modelTabs;
		// var visible = $(".tab:visible").attr('class').split(" ")[1];
		var curr_ind = 0;
		$(".back, .submit, #metaDataToggle, #metaDataText").hide();

		// Click handler
		$('.input_nav ul li').click(function() {
			// Check if "li" element has class (ignores the input buttons)
			if ($(this).attr('class')) {
				var testClass = $(this).attr("class").split(' ')[0];

				console.log(testClass);

				curr_ind = $.inArray(testClass, modelTabs);

				console.log(curr_ind);
				console.log(liTabArray[curr_ind]);

				// Remove current tab from array;
				var liTabArrayMinusCurr = liTabArray.slice(0);
				liTabArrayMinusCurr.splice(curr_ind,1);

				console.log(liTabArrayMinusCurr);
				console.log(liTabArray);

				if (curr_ind == 0) {
					console.log('First');
					
					$(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
					$(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
					$('.tab:visible, .back, .submit, #metaDataToggle, #metaDataText').hide();
					$(tab_pool[curr_ind]+", .next").show();
					// Check if this tab has subTabs
					if ( subTabs.isSubTabs && subTabs.hasOwnProperty(testClass) ) {
						alert("If statement");
						$(subTabs[testClass].toString()).show();
					}
				}

				if ( curr_ind > 0 && curr_ind < (modelTabs.length-1) ) {
					console.log('Middle');

					$(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
					$(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
					$('.tab:visible, .submit, #metaDataToggle, #metaDataText').hide();
					$(tab_pool[curr_ind]+", .back, .next").show();
					// Check if this tab has subTabs
					if ( subTabs.isSubTabs && subTabs.hasOwnProperty(testClass) ) {
						alert("If statement");
						$(subTabs[testClass].toString()).show();
					}
				}

				if ( curr_ind == (modelTabs.length-1) ) {
					console.log('Last');

					$(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
					$(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
					$('.tab:visible, .next, #metaDataToggle, #metaDataText').hide();
					$(tab_pool[curr_ind]+", .back, .submit").show();
					// Check if this tab has subTabs
					if ( subTabs.isSubTabs && subTabs.hasOwnProperty(testClass) ) {
						alert("If statement");
						$(subTabs[testClass].toString()).show();
					}
				}
			}
		});

		$('.next').click(function () {
			var tab = $(".tab:visible");
			if (curr_ind < (modelTabs.length-1)) {
				$(tab).hide();
				$("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
				curr_ind = curr_ind + 1;
				$(tab_pool[curr_ind]).show();
				$("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
				$(".submit, #metaDataToggle, #metaDataText").hide();
				$(".back").show();
				// Check if this tab has subTabs
				if ( subTabs.isSubTabs && curr_ind > 1 ) {
					var subTabsText = tab_pool[curr_ind].replace(".tab_","");
					console.log("subTabsText = "+subTabsText);
					if ( subTabs.hasOwnProperty(subTabsText) ) {
						alert("If statement");
						$(subTabs[subTabsText].toString()).show();
					}
				}
			}
			if (curr_ind == (modelTabs.length-1)) {
				$('.submit, #metaDataToggle, #metaDataText').show();
				$(".next").hide();
			}
		});

		$('.back').click(function () {
			if (curr_ind > 0) {
				$(".tab:visible").hide();
				$("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
				curr_ind = curr_ind - 1;
				console.log(curr_ind);
				console.log(tab_pool[curr_ind]);
				$(tab_pool[curr_ind]).show();
				$("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
				$(".submit, #metaDataToggle, #metaDataText").hide();
				$(".next").show();
				// Check if this tab has subTabs
				if ( subTabs.isSubTabs ) {
					var subTabsText = tab_pool[curr_ind].replace(".tab_","");
					console.log("subTabsText = "+subTabsText);
					if ( subTabs.hasOwnProperty(subTabsText) ) {
						alert("If statement");
						$(subTabs[subTabsText].toString()).show();
					}
				}
			}
			if (curr_ind == 0) {
				$(".back, #metaDataToggle, #metaDataText").hide();
			}
		});
	}
});