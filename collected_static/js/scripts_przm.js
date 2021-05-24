$(document).ready(function() {

var Planting_pool={'NC Sweet Potato MLRA-133': '0805', 'ID Potato   MLRA-11B': '2505', 'NY Grape   MLRA-100/101': '2505', 'CA Citrus   MLRA-17': '2512', 'OR Hops   MLRA-2': '2503', 'FL Sugarcane   MLRA-156A': '2512', 'OR Mint   MLRA-2': '0804', 'FL Citrus   MLRA-156A': '2512', 'CA Almonds MLRA-17': '0901', 'ND Canola   MLRA-55A': '0905', 'MI Asparagus MLRA-96': '0906', 'PR Coffee MLRA-270': '2512', 'FL Avocado MLRA-156A': '2202', 'NC Tobacco   MLRA-133A': '0904', 'CA Grape  MLRA-17': '2501', 'FL Cucumber   MLRA-156A': '0910', 'OH Corn   MLRA-111': '2404', 'NC Apple   MLRA-130': '2503', 'CA Onions MLRA-17': '0901', 'PA Turf  MLRA-148': '2503', 'MI Beans MLRA-99': '2505', 'GA Onions MLRA-153A/133A': '0809', 'LA Sugarcane   MLRA-131': '2512', 'NC Corn - E   MLRA-153A': '0804', 'OR Christmas Trees  MLRA-2': '2512', 'MN Sugarbeet   MLRA-56': '0905', 'FL Turf  MLRA-155': '2501', 'MS Cotton   MLRA-134': '2404', 'MS Soybean   MLRA-134': '0904', 'GA Pecan   MLRA-133A': '0904', 'OR Filberts   MLRA-2': '2202', 'OR Grass Seed   MLRA-2': '0909', 'GA Peach   MLRA-133A': '2202', 'FL Carrots MLRA-156B': '0910', 'NC Cotton   MLRA-133A': '2505', 'CA Lettuce  MLRA-14': '0902', 'FL Tomato   MLRA-155': '2501', 'OR Apple   MLRA-2': '2503', 'ND Wheat   MLRA-56': '0905', 'CA Tomato MLRA-17': '2202', 'PA Corn   MLRA-148': '0904', 'FL Peppers MLRA-156A': '2508', 'MS Corn   MLRA-134': '0304', 'MI Cherry   MLRA-96': '2404', 'IL Corn   MLRA-108': '2404', 'ME Potato   MLRA-146': '2505', 'FL Strawberry   MLRA-155': '2409', 'KS Sorghum   MLRA-112': '1305', 'PA Apple   MLRA-148': '0904', 'CA Cotton   MLRA-17': '2404', 'NC Peanut   MLRA-153A': '0905', 'FL Cabbage   MLRA-155': '0910'};
var EMergence_pool={'NC Sweet Potato MLRA-133': '1505', 'ID Potato   MLRA-11B': '0106', 'NY Grape   MLRA-100/101': '0106', 'CA Citrus   MLRA-17': '0101', 'OR Hops   MLRA-2': '0104', 'FL Sugarcane   MLRA-156A': '0101', 'OR Mint   MLRA-2': '1504', 'FL Citrus   MLRA-156A': '0101', 'CA Almonds MLRA-17': '1601', 'ND Canola   MLRA-55A': '1605', 'MI Asparagus MLRA-96': '1606', 'PR Coffee MLRA-270': '0101', 'FL Avocado MLRA-156A': '0103', 'NC Tobacco   MLRA-133A': '1604', 'CA Grape  MLRA-17': '0102', 'FL Cucumber   MLRA-156A': '1610', 'OH Corn   MLRA-111': '0105', 'NC Apple   MLRA-130': '0104', 'CA Onions MLRA-17': '1601', 'PA Turf  MLRA-148': '0104', 'MI Beans MLRA-99': '0106', 'GA Onions MLRA-153A/133A': '1509', 'LA Sugarcane   MLRA-131': '0101', 'NC Corn - E   MLRA-153A': '1504', 'OR Christmas Trees  MLRA-2': '0101', 'MN Sugarbeet   MLRA-56': '1605', 'FL Turf  MLRA-155': '0102', 'MS Cotton   MLRA-134': '0105', 'MS Soybean   MLRA-134': '1604', 'GA Pecan   MLRA-133A': '1604', 'OR Filberts   MLRA-2': '0103', 'OR Grass Seed   MLRA-2': '1609', 'GA Peach   MLRA-133A': '0103', 'FL Carrots MLRA-156B': '1610', 'NC Cotton   MLRA-133A': '0106', 'CA Lettuce  MLRA-14': '1602', 'FL Tomato   MLRA-155': '0102', 'OR Apple   MLRA-2': '0104', 'ND Wheat   MLRA-56': '1605', 'CA Tomato MLRA-17': '0103', 'PA Corn   MLRA-148': '1604', 'FL Peppers MLRA-156A': '0109', 'MS Corn   MLRA-134': '1004', 'MI Cherry   MLRA-96': '0105', 'IL Corn   MLRA-108': '0105', 'ME Potato   MLRA-146': '0106', 'FL Strawberry   MLRA-155': '0110', 'KS Sorghum   MLRA-112': '2005', 'PA Apple   MLRA-148': '1604', 'CA Cotton   MLRA-17': '0105', 'NC Peanut   MLRA-153A': '1605', 'FL Cabbage   MLRA-155': '1610'};
var MAturation_pool={'NC Sweet Potato MLRA-133': '1509', 'ID Potato   MLRA-11B': '1508', 'NY Grape   MLRA-100/101': '0107', 'CA Citrus   MLRA-17': '0201', 'OR Hops   MLRA-2': '3007', 'FL Sugarcane   MLRA-156A': '0201', 'OR Mint   MLRA-2': '2507', 'FL Citrus   MLRA-156A': '0201', 'CA Almonds MLRA-17': '0208', 'ND Canola   MLRA-55A': '1508', 'MI Asparagus MLRA-96': '2508', 'PR Coffee MLRA-270': '0201', 'FL Avocado MLRA-156A': '1511', 'NC Tobacco   MLRA-133A': '0707', 'CA Grape  MLRA-17': '0103', 'FL Cucumber   MLRA-156A': '0512', 'OH Corn   MLRA-111': '2609', 'NC Apple   MLRA-130': '0305', 'CA Onions MLRA-17': '0106', 'PA Turf  MLRA-148': '1504', 'MI Beans MLRA-99': '2707', 'GA Onions MLRA-153A/133A': '0106', 'LA Sugarcane   MLRA-131': '0201', 'NC Corn - E   MLRA-153A': '2808', 'OR Christmas Trees  MLRA-2': '0201', 'MN Sugarbeet   MLRA-56': '0110', 'FL Turf  MLRA-155': '1502', 'MS Cotton   MLRA-134': '0709', 'MS Soybean   MLRA-134': '0109', 'GA Pecan   MLRA-133A': '2109', 'OR Filberts   MLRA-2': '1504', 'OR Grass Seed   MLRA-2': '1505', 'GA Peach   MLRA-133A': '1505', 'FL Carrots MLRA-156B': '1501', 'NC Cotton   MLRA-133A': '0108', 'CA Lettuce  MLRA-14': '0505', 'FL Tomato   MLRA-155': '2104', 'OR Apple   MLRA-2': '3004', 'ND Wheat   MLRA-56': '2507', 'CA Tomato MLRA-17': '0107', 'PA Corn   MLRA-148': '0407', 'FL Peppers MLRA-156A': '1511', 'MS Corn   MLRA-134': '2208', 'MI Cherry   MLRA-96': '0707', 'IL Corn   MLRA-108': '2109', 'ME Potato   MLRA-146': '0110', 'FL Strawberry   MLRA-155': '1011', 'KS Sorghum   MLRA-112': '2009', 'PA Apple   MLRA-148': '1005', 'CA Cotton   MLRA-17': '2009', 'NC Peanut   MLRA-153A': '0110', 'FL Cabbage   MLRA-155': '0802'};
var HArvest_pool={'NC Sweet Potato MLRA-133': '2209', 'ID Potato   MLRA-11B': '1509', 'NY Grape   MLRA-100/101': '1510', 'CA Citrus   MLRA-17': '3112', 'OR Hops   MLRA-2': '0109', 'FL Sugarcane   MLRA-156A': '3112', 'OR Mint   MLRA-2': '0108', 'FL Citrus   MLRA-156A': '3112', 'CA Almonds MLRA-17': '1309', 'ND Canola   MLRA-55A': '2508', 'MI Asparagus MLRA-96': '1503', 'PR Coffee MLRA-270': '3112', 'FL Avocado MLRA-156A': '3011', 'NC Tobacco   MLRA-133A': '1607', 'CA Grape  MLRA-17': '3108', 'FL Cucumber   MLRA-156A': '1012', 'OH Corn   MLRA-111': '2510', 'NC Apple   MLRA-130': '2510', 'CA Onions MLRA-17': '1506', 'PA Turf  MLRA-148': '0111', 'MI Beans MLRA-99': '0409', 'GA Onions MLRA-153A/133A': '1506', 'LA Sugarcane   MLRA-131': '3112', 'NC Corn - E   MLRA-153A': '1209', 'OR Christmas Trees  MLRA-2': '3112', 'MN Sugarbeet   MLRA-56': '1510', 'FL Turf  MLRA-155': '1512', 'MS Cotton   MLRA-134': '2209', 'MS Soybean   MLRA-134': '1010', 'GA Pecan   MLRA-133A': '0110', 'OR Filberts   MLRA-2': '1011', 'OR Grass Seed   MLRA-2': '3006', 'GA Peach   MLRA-133A': '3108', 'FL Carrots MLRA-156B': '2201', 'NC Cotton   MLRA-133A': '0111', 'CA Lettuce  MLRA-14': '1205', 'FL Tomato   MLRA-155': '1505', 'OR Apple   MLRA-2': '3110', 'ND Wheat   MLRA-56': '0508', 'CA Tomato MLRA-17': '0109', 'PA Corn   MLRA-148': '0110', 'FL Peppers MLRA-156A': '0112', 'MS Corn   MLRA-134': '0209', 'MI Cherry   MLRA-96': '2107', 'IL Corn   MLRA-108': '2010', 'ME Potato   MLRA-146': '0510', 'FL Strawberry   MLRA-155': '1502', 'KS Sorghum   MLRA-112': '0110', 'PA Apple   MLRA-148': '1510', 'CA Cotton   MLRA-17': '1111', 'NC Peanut   MLRA-153A': '1010', 'FL Cabbage   MLRA-155': '1502'};
//alert (HArvest_select['NC Sweet Potato MLRA-133']);

    var ss=$('form').attr('id', 'form1');

    $('#id_CAM_1').attr('id', 'id_1').closest('tr').addClass('method_options').hide();
    $('#id_CAM_2').attr('id', 'id_2').closest('tr').addClass('method_options').hide();
    $('#id_CAM_3').attr('id', 'id_3').closest('tr').addClass('method_options').hide();
    $('#id_CAM_4').attr('id', 'id_4').closest('tr').addClass('method_options').hide();
    $('#id_DEPI').attr('id', 'id_5').closest('tr').addClass('method_options').hide();

    i = 1;
    $('.articles_input').find('table:first').addClass('table');
    $('#id_Ap_m').closest('tr').addClass('app_method');
    $('#id_Ar').closest('tr').addClass('app_rate');
    $('#id_Apt').closest('tr').addClass('app_timing');
    $('#id_DayRe').closest('tr').addClass('app_days');
    //$('#id_CAM_1').closest('tr').addClass('app_days');
    
    $('<tr class="app_dates"><th><label for="id_Date_apt">Application Date 1 (MM/DD):</label></th><td><input readonly="readonly" type="text" name="Date_apt" value="MM/DD" id="id_Date_apt"/></td></tr>').insertAfter('.table tr:nth-child(5)');

//set default values//
    $('#id_Scenarios').val('FL Citrus   MLRA-156A');

    $('#id_NOA').val(1);
    $('#id_Unit_0').attr('checked', true);
    $('#id_Apt').val(1);
    if ($('#id_Apt').val()=='1') {
        $('#id_Apt').closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
        $('#id_Apt').closest('.app_timing').nextAll('.app_days:first').show();
        $('#id_Apt').closest('.app_timing').nextAll('.app_dates:first').find('input').val(Planting_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+Planting_pool[$('#id_Scenarios').val()].slice(0,2));
    }

    $('#id_Ap_m').val(1);
    $('#id_1').closest('tr').show();

    $('#id_1').change(function() {
    $('#id_5').closest('tr').hide();    
    if ($(this).val() >= "4"){          
        $('#id_5').closest('tr').show();
        }
    });

    $('#id_Ar').val(4);

//end setup defaults////


//application method//
    $('#id_Ap_m').change(function() {
        $('tr.method_options').hide();
        if ($(this).val() == "1"){
            $('#id_' + $(this).val()).closest('tr').show();
            $('#id_1').change(function() {
                $('#id_5').closest('tr').hide();    
                if ($(this).val() >= "4"){          
                    $('#id_5').closest('tr').show();
                    }
            });
        }
        else if ($(this).val() == "2"){
            $('#id_' + $(this).val()).closest('tr').show();
            $('#id_2').change(function() {
                $('#id_5').closest('tr').hide();    
                if ($(this).val() >= "4"){          
                    $('#id_5').closest('tr').show();
                    }
            });
        }
        else if ($(this).val() == "3"){
            $('#id_' + $(this).val()).closest('tr').show();
            $('#id_3').change(function() {
                $('#id_5').closest('tr').hide();    
                if ($(this).val() >= "4"){          
                    $('#id_5').closest('tr').show();
                    }
            });
        }
        else if ($(this).val() == "4"){
            $('#id_' + $(this).val()).closest('tr').show();
            $('#id_4').change(function() {
                $('#id_5').closest('tr').hide();    
                if ($(this).val() >= "4"){          
                    $('#id_5').closest('tr').show();
                    }
            });
        }
    });
        
        $('#id_Scenarios').change(function() {
            $('.app_timing').find('select').val( $('.app_timing').find('select').prop('defaultSelected') );
            $('.app_dates').find('input').val( $('.app_dates').find('input').prop('defaultValue') );
            $('.app_days').find('input').val( $('.app_days').find('input').prop('defaultValue') );
            $('.app_timing').find('select').bind('change', function() {
                if ($(this).val()=='1') {
                    $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                    $(this).closest('.app_timing').nextAll('.app_days:first').show();
                    $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(Planting_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+Planting_pool[$('#id_Scenarios').val()].slice(0,2));
                }
                else if ($(this).val()=='2') {
                    $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                    $(this).closest('.app_timing').nextAll('.app_days:first').show();
                    $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(EMergence_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+EMergence_pool[$('#id_Scenarios').val()].slice(0,2));
                }           
                else if ($(this).val()=='3') {
                    $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                    $(this).closest('.app_timing').nextAll('.app_days:first').show();
                    $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(MAturation_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+MAturation_pool[$('#id_Scenarios').val()].slice(0,2));
                }               
                else if ($(this).val()=='4') {
                    $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                    $(this).closest('.app_timing').nextAll('.app_days:first').show();
                    $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(HArvest_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+HArvest_pool[$('#id_Scenarios').val()].slice(0,2));
                }               
                else if ($(this).val()=='5') {
                        $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').attr('readonly',false).val('MM/DD');
                        $(this).closest('.app_timing').nextAll('.app_days:first').find('input').val(0);
                        $(this).closest('.app_timing').nextAll('.app_days:first').hide();
                }
                //alert($('#id_Date_apt2').val().slice(3,5));                  
            });
        });

    // $('#id_Scenarios').attr("disabled", true);

//Number of applications//
    $('#id_NOA').change(function() {
        var total = $(this).val();
        //remove all
        // $('#id_Scenarios').attr("disabled", false);
        $('.app_method').each(function(index) {
            if (index != 0) $(this).remove();
        });
        $('.app_dates').each(function(index) {
            if (index != 0) $(this).remove();
        });     
        $('.app_rate').each(function(index) {
            if (index != 0) $(this).remove();
        });
        $('.app_timing').each(function(index) {
            if (index != 0) $(this).remove();
        });
        $('.app_days').each(function(index) {
            if (index != 0) $(this).remove();
        });
        $('tr[class^="method_options_1"]').remove();
        $('tr[class^="method_options_2"]').remove();        
        $('tr[class^="method_options_3"]').remove();        
        $('tr[class^="method_options_4"]').remove();
        $('tr[class^="method_options_5"]').remove();
        $('.blank').remove();       
        
        //create new ones//
        for (var i = 2; i <= total; i++) {

            $('<tr class="blank"><th colspan="2" align="center">Application'+i+'</th></tr>').appendTo('.table');
            $('<tr class="app_timing"><th><label for="id_Apt'+i+'">Application timing '+i+':</label></th><td><select name="Apt'+i+'" id="id_Apt'+i+'"><option value="" selected="selected">Select an application timing</option><option value="1">Relative to planting</option><option value="2">Relative to emergence</option><option value="3">Relative to maturity</option><option value="4">Relative to harvest</option><option value="5">Enter your own dates</option></select></td></tr>').appendTo('.table');
            $('<tr class="app_dates"><th><label for="id_Date_apt">Application Date '+i+' (MM/DD):</label></th><td><input readonly="readonly" type="text" name="Date_apt'+i+'" value="MM/DD" id="id_Date_apt'+i+'"/></td></tr>').appendTo('.table');
            $('<tr class="app_days"><th><label for="id_DayRe'+i+'">Days relevant to the application '+i+':</label></th><td><input type="text" name="DayRe'+i+'" value="0" id="id_DayRe'+i+'" /></td></tr>').appendTo('.table');
            $('<tr class="app_method"><th><label for="id_Ap_m'+i+'">Application method '+i+':</label></th><td><select name="Ap_m'+i+'" id="id_Ap_m'+i+'"><option value="" selected="selected">Select an application method</option><option value="1">Aerial</option><option value="2">Ground Sprayer</option><option value="3">Airblast</option><option value="4">Other equipment</option></select></td></tr>').appendTo('.table');
            $('<tr class="app_rate"><th><label for="id_Ar'+i+'">Application rate '+i+':</label></th><td><input type="text" name="Ar'+i+'" id="id_Ar'+i+'" /></td></tr>').appendTo('.table');
            $('<tr class="method_options_1'+i+'" style="display: none;"><th><label for="id_CAM_1">Chemical application Method (CAM):</label></th><td><select name="CAM_1_'+i+'" id="id_1_'+i+'"><option value="2">2-Interception based on crop canopy</option><option value="9">9-Linear foliar based on crop canop</option></select></td></tr>').appendTo('.table');
            $('<tr class="method_options_2'+i+'" style="display: none;"><th><label for="id_CAM_2">Chemical application Method (CAM):</label></th><td><select name="CAM_2_'+i+'" id="id_2_'+i+'"><option value="1">1-Soil applied (4cm incorporation, linearly decreasing with depth)</option><option value="2">2-Interception based on crop canopy</option><option value="9">9-Linear foliar based on crop canop</option></select></td></tr>').appendTo('.table');          
            $('<tr class="method_options_3'+i+'" style="display: none;"><th><label for="id_CAM_3">Chemical application Method (CAM):</label></th><td><select name="CAM_3_'+i+'" id="id_3_'+i+'"><option value="2">2-Interception based on crop canopy</option><option value="9">9-Linear foliar based on crop canop</option></select></td></tr>').appendTo('.table');   
            $('<tr class="method_options_4'+i+'" style="display: none;"><th><label for="id_CAM_4">Chemical application Method (CAM):</label></th><td><select name="CAM_4_'+i+'" id="id_4_'+i+'"><option value="1">1-Soil applied (4cm incorporation, linearly decreasing with depth)</option><option value="4">4-Soil applied (user-defined incorporation, uniform with depth)</option><option value="5">5-Soil applied (user-defined incorporation, linearly increasing with depth)</option><option value="6">6-Soil applied (user-defined incorporation, linearly decreasing with depth)</option><option value="7">7-Soil applied, T-Band granular application</option><option value="8">8-Soil applied, chemical incorporated depth specified by user</option></select></td></tr>').appendTo('.table');              
            $('<tr class="method_options_5'+i+'" style="display: none;"><th><label for="id_DEPI">Incorporation depth (DEPI, cm) :</label></th><td><input type="text" name="DEPI_'+i+'" value="4.0" id="id_DEPI_'+i+'"/></td></tr>').appendTo('.table');

            $('.app_timing').find('select').bind('change', function() {
                if ($(this).val()=='1') {
                    $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                    $(this).closest('.app_timing').nextAll('.app_days:first').show();
                    $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(Planting_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+Planting_pool[$('#id_Scenarios').val()].slice(0,2));
                }
                else if ($(this).val()=='2') {
                    $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                    $(this).closest('.app_timing').nextAll('.app_days:first').show();
                    $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(EMergence_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+EMergence_pool[$('#id_Scenarios').val()].slice(0,2));
                }           
                else if ($(this).val()=='3') {
                    $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                    $(this).closest('.app_timing').nextAll('.app_days:first').show();
                    $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(MAturation_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+MAturation_pool[$('#id_Scenarios').val()].slice(0,2));
                }               
                else if ($(this).val()=='4') {
                    $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                    $(this).closest('.app_timing').nextAll('.app_days:first').show();
                    $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(HArvest_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+HArvest_pool[$('#id_Scenarios').val()].slice(0,2));
                }               
                else if ($(this).val()=='5') {
                        $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').attr('readonly',false).val('MM/DD');
                        $(this).closest('.app_timing').nextAll('.app_days:first').find('input').val(0);
                        $(this).closest('.app_timing').nextAll('.app_days:first').hide();
                }
            });

            $('#id_Scenarios').change(function() {
                $('.app_timing').find('select').val( $('.app_timing').find('select').prop('defaultSelected') );
                $('.app_dates').find('input').val( $('.app_dates').find('input').prop('defaultValue') );
                $('.app_days').find('input').val( $('.app_days').find('input').prop('defaultValue') );
                $('.app_timing').find('select').bind('change', function() {
                    if ($(this).val()=='1') {
                        $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                        $(this).closest('.app_timing').nextAll('.app_days:first').show();
                        $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(Planting_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+Planting_pool[$('#id_Scenarios').val()].slice(0,2));
                    }
                    else if ($(this).val()=='2') {
                        $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                        $(this).closest('.app_timing').nextAll('.app_days:first').show();
                        $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(EMergence_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+EMergence_pool[$('#id_Scenarios').val()].slice(0,2));
                    }           
                    else if ($(this).val()=='3') {
                        $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                        $(this).closest('.app_timing').nextAll('.app_days:first').show();
                        $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(MAturation_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+MAturation_pool[$('#id_Scenarios').val()].slice(0,2));
                    }               
                    else if ($(this).val()=='4') {
                        $(this).closest('.app_timing').nextAll('.app_days:first').prop('value', 'readonly');
                        $(this).closest('.app_timing').nextAll('.app_days:first').show();
                        $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').val(HArvest_pool[$('#id_Scenarios').val()].slice(2,4)+'/'+HArvest_pool[$('#id_Scenarios').val()].slice(0,2));
                    }               
                    else if ($(this).val()=='5') {
                            $(this).closest('.app_timing').nextAll('.app_dates:first').find('input').attr('readonly',false).val('MM/DD');
                            $(this).closest('.app_timing').nextAll('.app_days:first').find('input').val(0);
                            $(this).closest('.app_timing').nextAll('.app_days:first').hide();
                    }
                    //alert($('#id_Date_apt2').val().slice(3,5));
                });
            });

            $('.app_method:last').find('select').bind('change', { row: i }, function(event) {
                var i = event.data.row;
                $('.method_options_1'+i).hide();
                $('.method_options_2'+i).hide();
                $('.method_options_3'+i).hide();
                $('.method_options_4'+i).hide();
                $('.method_options_5'+i).hide();
                if ($(this).val() == "1"){
                    $('.method_options_1'+i).show();
                    $('#id_1_'+i).change(function(){
                        $('#id_DEPI_'+i).closest('tr').hide();  
                        if ($(this).val() >= "4"){          
                            $('#id_DEPI_'+i).closest('tr').show();
                        }
                    });
                }
                else if ($(this).val() == "2"){
                    $('.method_options_2'+i).show();
                    $('#id_2_'+i).change(function(){
                        $('#id_DEPI_'+i).closest('tr').hide();  
                        if ($(this).val() >= "4"){          
                            $('#id_DEPI_'+i).closest('tr').show();
                        }
                    });
                }            
                else if ($(this).val() == "3"){
                    $('.method_options_3'+i).show();
                    $('#id_3_'+i).change(function(){
                        $('#id_DEPI_'+i).closest('tr').hide();  
                        if ($(this).val() >= "4"){          
                            $('#id_DEPI_'+i).closest('tr').show();
                        }
                    });
                }
                else if ($(this).val() == "4"){
                    $('.method_options_4'+i).show();
                    $('#id_4_'+i).change(function(){
                        $('#id_DEPI_'+i).closest('tr').hide();  
                        if ($(this).val() >= "4"){          
                            $('#id_DEPI_'+i).closest('tr').show();
                        }
                    });
                }
            }); //end .app_method:last//
    
        } //  endcreate new ones//

    });
        
    var title_app_timing='The application dates should be in sequential.';
    $('.app_timing').find('th').attr('title', title_app_timing);
    $('.app_timing th').qtip();

    var title_chemical='Based on EXPRESS standard scenarios. More scenarios are coming!';
    $("label[for='id_chemical_name']").attr({'title': title_chemical, 'id':'id_chemical_name_title'});
    $('#id_chemical_name_title').qtip();        
        
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////begin the form validation process//////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    // $.validator.addMethod(
    //     "apptiming",
    //     function(value, element) {
    //         if (element.value == "")
    //         {
    //             return false;
    //         }
    //         else return true;
    //     },
    //     "Please choose a application timing."
    // );
    
    // $.validator.addMethod(
    //     "dateFormat",
    //     function (value, element) {
    //         return isDate(value);
    //     },
    //     "Please enter a date in the format MM/DD"
    // );

    // $.validator.addMethod(
    //     "dateSeq",
    //     function (value, element) {
    //         return dateS(value, element);
    //     },
    //     "Application Date should be later than its previous one"
    // );

    // $.validator.addMethod(
    //     "dateRange",
    //     function (value, element) {
    //         return dateRange(value, element);
    //     },
    //     "Application Date should between Jan 1st and Dec 31th"
    // );
                    
    // function isDate(txtDate) {
    //     var currVal = txtDate;
    //     if (currVal == '') {
    //         return false;
    //     }
    //     //Declare Regex  
    //     var rxDatePattern = /^(\d{1,2})(\/|-)(\d{1,2})$/;
    //     var dtArray = currVal.match(rxDatePattern); // is format OK?
    //     if (dtArray == null) {
    //         return false;
    //     }
    //     //Checks for dd/mm format.
    //     var dtDay = dtArray[3];
    //     var dtMonth = dtArray[1];

    //     if (dtMonth.length !=2 ||dtMonth < 1 || dtMonth > 12) {
    //         return false;
    //     } else if (dtDay.length !=2 || dtDay < 1 || dtDay > 31) {
    //         return false;
    //     }
    //     return true;
    // }

    // function dateS(value, element) {

    //     var date1_m = parseFloat($(element).val().slice(0, 2))
    //     var date1_d = parseFloat($(element).val().slice(3, 5))
    //     var dayR1 = parseFloat($(element).closest("tr").nextAll('.app_days:first').find('input').val()) 
    //     var date2_m = parseFloat($(element).closest("tr").prevAll('.app_dates:first').find('input').val().slice(0, 2))
    //     var date2_d = parseFloat($(element).closest("tr").prevAll('.app_dates:first').find('input').val().slice(3, 5))
    //     var dayR2 = parseFloat($(element).closest("tr").prevAll('.app_days:first').find('input').val()) 
    //     var date1_full = new Date(1960, date1_m - 01, date1_d+dayR1)
    //     var date2_full = new Date(1960, date2_m - 01, date2_d+dayR2)

    //     if (date1_full <= date2_full) {
    //         return false;
    //     }
    //     else {
    //         return true;
    //     }
    // }

    // function dateRange(value, element) {
    //     var date1_m = parseFloat($(element).val().slice(0, 2))
    //     var date1_d = parseFloat($(element).val().slice(3, 5))
    //     var dayR1 = parseFloat($(element).closest("tr").nextAll('.app_days:first').find('input').val()) 
    //     var date1_full = new Date(1960, date1_m - 01, date1_d+dayR1)
    //     if (date1_full <= new Date(1960, 11, 31) && date1_full >= new Date(1960, 00, 01) ) {
    //         return true;
    //     }
    //     else {
    //         return false;
    //     }
    // }
    
    // // var validator = $( "#myform" ).validate();
    // // validator.form();


    // $("form").validate({
    //     rules: {
    //         chemical_name: "required",      // simple rule, converted to {required:true}
    //         Scenarios:"required",
    //         NOA:"required",
    //         Unit:"required",
    //         Apt:{apptiming:true
    //         },
    //         DayRe:"required",
    //         Ap_m:"required",
    //         Ar:"required",
    //         Date_apt:{dateFormat:true,
    //                   dateRange:true
    //         },
    //     //2 application
    //         Apt2:{apptiming:true
    //         },
    //         DayRe2:"required",
    //         Ap_m2: {required:true,
    //             equalTo: "#id_Ap_m"
    //             },
    //         Ar2:"required",
    //         Date_apt2:{dateFormat:true,
    //                    dateRange:true,
    //                    dateSeq:true
    //         },                      
    //     //3 application
    //         Apt3:"required",
    //         DayRe3:"required",
    //         Ap_m3: {required:true,
    //                 equalTo: "#id_Ap_m2" 
    //             },
    //         Ar3:"required",
    //         Date_apt3:{dateFormat:true,
    //                    dateRange:true,
    //                    dateSeq:true
    //         },                          
    //     //4 application
    //         Apt4:"required",
    //         DayRe4:"required",
    //         Ap_m4: {required:true,
    //             equalTo: "#id_Ap_m3" 
    //             },
    //         Ar4:"required",
    //         Date_apt4:{dateFormat:true,
    //                    dateRange:true,
    //                    dateSeq:true
    //         }                       
    //     },
    //     messages: {
    //         Scenarios: "Please choose a scenario.",                 
    //         Unit: "Please choose a unit."
    //     }
    // });

});