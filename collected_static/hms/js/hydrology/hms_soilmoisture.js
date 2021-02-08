$(document).ready(function () {

    $('#id_source').change(function () {
        if (document.input_table.layers) {
            var element = document.getElementById("id_source");
            var layers = document.getElementById("id_layers");
            if (element.options[element.selectedIndex].value === 'nldas') {
                layers.options.length = 0;
                layers.options[0] = new Option("0-10cm", "0-10");
                layers.options[1] = new Option("10-40cm", "10-40");
                layers.options[2] = new Option("40-100cm", "40-100");
                layers.options[3] = new Option("100-200cm", "100-200");
                layers.options[4] = new Option("0-100cm", "0-100");
                layers.options[5] = new Option("0-200cm", "0-200");
            }
            else if (element.options[element.selectedIndex].value === 'gldas') {
                layers.options.length = 0;
                layers.options[0] = new Option("0-10cm", "0-10");
                layers.options[1] = new Option("10-40cm", "10-40");
                layers.options[2] = new Option("40-100cm", "40-100");
                layers.options[3] = new Option("0-100cm", "0-100");
            }
        }
    });

    $(window).bind('beforeunload', function () {
        $(":reset").click();
    });

});