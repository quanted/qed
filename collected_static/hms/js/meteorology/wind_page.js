var baseUrl = "/hms/rest/api/v3/meteorology/wind/";


$(function () {
    // $('#overview_block').accordion({
    //     collapsible: true,
    //     heightStyle: "content"
    // });
    $('#id_stationID').parent().parent().hide();
    $('#id_source').on('change', updateSourceSelection);
    $('#id_area_of_interest').on('change', updateAoISelection);

    setTimeout(setOverviewTabindex, 100);
    setTimeout(updateAoISelection, 100);
    setTimeout(updateSourceSelection, 100);
});

function setOutputUI(){
    setMetadata();
    setDataGraph2();
    return false;
}

function getParameters() {
    // Dataset specific request object
    var requestJson = {
        "source": $('#id_source').val(),
        "component": $('#id_component').val(),
        "dateTimeSpan": {
            "startDate": $("#id_startDate").val(),
            "endDate": $('#id_endDate').val()
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
        "outputFormat": "json"
    };
    if($('#id_source').val() === "ncei"){
        requestJson["geometry"]["stationID"] = $("#id_stationID").val();
    }
    if($('#id_area_of_interest').val() === "Catchment Centroid"){
        delete requestJson["geometry"]["point"];
        requestJson["geometry"]["comid"] = $("#id_catchment_comid").val()
    }
    return requestJson;
}

function updateSourceSelection() {
    var selectedSource = $('#id_source').val();
    var ncdcSelect = $('#id_stationID').parent().parent();
    if (selectedSource === "ncei") {
        ncdcSelect.show();
    }
    else {
        ncdcSelect.hide();
    }
    setTimeout(updateAoISelection, 100);
    return false;
}

function updateAoISelection(){
    var source = $("#id_source").val();
    if(source === "ncei"){
        $("#id_area_of_interest").parent().parent().hide();
        $("#id_latitude").parent().parent().hide();
        $("#id_longitude").parent().parent().hide();
        $("#id_catchment_comid").parent().parent().hide();
    }
    else {
        $("#id_area_of_interest").parent().parent().show();
        var aoi = $('#id_area_of_interest').val();
        if (aoi === "Latitude/Longitude") {
            $("#id_latitude").parent().parent().show();
            $("#id_longitude").parent().parent().show();
            $("#id_catchment_comid").parent().parent().hide();
        } else {
            $("#id_latitude").parent().parent().hide();
            $("#id_longitude").parent().parent().hide();
            $("#id_catchment_comid").parent().parent().show();
        }
    }
}

function setOverviewTabindex(){
    $('#ui-id-3').attr('tabindex', '0');
    $('#ui-id-5').attr('tabindex', '0');
    $('#ui-id-7').attr('tabindex', '0');
    $('#ui-id-9').attr('tabindex', '0');
}
