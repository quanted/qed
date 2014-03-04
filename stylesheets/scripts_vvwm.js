$(document).ready(function() {
    // Call function to setup tabbed nav
    uberNavTabs(
        ["Chemical", "Applications", "CropLand", "WaterBody"],
        {   "isSubTabs":true,
            "Chemical": [".tab_Chemical0"] }
    );

    // Inital & Maximum Water Body Depth
    $("input[name$='_Custom']").closest('tr').hide();
    $("input[name$='_Pond'], input[name$='_Reservoir']").prop('readonly', true);
    $('#id_SimTypeFlag').change(function() {
        // Simtype selection        
        if ($(this).val() == '0') {
            $("input[name$='_Pond'], input[name$='_Reservoir']").closest('tr').show();
            $("input[name$='_Custom']").closest('tr').hide();
        }
        if ($(this).val() == '4') {
            $("input[name$='_Reservoir']").closest('tr').show();
            $("input[name$='_Pond'], input[name$='_Custom']").closest('tr').hide();
        }
        if ($(this).val() == '5') {
            $("input[name$='_Pond']").closest('tr').show();
            $("input[name$='_Reservoir'], input[name$='_Custom']").closest('tr').hide();
        }
        if ($(this).val() == '1' || $(this).val() == '2' || $(this).val() == '3') {
            $("input[name$='_Custom']").closest('tr').show();
            $("input[name$='_Reservoir'], input[name$='_Pond'], #id_resAvgBox_Custom").closest('tr').hide();
        }
        if ($(this).val() == '6') {
            $("input[name$='_Custom'], #id_resAvgBox_Custom").closest('tr').show();
            $("input[name$='_Reservoir'], input[name$='_Pond']").closest('tr').hide();
        }
    });

    // Temporary Fixes
    $('#id_app_date_type, #upfile1, #upfile2').prop('disabled', true);
    $('#id_year_a_0').prop('disabled', true);

    // Save input page html to browser Local Storage to be retrieved on output page
    $("input[value='Submit']").click(function() {
        var html_input = $("form").html();
        localStorage.html_input=html_input;
        var html_new = $("form").serialize();
        localStorage.html_new=html_new;
    });

});