var baseUrl = "/hms/rest/api/v3/meteorology/humidity/";


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
            "endDate": $('#id_endDate').val(),
            // "dateTimeFormat": $("#id_datetimeformat").val()
        },
        "geometry": {
            "point": {
                "latitude": $("#id_latitude").val(),
                "longitude": $("#id_longitude").val()
            }
        },
        "dataValueFormat": $("#id_outputformat").val(),
        "temporalResolution": $("#id_temporalresolution").val(),
        "timeLocalized": $("#id_timelocalized").val(),
        "units": "default",
        "outputFormat": "json"
    };
    if ($("#id_component").val() === "dewpoint"){
        baseUrl = "/hms/rest/api/v3/meteorology/dewpoint/";
    }
    else{
        requestJson["relative"] = true;
    }

    return requestJson;
}