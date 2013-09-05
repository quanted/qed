$(document).ready(function() {
    var curr_ind = 0;
    $(".submit").hide();
    $(".back").hide();
    $(".next").hide();

    $('.start').click(function () {
        if ($("input:checkbox").is(':checked')) {
            $(".next").show();
            $(".start").hide();
            // var tab = $(".tab:visible");

            var tab_pool = ["tab_model"];
            var uptab_pool = ["model"];
            var vis_list = [".model"];

            $('input[name="model"]:checked').each(function () {
                selec_temp = $(this).val()
                tab_pool.push(selec_temp);
                uptab_pool.push(selec_temp.slice(4));
                vis_list.push("."+selec_temp.slice(4));
            });

            $(vis_list.join(', ')).show();
            $(vis_list.join('_li, ')).show();
            
            $(".tab:visible").hide();
            $("."+ uptab_pool[curr_ind]).css({'color': '#333333'});
            curr_ind = curr_ind + 1;

            $("." + tab_pool[curr_ind]).show();
            $("."+ uptab_pool[curr_ind]).css({'color': '#A31E39'});
            
            if (vis_list.length == 2) {
                $(".back").show();
                $(".submit").show();
                $(".next").hide(); }
            else {
                $(".submit").hide();
                $(".back").show(); }

            // Dynamic clickable model nav
            $('li.model').click(function(){
                curr_ind = 0;
                $('li.model').css({'color': '#A31E39'});
                $('li.hdflr, li.vlflr, li.cpcln, li.ipcap, li.mactk, li.ccpst, li.ldtpr, li.clopr, li.impdp, li.cldst, li.impty').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_model').show();
                $(".back").hide();
                $(".submit").hide();
                $(".next").show();
            });

            $('li.hdflr').click(function(){
                if ($.inArray('.hdflr',vis_list) !== -1) {
                    curr_ind = $.inArray('.hdflr',vis_list); }
                $('li.hdflr').css({'color': '#A31E39'});
                $('li.model, li.vlflr, li.cpcln, li.ipcap, li.mactk, li.ccpst, li.ldtpr, li.clopr, li.impdp, li.cldst, li.impty').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_hdflr').show();
                if ($.inArray('.hdflr',vis_list) == vis_list.length - 1) {
                    $(".back").show();
                    $(".submit").show();
                    $(".next").hide(); }
                else {
                    $(".back").show();
                    $(".submit").hide();
                    $(".next").show(); }
            });

            $('li.vlflr').click(function(){
                if ($.inArray('.vlflr',vis_list) !== -1)
                    curr_ind = $.inArray('.vlflr',vis_list);
                $('li.vlflr').css({'color': '#A31E39'});
                $('li.model, li.hdflr, li.cpcln, li.ipcap, li.mactk, li.ccpst, li.ldtpr, li.clopr, li.impdp, li.cldst, li.impty').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_vlflr').show();
                if ($.inArray('.vlflr',vis_list) == vis_list.length - 1) {
                    $(".back").show();
                    $(".submit").show();
                    $(".next").hide(); }
                else {
                    $(".back").show();
                    $(".submit").hide();
                    $(".next").show(); }
            });

            $('li.cpcln').click(function(){
                if ($.inArray('.cpcln',vis_list) !== -1) {
                    curr_ind = $.inArray('.cpcln',vis_list); }
                $('li.cpcln').css({'color': '#A31E39'});
                $('li.model, li.hdflr, li.vlflr, li.ipcap, li.mactk, li.ccpst, li.ldtpr, li.clopr, li.impdp, li.cldst, li.impty').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_cpcln').show();
                if ($.inArray('.cpcln',vis_list) == vis_list.length - 1) {
                    $(".back").show();
                    $(".submit").show();
                    $(".next").hide(); }
                else {
                    $(".back").show();
                    $(".submit").hide();
                    $(".next").show(); }
            });

            $('li.ipcap').click(function(){
                if ($.inArray('.ipcap',vis_list) !== -1) {
                    curr_ind = $.inArray('.ipcap',vis_list); }
                $('li.ipcap').css({'color': '#A31E39'});
                $('li.model, li.hdflr, li.vlflr, li.cpcln, li.mactk, li.ccpst, li.ldtpr, li.clopr, li.impdp, li.cldst, li.impty').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_ipcap').show();
                if ($.inArray('.ipcap',vis_list) == vis_list.length - 1) {
                    $(".back").show();
                    $(".submit").show();
                    $(".next").hide(); }
                else {
                    $(".back").show();
                    $(".submit").hide();
                    $(".next").show(); }
            });

            $('li.mactk').click(function(){
                if ($.inArray('.mactk',vis_list) !== -1) {
                    curr_ind = $.inArray('.mactk',vis_list); }
                $('li.mactk').css({'color': '#A31E39'});
                $('li.model, li.hdflr, li.vlflr, li.cpcln, li.ipcap, li.ccpst, li.ldtpr, li.clopr, li.impdp, li.cldst, li.impty').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_mactk').show();
                if ($.inArray('.mactk',vis_list) == vis_list.length - 1) {
                    $(".back").show();
                    $(".submit").show();
                    $(".next").hide(); }
                else {
                    $(".back").show();
                    $(".submit").hide();
                    $(".next").show(); }
            });

            $('li.ccpst').click(function(){
                if ($.inArray('.ccpst',vis_list) !== -1) {
                    curr_ind = $.inArray('.ccpst',vis_list); }
                $('li.ccpst').css({'color': '#A31E39'});
                $('li.model, li.hdflr, li.vlflr, li.cpcln, li.ipcap, li.mactk, li.ldtpr, li.clopr, li.impdp, li.cldst, li.impty').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_ccpst').show();
                if ($.inArray('.ccpst',vis_list) == vis_list.length - 1) {
                    $(".back").show();
                    $(".submit").show();
                    $(".next").hide(); }
                else {
                    $(".back").show();
                    $(".submit").hide();
                    $(".next").show(); }
            });

            $('li.ldtpr').click(function(){
                if ($.inArray('.ldtpr',vis_list) !== -1) {
                    curr_ind = $.inArray('.ldtpr',vis_list); }
                $('li.ldtpr').css({'color': '#A31E39'});
                $('li.model, li.hdflr, li.vlflr, li.cpcln, li.ipcap, li.mactk, li.ccpst, li.clopr, li.impdp, li.cldst, li.impty').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_ldtpr').show();
                if ($.inArray('.ldtpr',vis_list) == vis_list.length - 1) {
                    $(".back").show();
                    $(".submit").show();
                    $(".next").hide(); }
                else {
                    $(".back").show();
                    $(".submit").hide();
                    $(".next").show(); }
            });

            $('li.clopr').click(function(){
                if ($.inArray('.clopr',vis_list) !== -1) {
                    curr_ind = $.inArray('.clopr',vis_list); }
                $('li.clopr').css({'color': '#A31E39'});
                $('li.model, li.hdflr, li.vlflr, li.cpcln, li.ipcap, li.mactk, li.ccpst, li.ldtpr, li.impdp, li.cldst, li.impty').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_clopr').show();
                if ($.inArray('.clopr',vis_list) == vis_list.length - 1) {
                    $(".back").show();
                    $(".submit").show();
                    $(".next").hide(); }
                else {
                    $(".back").show();
                    $(".submit").hide();
                    $(".next").show(); }
            });

            $('li.impdp').click(function(){
                if ($.inArray('.impdp',vis_list) !== -1) {
                    curr_ind = $.inArray('.impdp',vis_list); }
                $('li.impdp').css({'color': '#A31E39'});
                $('li.model, li.hdflr, li.vlflr, li.cpcln, li.ipcap, li.mactk, li.ccpst, li.ldtpr, li.clopr, li.cldst, li.impty').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_impdp').show();
                if ($.inArray('.impdp',vis_list) == vis_list.length - 1) {
                    $(".back").show();
                    $(".submit").show();
                    $(".next").hide(); }
                else {
                    $(".back").show();
                    $(".submit").hide();
                    $(".next").show(); }
            });

            $('li.cldst').click(function(){
                if ($.inArray('.cldst',vis_list) !== -1) {
                    curr_ind = $.inArray('.cldst',vis_list); }
                $('li.cldst').css({'color': '#A31E39'});
                $('li.model, li.hdflr, li.vlflr, li.cpcln, li.ipcap, li.mactk, li.ccpst, li.ldtpr, li.clopr, li.impdp, li.impty').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_cldst').show();
                if ($.inArray('.cldst',vis_list) == vis_list.length - 1) {
                    $(".back").show();
                    $(".submit").show();
                    $(".next").hide(); }
                else {
                    $(".back").show();
                    $(".submit").hide();
                    $(".next").show(); }
            });

            $('li.impty').click(function(){
                if ($.inArray('.impty',vis_list) !== -1) {
                    curr_ind = $.inArray('.impty',vis_list); }
                $('li.impty').css({'color': '#A31E39'});
                $('li.model, li.hdflr, li.vlflr, li.cpcln, li.ipcap, li.mactk, li.ccpst, li.ldtpr, li.clopr, li.impdp, li.cldst').css({'color': '#333333'});
                $(".tab:visible").hide();
                $('.tab_impty').show();
                if ($.inArray('.impty',vis_list) == vis_list.length - 1) {
                    $(".back").show();
                    $(".submit").show();
                    $(".next").hide(); }
                else {
                    $(".back").show();
                    $(".submit").hide();
                    $(".next").show(); }
            });

        }
        else {
            $(".submit").hide();
            $(".next").hide();
            $(".back").hide();
            $(".start").show();
        }
    });

    $('.next').click(function () {
        console.log(curr_ind)
        if (curr_ind < 11) {      
            var tab_pool = ["tab_model"];
            var uptab_pool = ["model"];
            var vis_list = [".model"];
            
            $('input[name="model"]:checked').each(function () {
                selec_temp = $(this).val()
                tab_pool.push(selec_temp);
                uptab_pool.push(selec_temp.slice(4));
                vis_list.push("."+selec_temp.slice(4));
            });

            $(vis_list.join(', ')).show();
            $(vis_list.join('_li, ')).show();

            $(".tab:visible").hide();
            $("."+ uptab_pool[curr_ind]).css({'color': '#333333'});
            curr_ind = curr_ind + 1;

            $("." + tab_pool[curr_ind]).show();
            $("."+ uptab_pool[curr_ind]).css({'color': '#A31E39'});
            $(".submit").hide();
            $(".back").show();
            }

        if (curr_ind == tab_pool.length-1) {
            $(".submit").show();
            $(".next").hide();
            $(".start").hide();
        }
    });

    $('.back').click(function () {
        console.log(curr_ind)
        if (curr_ind > 0) {
            var tab_pool = ["tab_model"];
            var uptab_pool = ["model"];
            var vis_list = [".model"];

            $('input[name="model"]:checked').each(function () {
                selec_temp = $(this).val()
                tab_pool.push(selec_temp);
                uptab_pool.push(selec_temp.slice(4));
                vis_list.push("."+selec_temp.slice(4));
            });

            $('.uutab').hide();
            $(vis_list.join(', ')).show();
            $(vis_list.join('_li, ')).show();

            $(".tab:visible").hide();
            $("."+ uptab_pool[curr_ind]).css({'color': '#333333'});
            curr_ind = curr_ind - 1;
            $("." + tab_pool[curr_ind]).show();
            $("."+ uptab_pool[curr_ind]).css({'color': '#A31E39'});
            $(".submit").hide();
            $(".next").show();
        }
        if (curr_ind == 0) {
            $(".back").hide();
            $(".next").hide();
            $(".start").show();
        }
    });

});
