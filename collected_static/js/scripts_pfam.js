$(document).ready(function() {
    // Call function to setup tabbed nav
    uberNavTabs(
        ["Chemical", "Application", "Location", "Floods", "Crop", "Physical", "Output"],
        {   "isSubTabs":false  }
    );

    // //Input form validation method
    // function isSci(txtValue) {
    //     var currVal = txtValue;
    //     if (currVal == '') {
    //        return false;
    //     }
    //     //Declare Regex  
    //     var rxNumberPattern = /^-?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?/;
    //     var dtArray = currVal.match(rxNumberPattern); // is format OK?
    //     if (dtArray == null) {
    //         return false;
    //     }
    // return true;
    // }   
    
    // function isDate(txtDate) {
    //     var currVal = txtDate;
    //     if (currVal == '') {
    //        return false;
    //     }
    //     //Declare Regex  
    //     var rxDatePattern = /^(\d{1,2})(\/|-)(\d{1,2})$/;
    //     var dtArray = currVal.match(rxDatePattern); // is format OK?
    //     if (dtArray == null) {
    //       return false;
    //     }
    //     //Checks for dd/mm format.
    //     var dtDay = dtArray[3];
    //     var dtMonth = dtArray[1];
        
    //     if (dtMonth.length != 2 || dtMonth < 1 || dtMonth > 12) {
    //         return false;
    //     } else if (dtDay.length != 2 || dtDay < 1 || dtDay > 31) {
    //         return false;
    //     } else if (dtMonth == 2 && dtDay > 29) {
    //         return false;
    //     } else if ( (dtMonth == 4 || dtMonth == 6 || dtMonth == 9 || dtMonth == 11) && (dtDay > 30)) {
    //         return false;
    //     }
    //     return true;
    // }

    // function mmCheck(value) {
    //     var mmValue = Number(value);
    //     if (mmValue < 1 || mmValue > 12) 
    //         return false;
    //     return true;
    // }

    // function ddCheck(value, element) {
    //     var mmValue1 = Number($(element).parent().prev('td').children('input').val());
    //     //console.log(mmValue1);
    //     var ddValue1 = Number(value);
    //     //console.log(value);
    //     if (ddValue1 < 1 || ddValue1 > 31) 
    //         return false;
    //     else if (mmValue1 == 2 && ddValue1 > 29) 
    //         return false;
    //     else if ((mmValue1 == 4 || mmValue1 == 6 || mmValue1 == 9 || mmValue1== 11) && (ddValue1 > 30) )
    //         return false;
    //     return true;
    // }

    // function wlflCheck(value, element) {
    //     var flValue1 = Number($(element).parent().prev('td').children('input').val());
    //     //console.log(flValue1);
    //     var wlValue1 = Number(value);
    //     //console.log(wlValue1);
    //     if (flValue1 >wlValue1) 
    //         return false;
    //     return true;
    // }

    // function mlflCheck(value, element) {
    //     var flValue1 = Number($(element).parent().prev('td').prev('td').children('input').val());
    //     //console.log(flValue1);
    //     var mlValue1 = Number(value);
    //     //console.log(mlValue1);
    //     if (mlValue1 >flValue1) 
    //         return false;
    //     return true;
    // }
            
    // $.validator.addMethod(
    //     "sciFormat",
    //     function (value, element) {
    //         return isSci(value)
    //     },
    //     "Wrong numeric format"
    // );
    
    // $.validator.addMethod(
    //     "dateFormat",
    //     function (value, element) {
    //         return isDate(value)
    //     },
    //     "Date format MM/DD"
    // );

    // $.validator.addMethod(
    //     "monthCheck",
    // function (value) {
    //     return mmCheck(value);
    // },
    //     "Wrong month");

    // $.validator.addMethod(
    //     "dayCheck",
    // function (value, element) {
    //     return ddCheck(value, element);
    // },
    //     "Wrong day");

    // $.validator.addMethod("integer", function(value, element) {
    //     return this.optional(element) || /^-?\d+$/.test(value);
    // }, "Positive integer");

    // $.validator.addMethod(
    //     "wlflCheck",
    // function (value, element) {
    //     return wlflCheck(value, element);
    // },
    //     "Should greater than Fill Level");

    // $.validator.addMethod(
    //     "mlflCheck",
    // function (value, element) {
    //     return mlflCheck(value, element);
    // },
    //     "Should no more than Fill Level");
    
    // $.validator.addMethod('positiveNumber',
    //     function(value) {
    //         return Number(value) > 0;
    //     }, 'Positive number');


    // $.validator.addMethod("mtp", function (value, element) {
    //     var pre_val = Number($(element).parent().parent().prev('tr').find('td:nth-child(2)').children('input').val());
    //     var cur_app_val = Number($(element).parent().prev('td').children('input').val());
    //     var cur_val = Number(value);
    //     // console.log("cur_app_val=", cur_app_val);
    //     // console.log("pre_val=", pre_val);
    //     // console.log("cur_val=", cur_val);

    //     if (cur_app_val == 1)
    //             return true;
    //     else if (cur_val<pre_val)
    //             return false;
    //     return true;

    // }, "In an increasing order");

    // $.validator.messages.required = 'Required';
                  
    // var validator = $('form').validate({
    //     errorElement: "div",
    //     wrapper: "div",  // a wrapper around the error message
    //     ignore: 'input[type="button"],input[type="submit"]',
    //     rules: {
    //         //Chemical tab//
    //         wat_hl: {
    //             required: true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         },
    //         wat_t: {
    //             required : true,
    //             sciFormat: true
    //         },
    //         ben_hl: {
    //             required : true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         },          
    //         ben_t: {
    //             required : true,
    //             sciFormat: true
    //         },          
    //         unf_hl: {
    //             required : true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         },          
    //         unf_t: {
    //             required : true,
    //             sciFormat: true
    //         },          
    //         aqu_hl: {
    //             required : true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         },          
    //         aqu_t: {
    //             required : true,
    //             sciFormat: true
    //         },          
    //         hyd_hl: {
    //             required : true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         },          
    //         mw: {
    //             required : true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         },
    //         vp: {
    //             required : true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         },              
    //         sol: {
    //             required : true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         },              
    //         koc: {
    //             required : true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         },              
    //         hea_h: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },              
    //         hea_r_t: {
    //             required : true,
    //             sciFormat: true
    //         },
    //         ///Application////          
    //         noa: {
    //             required : true
    //         },          
    //         ///Location//////
    //         weather: {
    //             required : true
    //         },          
    //         wea_l: {
    //             required : true,
    //             range: [0, 90]
    //         },
    //         ///Floods//////
    //         nof: {
    //             required : true
    //         },                              
    //         date_f1: {
    //             required : true,
    //             dateFormat: true
    //         },
    //         ///Crop//////
    //         zero_height_ref: {
    //             required : true,
    //             dateFormat: true
    //         },          
    //         days_zero_full: {
    //             required : true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         },              
    //         days_zero_removal: {
    //             required : true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         },  
    //         max_frac_cov: {
    //             required : true,
    //             sciFormat: true,
    //             range: [0, 1]
    //         },
    //         ///Physical////
    //         mas_tras_cof: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },
    //         leak: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },
    //         ref_d: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },              
    //         ben_d: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },          
    //         ben_por: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },              
    //         dry_bkd: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },      
    //         foc_wat: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },          
    //         foc_ben: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },              
    //         ss: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },              
    //         wat_c_doc: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },          
    //         chl: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },              
    //         dfac: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },              
    //         q10: {
    //             required : true,
    //             sciFormat: true,
    //             min: 0
    //         },
    //         ///Output//////
    //         area_app: {
    //             required : true,
    //             sciFormat: true,
    //             positiveNumber: true
    //         }
    //     }
    // });

    var i = 1;
    $('.tab_Application').append('<tr id="noa_header" style="display:none"><th width="18%">App#</th><th width="18%">Month</th><th width="18%">Day</th><th width="23%">Mass Applied</th><th width="23%">Slow Release</th></tr><tr id="noa_header" style="display:none"><th width="18%"></th><th width="18%"></th><th width="18%"></th><th width="23%">(kg/hA)</th><th width="23%">(1/day)</th></tr>');

    var j = 1;
    $('.tab_Floods').append('<tr id="nof_header" style="display:none"><th width="10%">Event</th><th width="18%">Number of</th><th width="18%">Fill Level</th><th width="18%">Wier Level</th><th width="18%">Min. Level</th><th width="18%">Turn Over</th></tr><tr id="nof_header" style="display:none"><th width="10%"></th><th width="18%">Days</th><th width="18%">(m)</th><th width="18%">(m)</th><th width="18%">(m)</th><th width="18%">(1/day)</th></tr>');

    //set default values//
    $('#id_noa').val(2);
    $('tr[id*="noa_header"]').show();
    while (i <= 2) {
        $('.tab_Application').append('<tr class="tab_noa1"><td><input name="jm' + i + '" type="text" size="5" value="' + i + '" disabled/></td><td><input type="text" size="5" name="mm' + i + '" id="id_mm' + i + '"/></td><td><input type="text" size="5" name="dd' + i + '" id="id_dd' + i + '"/></td><td><input type="text" size="5" name="ma' + i + '" id="id_ma' + i + '"/></td><td><input type="text" size="5" name="sr' + i + '" id="id_sr' + i + '" value="0"/></td></tr>');
        i = i + 1;
    }
    $('</table>').appendTo('.tab_Application');

    // $('[name*="mm"]').each(function () {
    //     $(this).rules('add', {
    //         required: true,
    //         monthCheck: true,
    //         integer:true
    //     });
    // });
    // $('[name*="dd"]').each(function () {
    //     $(this).rules('add', {
    //         required: true,
    //         dayCheck: true,
    //         integer:true            
    //     });
    // });
    // $('[name*="ma"]').each(function () {
    //     $(this).rules('add', {
    //         required : true,
    //         sciFormat: true,
    //         min: 0
    //     });
    // });
    // $('[name*="sr"]').each(function () {
    //     $(this).rules('add', {
    //         required : true,
    //         sciFormat: true,
    //         min: 0
    //     });
    // });

    $('[id^="id_mm"]').val(6);
    $('#id_dd1').val(3);
    $('#id_dd2').val(8);

    $('#id_ma1').val(1.12);
    $('#id_ma2').val(1.12);

    $('#id_weather').val('wTest');

    $('#id_nof').val(3);
    $('#id_date_f1').val('05/01');
    $('tr[id*="nof_header"]').show();
    while (j <= 3) {
        if (j == 1){
        $('.tab_Floods').append('<tr class="tab_nof1"><td><input type="text" size="5" value="'+j+'" disabled/></td><td><input type="text" size="5" name="nod'+j+'" id="id_nod'+j+'" value="0" disabled/></td><td><input type="text" size="5" name="fl'+j+'" id="id_fl'+j+'"/></td><td><input type="text" size="5" name="wl'+j+'" id="id_wl'+j+'"/></td><td><input type="text" size="5" name="ml'+j+'" id="id_ml'+j+'"/></td><td><input type="text" size="5" name="to'+j+'" id="id_to'+j+'"/></td></tr>');           
        }
        else {
        $('.tab_Floods').append('<tr class="tab_nof1"><td><input type="text" size="5" value="'+j+'" disabled/></td><td><input type="text" size="5" name="nod'+j+'" id="id_nod'+j+'"/></td><td><input type="text" size="5" name="fl'+j+'" id="id_fl'+j+'"/></td><td><input type="text" size="5" name="wl'+j+'" id="id_wl'+j+'"/></td><td><input type="text" size="5" name="ml'+j+'" id="id_ml'+j+'"/></td><td><input type="text" size="5" name="to'+j+'" id="id_to'+j+'"/></td></tr>');
        }
        j = j + 1;
    }

    $('#id_nod2').val(20);
    $('#id_nod3').val(60);
    $('#id_fl1').val(0.0254);
    $('#id_fl2').val(0.10);
    $('#id_fl3').val(0);
    $('#id_wl1').val(0.12);
    $('#id_wl2').val(0.12);
    $('#id_wl3').val(0);
    $('#id_ml1').val(0);
    $('#id_ml2').val(0.05);
    $('#id_ml3').val(0);
    $('#id_to1').val(0.1);
    $('#id_to2').val(0);
    $('#id_to3').val(0);

    // $('[name*="nod"]').each(function () {
    //     $(this).rules('add', {
    //         required : true,
    //         integer: true,
    //         min: 0,
    //         mtp : true
    //     });
    // });

    // $('[name*="fl"]').each(function () {
    //     $(this).rules('add', {
    //         required : true,
    //         sciFormat: true,
    //         min: 0
    //     });
    // });

    // $('[name*="wl"]').each(function () {
    //     $(this).rules('add', {
    //         required : true,
    //         sciFormat: true,
    //         min: 0,
    //         wlflCheck: true         
    //     });
    // });

    // $('[name*="ml"]').each(function () {
    //     $(this).rules('add', {
    //         required : true,
    //         sciFormat: true,
    //         min: 0,
    //         mlflCheck: true
    //     });
    // });

    // $('[name*="to"]').each(function () {
    //     $(this).rules('add', {
    //         required : true,
    //         sciFormat: true,
    //         min: 0
    //     });
    // });
    //end default setup//

    $('#id_noa').change(function () {
        var total = $(this).val();
        $('tr[id*="noa_header"]').show();
        
        while (i <= total) {
            $('.tab_Application').append('<tr class="tab_noa1"><td><input name="jm' + i + '" type="text" size="5" value="' + i + '" disabled/></td><td><input type="text" size="5" name="mm' + i + '" id="id_mm' + i + '"/></td><td><input type="text" size="5" name="dd' + i + '" id="id_dd' + i + '"/></td><td><input type="text" size="5" name="ma' + i + '" id="id_ma' + i + '"/></td><td><input type="text" size="5" name="sr' + i + '" id="id_sr' + i + '" value="0"/></td></tr>');
            i = i + 1;
        }
        while (i-1 > total) {
            $(".tab_Application tr:last").remove();
            i=i-1;
        }
        $('</table>').appendTo('.tab_Application');
        //addtion rules for dynamic generated cells
        $('[name*="mm"]').each(function () {
            $(this).rules('add', {
                required: true,
                monthCheck: true,
                integer:true
            });
        });

        $('[name*="dd"]').each(function () {
            $(this).rules('add', {
                required: true,
                dayCheck: true,
                integer:true            
            });
        });
        

        $('[name*="ma"]').each(function () {
            $(this).rules('add', {
                required : true,
                sciFormat: true,
                min: 0
            });
        });

        $('[name*="sr"]').each(function () {
            $(this).rules('add', {
                required : true,
                sciFormat: true,
                min: 0
            });

        });
        
    });

    $('#id_nof').change(function () {
        var total_nof = $(this).val();
        $('tr[id*="nof_header"]').show();
        
        while (j <= total_nof) {
            if (j == 1){
            $('.tab_Floods').append('<tr class="tab_nof1"><td><input type="text" size="5" value="'+j+'" disabled/></td><td><input type="text" size="5" name="nod'+j+'" id="id_nod'+j+'" value="0" disabled/></td><td><input type="text" size="5" name="fl'+j+'" id="id_fl'+j+'"/></td><td><input type="text" size="5" name="wl'+j+'" id="id_wl'+j+'"/></td><td><input type="text" size="5" name="ml'+j+'" id="id_ml'+j+'"/></td><td><input type="text" size="5" name="to'+j+'" id="id_to'+j+'"/></td></tr>');           
            }
            else {
            $('.tab_Floods').append('<tr class="tab_nof1"><td><input type="text" size="5" value="'+j+'" disabled/></td><td><input type="text" size="5" name="nod'+j+'" id="id_nod'+j+'"/></td><td><input type="text" size="5" name="fl'+j+'" id="id_fl'+j+'"/></td><td><input type="text" size="5" name="wl'+j+'" id="id_wl'+j+'"/></td><td><input type="text" size="5" name="ml'+j+'" id="id_ml'+j+'"/></td><td><input type="text" size="5" name="to'+j+'" id="id_to'+j+'"/></td></tr>');
            }
            j = j + 1;
        }
        while (j-1 > total_nof) {
            $(".tab_Floods tr:last").remove();
            j=j-1;
        }
        $('</table>').appendTo('.tab_Floods');
        
        $('[name*="nod"]').each(function () {
            $(this).rules('add', {
                required : true,
                integer: true,
                min: 0,
                mtp : true
            });
        });

        $('[name*="fl"]').each(function () {
            $(this).rules('add', {
                required : true,
                sciFormat: true,
                min: 0
            });
        });

        $('[name*="wl"]').each(function () {
            $(this).rules('add', {
                required : true,
                sciFormat: true,
                min: 0,
                wlflCheck: true         
            });
        });

        $('[name*="ml"]').each(function () {
            $(this).rules('add', {
                required : true,
                sciFormat: true,
                min: 0,
                mlflCheck: true
            });
        });

        $('[name*="to"]').each(function () {
            $(this).rules('add', {
                required : true,
                sciFormat: true,
                min: 0
            });
        });
    });
});