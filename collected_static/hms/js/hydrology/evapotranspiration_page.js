// var baseUrl = "/hms/rest/api/hydrology/evapotranspiration/";
var baseUrl = "hms/rest/api/v3/hydrology/evapotranspiration/";

$(function () {
	// $('#overview_block').accordion({
    //     collapsible: true,
    //     heightStyle: "content"
    // });
    // form initialization
    initializeInputForm();

    // form events
	$('#id_locationSource').change(toggleLocation);
	$('#id_algorithm').change(toggleParameters);
	$('#id_source').unbind();
	$('#id_source').change(toggleSource);
    $('#id_area_of_interest').on('change', updateAoISelection);

	setTimeout(setOverviewTabindex, 100);
    setTimeout(updateAoISelection, 100);
    setTimeout(toggleParameters, 100);

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
            "comid": $("#id_comid").val(),
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
    requestJson["algorithm"] = $('#id_algorithm').val();
    requestJson["albedo"] = $("#id_albedo").val();
    requestJson["centrallongitude"] = $("#id_centlong").val();
    requestJson["sunangle"] = $("#id_sunangle").val();
    requestJson["emissivity"] = $("#id_emissivity").val();
    requestJson["model"] = $("#id_model").val();
    requestJson["zenith"] =  $("#id_zenith").val();
    requestJson["lakesurfacearea"] = $("#id_lakesurfarea").val();
    requestJson["lakedepth"] = $("#id_lakedepth").val();
    requestJson["subsurfaceresistance"] = $("#id_subsurfres").val();
    requestJson["stomatalresistance"] = $("#id_stomres").val();
    requestJson["leafwidth"] = $("#id_leafwidth").val();
    requestJson["roughnesslength"] = $("#id_roughlength").val();
    requestJson["vegetationheight"] = $("#id_vegheight").val();
    if ($('#id_algorithm').val() === "shuttleworthwallace"){
        requestJson["leafareaindices"] = {
                    1: $("#id_leafarea_0").val(),
                    2: $("#id_leafarea_1").val(),
                    3: $("#id_leafarea_2").val(),
                    4: $("#id_leafarea_3").val(),
                    5: $("#id_leafarea_4").val(),
                    6: $("#id_leafarea_5").val(),
                    7: $("#id_leafarea_6").val(),
                    8: $("#id_leafarea_7").val(),
                    9: $("#id_leafarea_8").val(),
                    10: $("#id_leafarea_9").val(),
                    11: $("#id_leafarea_10").val(),
                    12: $("#id_leafarea_11").val()
            };
    }
    else if($("#id_algorithm").val() === "mcjannett"){
        requestJson["airtemperature"] = {
            1: $("#id_airtemps_0").val(),
            2: $("#id_airtemps_1").val(),
            3: $("#id_airtemps_2").val(),
            4: $("#id_airtemps_3").val(),
            5: $("#id_airtemps_4").val(),
            6: $("#id_airtemps_5").val(),
            7: $("#id_airtemps_6").val(),
            8: $("#id_airtemps_7").val(),
            9: $("#id_airtemps_8").val(),
            10:$("#id_airtemps_9").val(),
            11:$("#id_airtemps_10").val(),
            12:$("#id_airtemps_11").val()
        };
    }
    else if ($("#id_algorithm").val() === "gldas"){
        requestJson["source"] = "gldas";
    }
    if($('#id_area_of_interest').val() === "Catchment Centroid"){
        delete requestJson["geometry"]["point"];
        requestJson["geometry"]["comid"] = $("#id_catchment_comid").val()
    }
    return requestJson;
}

function initializeInputForm() {
	$('#id_albedo').parent().parent().hide();
	$('#id_centlong').parent().parent().hide();
	$('#id_sunangle').parent().parent().hide();
	$('#id_emissivity').parent().parent().hide();
	$('#id_model').parent().parent().hide();
	$('#id_zenith').parent().parent().hide();
	$('#id_lakesurfarea').parent().parent().hide();
	$('#id_lakedepth').parent().parent().hide();
	$('#id_subsurfres').parent().parent().hide();
	$('#id_stomres').parent().parent().hide();
	$('#id_leafwidth').parent().parent().hide();
	$('#id_roughlength').parent().parent().hide();
	$('#id_vegheight').parent().parent().hide();
	$('#id_leafarea_0').parent().parent().addClass("hidden");
	$('#id_airtemps_0').parent().parent().addClass("hidden");
	$('#id_leafarea_0').parent().parent().hide();
	$('#id_airtemps_0').parent().parent().hide();
	$('#id_stationID').parent().parent().hide();
	$('#id_userdata').parent().parent().hide();
	$('#id_geometrymetadata').parent().parent().hide();
	$("#id_comid").val(-1);
	$('#id_comid').parent().parent().hide();
}

function toggleLocation(){
	var loc = $('#id_locationSource').val();
	switch(loc){
		case 'latlong':
			$('#id_latitude').parent().parent().show();
			$('#id_longitude').parent().parent().show();
			$('#id_comid').parent().parent().hide();
			break;
		case 'comid':
			$('#id_latitude').parent().parent().hide();
			$('#id_longitude').parent().parent().hide();
			$('#id_comid').parent().parent().show();
			break;
		default:
			break;
	}
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


function toggleSource(){
	var state = $('#id_source').val();
	$("#id_timelocalized option[value='true']").prop('disabled', false);
	switch(state){
		case 'ncei':
			$('#id_latitude').parent().parent().hide();
            $('#id_longitude').parent().parent().hide();
            $('#id_stationID').parent().parent().show();
			break;
		case 'daymet':
			$("#id_timelocalized option[value='true']").prop('disabled', 'disabled');
			$("#id_timelocalized").val('false');
			break;
		case 'prism':
			$('#id_latitude').parent().parent().show();
            $('#id_longitude').parent().parent().show();
            $('#id_stationID').parent().parent().hide();
			break;
		case 'custom':
			$('#id_userdata').parent().parent().show();
			break;
		case 'nldas':
		case 'gldas':
		case 'wgen':
		default:
			break;
	}
	updateAoISelection();
}

function toggleParameters() {
	var state = $('#id_algorithm').val();
	$("#id_source").prop("disabled", false);
	$("#id_temporalresolution option[value='hourly']").prop('disabled', false);
	$("#id_temporalresolution option[value='3hourly']").prop('disabled', false);
	resetParameters();
	switch(state){
		case 'nldas':
			$("#id_temporalresolution").val('hourly');
			$("#id_source").prop("disabled", 'disabled');
			$("#id_source").val("nldas");
			break;
		case 'gldas':
			$("#id_temporalresolution option[value='hourly']").attr('disabled', 'disabled');
			$("#id_temporalresolution").val('3hourly');
			$("#id_source").prop("disabled", 'disabled');
			$("#id_source").val("gldas");
			break;
		case "hamon":
			$("#id_temporalresolution option[value='hourly']").attr('disabled', 'disabled');
			$("#id_temporalresolution option[value='3hourly']").attr('disabled', 'disabled');
			$("#id_temporalresolution").val('daily');
			$("#id_source").val("nldas");
			break;
		case "hargreaves":
			$("#id_temporalresolution option[value='hourly']").attr('disabled', 'disabled');
			$("#id_temporalresolution option[value='3hourly']").attr('disabled', 'disabled');
			$("#id_temporalresolution").val('daily');
			$("#id_source").val("nldas");
			break;
        case "priestlytaylor":
        case "grangergray":
        case "penpan":
		case "penmanopenwater":
        case "penmandaily":
			$('#id_albedo').parent().parent().show();
			$("#id_temporalresolution option[value='hourly']").attr('disabled', 'disabled');
			$("#id_temporalresolution option[value='3hourly']").attr('disabled', 'disabled');
			$("#id_source").val("nldas");
			$("#id_temporalresolution").val('daily');
			break;
        case "mcjannett":
			$('#id_albedo').parent().parent().show();
			$('#id_lakesurfarea').parent().parent().show();
			$('#id_lakedepth').parent().parent().show();
			$('#id_airtemps_0').parent().parent().removeClass("hidden");
			$('#id_airtemps_0').parent().parent().show();
			$('#id_airtemps_0')["0"].value = 1.0;
			$('#id_airtemps_1')["0"].value = 1.0;
			$('#id_airtemps_2')["0"].value = 1.0;
			$('#id_airtemps_3')["0"].value = 1.0;
			$('#id_airtemps_4')["0"].value = 1.0;
			$('#id_airtemps_5')["0"].value = 1.0;
			$('#id_airtemps_6')["0"].value = 1.0;
			$('#id_airtemps_7')["0"].value = 1.0;
			$('#id_airtemps_8')["0"].value = 1.0;
			$('#id_airtemps_9')["0"].value = 1.0;
			$('#id_airtemps_10')["0"].value = 1.0;
			$('#id_airtemps_11')["0"].value = 1.0;
			break;
        case "penmanhourly":
			$('#id_albedo').parent().parent().show();
			$('#id_centlong').parent().parent().show();
			$('#id_sunangle').parent().parent().show();
			break;
        case "mortoncrae":
			$('#id_albedo').parent().parent().show();
			$('#id_emissivity').parent().parent().show();
			$('#id_model').parent().parent().show();
			$('#id_model')["0"].options[0] = new Option('ETP', 'ETP');
			$('#id_model')["0"].options[1] = new Option('ETW', 'ETW');
			$('#id_model')["0"].options[2] = new Option('ETA', 'ETA');
			break;
        case "mortoncrwe":
			$('#id_albedo').parent().parent().show();
			$('#id_emissivity').parent().parent().show();
			$('#id_model').parent().parent().show();
			$('#id_model').empty();
			$('#id_model')["0"].options[0] = new Option('ETP', 'ETP');
			$('#id_model')["0"].options[1] = new Option('ETW', 'ETW');
			$('#id_zenith').parent().parent().show();
			break;
        case "shuttleworthwallace":
			$('#id_albedo').parent().parent().show();
			$('#id_subsurfres').parent().parent().show();
			$('#id_stomres').parent().parent().show();
			$('#id_leafwidth').parent().parent().show();
			$('#id_roughlength').parent().parent().show();
			$('#id_vegheight').parent().parent().show();
			$('#id_leafarea_0').parent().parent().removeClass("hidden");
			$('#id_leafarea_0').parent().parent().show();
			$('#id_leafarea_0')["0"].value = 2.51;
			$('#id_leafarea_1')["0"].value = 2.51;
			$('#id_leafarea_2')["0"].value = 2.51;
			$('#id_leafarea_3')["0"].value = 2.51;
			$('#id_leafarea_4')["0"].value = 2.51;
			$('#id_leafarea_5')["0"].value = 2.51;
			$('#id_leafarea_6')["0"].value = 2.51;
			$('#id_leafarea_7')["0"].value = 2.51;
			$('#id_leafarea_8')["0"].value = 2.51;
			$('#id_leafarea_9')["0"].value = 2.51;
			$('#id_leafarea_10')["0"].value = 2.51;
			$('#id_leafarea_11')["0"].value = 2.51;
			break;
        case "hspf":
			$('#id_albedo').parent().parent().show();
			$('#id_centlong').parent().parent().show();
			$('#id_sunangle').parent().parent().show();
			break;
		default:
	}
	updateAoISelection();
}

function resetParameters() {
	$('#id_albedo').parent().parent().hide();
	$('#id_centlong').parent().parent().hide();
	$('#id_sunangle').parent().parent().hide();
	$('#id_emissivity').parent().parent().hide();
	$('#id_model').parent().parent().hide();
	$('#id_zenith').parent().parent().hide();
	$('#id_lakesurfarea').parent().parent().hide();
	$('#id_lakedepth').parent().parent().hide();
	$('#id_subsurfres').parent().parent().hide();
	$('#id_stomres').parent().parent().hide();
	$('#id_leafwidth').parent().parent().hide();
	$('#id_roughlength').parent().parent().hide();
	$('#id_vegheight').parent().parent().hide();
	$('#id_leafarea_0').parent().parent().addClass("hidden");
	$('#id_airtemps_0').parent().parent().addClass("hidden");
	$('#id_leafarea_0').parent().parent().hide();
	$('#id_airtemps_0').parent().parent().hide();
}

function setOverviewTabindex(){
    $('#ui-id-3').attr('tabindex', '0');
    $('#ui-id-5').attr('tabindex', '0');
    $('#ui-id-7').attr('tabindex', '0');
    $('#ui-id-9').attr('tabindex', '0');
}