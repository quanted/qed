$(document).ready(function() {

    // Testing:
    // $('div.articles_input .Chemical').uberNav({
    //     text: 'Salut, le monde!',
    //     complete: function() { console.log('Plugin Ran') }
    // });
    // List[0] = tab name; List[1] = Additional tables on any tab .class ('tab_Chemical0'); List[1] can be empty/undefined
    uberNavTabs(
        ["Chemical", "Applications", "CropLand", "WaterBody"],
        {   "isSubTabs":true,
            "Chemical":['Chemical0','Chemical1']    }
    );

    // Menu Nav
    function uberNavTabs( modelTabs, subTabs ) {
        console.log('uberNavTabs Function Ran');
        console.log("modelTabs = "+modelTabs);
        console.log("subTabs = "+subTabs.Chemical[0]);
        // Define new variables
        var modelTabsClass = [], liTabArray = [], noOfTabs = modelTabs.length
        // Create 'tab_' & 'li.' arrays
        for (var i = 0;i<noOfTabs;i++) {
            var addTabText = "tab_"+modelTabs[i];
            modelTabsClass.push(addTabText);    
            var addTabText_li = 'li.'+modelTabs[i];
            console.log(addTabText_li);
            liTabArray.push(addTabText_li);
        }
        console.log("modelTabsClass = "+modelTabsClass);
        console.log("liTabArray = "+liTabArray);
        console.log('subTabs.isSubTabs = '+subTabs.isSubTabs);
        if (subTabs.isSubTabs) {
            var subTabsClass = [], liSubTabArray = [], noOfTabSubs = subTabs.length
            for (var j = 1;j<noOfTabSubs;j++) {
                var addSubTabText = "tab_"+subTabs[j];
                subTabsClass.push(addSubTabText);    
                var addSubTabText_li = 'li.'+subTabs[j];
                console.log(addSubTabText_li);
                liSubTabArray.push(addSubTabText_li);
            }
        }
        console.log("subTabsClass = "+subTabsClass);
        console.log("liSubTabArray = "+liSubTabArray);

        // Setup tab defaults
        var tab_pool = modelTabsClass;
        var uptab_pool = modelTabs;
        var visible = $(".tab:visible").attr('class').split(" ")[1];
        var curr_ind = $.inArray(visible, tab_pool);
        $(".back, .submit, #metaDataToggle, #metaDataText").hide();

        // Click handler
        // for (var tabs = 0;tabs<noOfTabs;tabs++) {
            
        // }
        $('.input_nav ul li').click(function() {
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
                $("."+ tab_pool[curr_ind]+", .next").show();
                if ( subTabs[0] == true ) {
                    for (var k = 0;k<liSubTabArray.length;k++) {
                        $("."+ subTabsClass[k]).show();
                    }
                }
            }

            if ( curr_ind > 0 && curr_ind < (modelTabs.length-1) ) {
                console.log('Middle');

                $(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
                $(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
                $('.tab:visible, .submit, #metaDataToggle, #metaDataText').hide();
                $("."+ tab_pool[curr_ind]+", .back, .next").show();
            }

            if ( curr_ind == (modelTabs.length-1) ) {
                console.log('Last');

                $(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
                $(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
                $('.tab:visible, .next, #metaDataToggle, #metaDataText').hide();
                $("."+ tab_pool[curr_ind]+", .back, .submit").show();
            }

        });


        // $('li.Chemical').click(function(){
        //     curr_ind = 0;
        //     $('li.Chemical').addClass('tabSel').removeClass('tabUnsel');
        //     $('li.Applications, li.CropLand, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        //     $('.tab:visible, .back, .submit, #metaDataToggle, #metaDataText').hide();
        //     $('.tab_Chemical, .tab_Chemical0, .next').show();
        // });

        // $('li.Applications').click(function(){
        //     curr_ind = 1;
        //     $('li.Applications').addClass('tabSel').removeClass('tabUnsel');
        //     $('li.Chemical, li.CropLand, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        //     $('.tab:visible, .submit, #metaDataToggle, #metaDataText').hide();
        //     $('.tab_Applications, .back, .next').show();
        // });

        // $('li.CropLand').click(function(){
        //     curr_ind = 2;
        //     $('li.CropLand').addClass('tabSel').removeClass('tabUnsel');
        //     $('li.Chemical, li.Applications, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        //     $('.tab:visible, .submit, #metaDataToggle, #metaDataText').hide();
        //     $('.tab_CropLand, .back, .next').show();
        // });

        // $('li.WaterBody').click(function(){
        //     curr_ind = 3;
        //     $('li.WaterBody').addClass('tabSel').removeClass('tabUnsel');
        //     $('li.Chemical, li.Applications, li.CropLand').addClass('tabUnsel').removeClass('tabSel');
        //     $('.tab:visible, .next').hide();
        //     $('.tab_WaterBody, .tab_WaterBodyWCparms, .tab_WaterBodyBparms, .back, .submit, #metaDataToggle, #metaDataText').show();
        // });

        $('.next').click(function () {
            var tab = $(".tab:visible");
            if (curr_ind < 3) {      
                $(".tab:visible").hide();
                $("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
                curr_ind = curr_ind + 1;
                $("." + tab_pool[curr_ind]).show();
                $("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
                $(".submit, #metaDataToggle, #metaDataText").hide();
                $(".back").show();
                }
            if (curr_ind == 3) {
                $('.submit, .tab_WaterBodyWCparms, .tab_WaterBodyBparms, #metaDataToggle, #metaDataText').show();
                $(".next").hide();
            }
        });

        $('.back').click(function () {
            if (curr_ind > 0) {
                $(".tab:visible").hide();
                $("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
                curr_ind = curr_ind - 1;
                $("." + tab_pool[curr_ind]).show();
                $("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
                $(".submit, #metaDataToggle, #metaDataText").hide();
                $(".next").show();
            }
            if (curr_ind == 0) {
                $(".back, #metaDataToggle, #metaDataText").hide();
                $('.tab_Chemical0').show();
            }
        });
    }
});