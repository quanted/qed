// var baseUrl = "/hms/rest/api/hydrology/soilmoisture/";
var baseUrl = "/hms/rest/api/v3/hydrology/soilmoisture/";


$(function () {
    // form events
    $('#id_source').change(updateForm);
    document.getElementById("id_layers").options[0].selected = "selected";
});

function setOutputUI() {
    setMetadata();
    setDataGraph2();
    return false;
}

function getParameters() {
    // Dataset specific request object
    var requestJson = {
        "source": $('#id_source').val(),
        "dateTimeSpan": {
            "startDate": $("#id_startDate").val(),
            "endDate": $('#id_endDate').val(),
            // "dateTimeFormat": $("#id_datetimeformat").val()
        },
        "geometry": {
            "point": {
                "latitude": $("#id_latitude").val(),
                "longitude": $("#id_longitude").val()
            },
            "geometryMetadata": {
                "stationID": $("#id_stationID").val()
            }
        },
        "dataValueFormat": $("#id_outputformat").val(),
        "temporalResolution": $("#id_temporalresolution").val(),
        "timeLocalized": $("#id_timelocalized").val(),
        "units": "default",
        "outputFormat": "json",
        "layers": $("#id_layers").val()
    };
    return requestJson;
}

function updateForm() {
    $('#id_source').change(function () {
        // if (document.input_table.layers) {
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
        }
        document.getElementById("id_layers").options[0].selected = "selected";
    });
}