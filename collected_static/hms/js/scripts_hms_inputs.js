$(document).ready(function() {
    $('#id_geojson').closest('tr').hide();
    $('#id_geojson_file').closest('tr').hide();
    $('#id_spatial_input').trigger("change");


    $('#id_source').change(function(){
        if(document.input_table.layers) {
            var element = document.getElementById("id_source");
            if(element.options[element.selectedIndex].value === 'NLDAS'){
                 document.input_table.layers.options.length = 0;
                 document.input_table.layers.options[0] = new Option("0-10cm", "0-10");
                 document.input_table.layers.options[1] = new Option("10-40cm", "10-40");
                 document.input_table.layers.options[2] = new Option("40-100cm", "40-100");
                 document.input_table.layers.options[3] = new Option("100-200cm", "100-200");
                 document.input_table.layers.options[4] = new Option("0-100cm", "0-100");
                 document.input_table.layers.options[5] = new Option("0-200cm", "0-200");
             }
             else if (element.options[element.selectedIndex].value === 'GLDAS') {
                document.input_table.layers.options.length = 0;
                document.input_table.layers.options[0] = new Option("0-10cm", "0-10");
                document.input_table.layers.options[1] = new Option("10-40cm", "10-40");
                document.input_table.layers.options[2] = new Option("40-100cm", "40-100");
                document.input_table.layers.options[3] = new Option("0-100cm", "0-100");
             }
        }
    });

    $('#id_spatial_input').change(function(){
       if ($(this).val() === "coordinates"){
           $('#id_geojson').closest('tr').hide();
           document.input_table.geojson.value = "";
           $('#id_geojson_file').closest('tr').hide();
           document.input_table.geojson_file.value = "";
           $('#id_latitude').closest('tr').show();
           $('#id_longitude').closest('tr').show();

           $('#id_temporalresolution').closest('tr').show();

       }
       else if ($(this).val() === "geojson"){
           $('#id_geojson').closest('tr').show();
           $('#id_latitude').closest('tr').hide();
           document.input_table.latitude.value = "";
           $('#id_longitude').closest('tr').hide();
           document.input_table.longitude.value = "";
           $('#id_geojson_file').closest('tr').hide();
           document.input_table.geojson_file.value = "";

           $('#id_temporalresolution').closest('tr').hide();
           $('#id_temporalresolution').val("default");
       }
       else if ($(this).val() === "geojson_file"){
           $('#id_geojson').closest('tr').hide();
           document.input_table.geojson.value = "";
           $('#id_latitude').closest('tr').hide();
           document.input_table.latitude.value = "";
           $('#id_longitude').closest('tr').hide();
           document.input_table.longitude.value = "";
           $('#id_geojson_file').closest('tr').show();

           $('#id_temporalresolution').closest('tr').hide();
           $('#id_temporalresolution').val("default");
       }
    });

    $(window).bind('beforeunload', function () {
        $(":reset").click();
    });
});