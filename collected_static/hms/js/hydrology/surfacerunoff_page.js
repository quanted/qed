// var baseUrl = "/hms/rest/api/hydrology/surfacerunoff/";
var baseUrl = "/hms/rest/api/v3/hydrology/surfacerunoff/";

$(function () {
    // $('#overview_block').accordion({
    //     collapsible: true,
    //     heightStyle: "content"
    // });
    $('#id_area_of_interest').on('change', updateAoISelection);
    $("#id_source").on('change', precipSourceUpdate);
    $("#id_precip_source").on("change", precipSourceUpdate);

    setTimeout(setOverviewTabindex, 100);
    setTimeout(updateAoISelection, 100);
    setTimeout(precipSourceUpdate, 200);
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
        "dateTimeSpan": {
            "startDate": $("#id_startDate").val(),
            "endDate": $('#id_endDate').val()
        },
        "geometry": {
            "point": {
                "latitude": $("#id_latitude").val(),
                "longitude": $("#id_longitude").val()
            },
            "stationID": $("#id_stationID").val(),
            "geometryMetadata": {
                "precipSource": $("#id_precip_source").val()
            }
        },
        "dataValueFormat": $("#id_outputformat").val(),
        "temporalResolution": $("#id_temporalresolution").val(),
        "timeLocalized": $("#id_timelocalized").val(),
        "units": "default",
        "outputFormat": "json"
    };
    if($('#id_area_of_interest').val() === "Catchment Centroid"){
        delete requestJson["geometry"]["point"];
        requestJson["geometry"]["comid"] = $("#id_catchment_comid").val();
    }
    return requestJson;
}

function updateAoISelection(){
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

function precipSourceUpdate(){
    var algorithm = $("#id_source").val();
    if(algorithm === "curvenumber") {
        $('#id_precip_source').parent().parent().show();
        var pSource = $("#id_precip_source").val();
        if (pSource === "ncei") {
            $("#id_stationID").parent().parent().show();
        } else {
            $("#id_stationID").parent().parent().hide();
        }
        setPrecipSourceConfig();
        $("#id_temporalresolution option").attr('disabled', 'disabled');
        $("#id_temporalresolution option").removeAttr('selected');
        $("#id_temporalresolution option[value='daily']").removeAttr('disabled');
        $("#id_temporalresolution option[value='daily']").attr('selected', 'selected');
        $("#id_temporalresolution option[value='monthly']").removeAttr('disabled');
    }
    else{
        $("#id_stationID").parent().parent().hide();
        $('#id_precip_source').parent().parent().hide();
        $("#id_temporalresolution option").removeAttr('disabled');
        $("#id_temporalresolution option").removeAttr('selected');
        if(algorithm === "nldas"){
            $("#id_temporalresolution option[value='hourly']").attr('selected', 'selected');
            $("#id_temporalresolution option[value='3hourly']").attr('disabled', 'disabled');
        }
        else{
            $("#id_temporalresolution option[value='hourly']").attr('disabled', 'disabled');
            $("#id_temporalresolution option[value='3hourly']").attr('selected', 'selected');
        }
    }
}


function setOverviewTabindex(){
    $('#ui-id-3').attr('tabindex', '0');
    $('#ui-id-5').attr('tabindex', '0');
    $('#ui-id-7').attr('tabindex', '0');
    $('#ui-id-9').attr('tabindex', '0');
}

function setPrecipSourceConfig(){
    var src = $('#id_precip_source').val();
    var local = null;
    var resolution = null;
    if (sourceConfigs.hasOwnProperty(src)) {
        local = sourceConfigs[src]['localtime'];
        resolution = sourceConfigs[src]['temporalResolution'];
    }
    if(local){
        $("#id_timelocalized option[value='true']").removeAttr('disabled');
        $("#id_timelocalized option[value='true']").removeAttr('selected');
        $("#id_timelocalized option[value='true']").attr('selected', 'selected');
    }
    else{
        $("#id_timelocalized option[value='true']").removeAttr('selected');
        $("#id_timelocalized option[value='true']").attr('disabled', 'disabled');
        $("#id_timelocalized option[value='false']").attr('selected', 'selected');
    }

    if(resolution) {
        var validRes = false;
        var resolutionOptions = document.getElementById("id_temporalresolution").getElementsByTagName("option");
        for (var i = 0; i < resolutionOptions.length - 1; i++) {
            if (!validRes) {
                if (resolutionOptions[i].value === resolution) {
                    validRes = true;
                    resolutionOptions[i].disabled = false;
                    resolutionOptions[i].selected = true;
                } else {
                    resolutionOptions[i].disabled = true;
                }
            } else {
                resolutionOptions[i].disabled = false;
            }
        }
    }
}
