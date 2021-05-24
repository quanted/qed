$(document).ready(function () {
    // form initialization
    initializeInputForm();
    // form events 
	$('#id_algorithm').change(toggleParameters);
	$('#id_source').change(toggleSource);
});

function initializeInputForm() {
	$('#id_albedo').closest('tr').hide();
	$('#id_centlong').closest('tr').hide();
	$('#id_sunangle').closest('tr').hide();
	$('#id_emissivity').closest('tr').hide();
	$('#id_model').closest('tr').hide();
	$('#id_zenith').closest('tr').hide();
	$('#id_lakesurfarea').closest('tr').hide();
	$('#id_lakedepth').closest('tr').hide();
	$('#id_subsurfres').closest('tr').hide();
	$('#id_stomres').closest('tr').hide();
	$('#id_leafwidth').closest('tr').hide();
	$('#id_roughlength').closest('tr').hide();
	$('#id_vegheight').closest('tr').hide();
	$('#id_leafarea_0').addClass("hidden");
	$('#id_airtemps_0').addClass("hidden");
	$('#id_leafarea_0').closest('tr').hide();
	$('#id_airtemps_0').closest('tr').hide();
	$('#id_stationID').closest('tr').hide();
	$('#id_userdata').closest('tr').hide();
}

function toggleSource(){
	var state = $('#id_source').val();
	switch(state){
		case 'ncdc':
			$('#id_latitude').closest('tr').hide();
            $('#id_longitude').closest('tr').hide();
            $('#id_stationID').closest('tr').show();
			break;
		case 'nldas':
		case 'gldas':
		case 'wgen':
		case 'daymet':
		case 'prism':
			$('#id_latitude').closest('tr').show();
            $('#id_longitude').closest('tr').show();
            $('#id_stationID').closest('tr').hide();
			break;
		case 'custom':
			$('#id_userdata').closest('tr').show();
			break;
		default:
			break;
	}
}

function toggleParameters() {
	var state = $('#id_algorithm').val();
	resetParameters();
	switch(state){
		case 'nldas':
		case 'gldas':
		case "hamon":
			break;
        case "priestlytaylor":
        case "grangergray":
        case "penpan":
		case "penmanopenwater":
        case "penmandaily":
			$('#id_albedo').closest('tr').show();
			break;
        case "mcjannett":
			$('#id_albedo').closest('tr').show();
			$('#id_lakesurfarea').closest('tr').show();
			$('#id_lakedepth').closest('tr').show();
			$('#id_airtemps_0').removeClass("hidden");
			$('#id_airtemps_0').closest('tr').show();
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
			$('#id_albedo').closest('tr').show();
			$('#id_centlong').closest('tr').show();
			$('#id_sunangle').closest('tr').show();
			//$('#id_temporalresolution')["0"].options[4] = new Option('hourly', 'hourly');
			break;
        case "mortoncrae":
			$('#id_albedo').closest('tr').show();
			$('#id_emissivity').closest('tr').show();
			$('#id_model').closest('tr').show();
			$('#id_model')["0"].options[0] = new Option('ETP', 'ETP');
			$('#id_model')["0"].options[1] = new Option('ETW', 'ETW');
			$('#id_model')["0"].options[2] = new Option('ETA', 'ETA');
			break;
        case "mortoncrwe":
			$('#id_albedo').closest('tr').show();
			$('#id_emissivity').closest('tr').show();
			$('#id_model').closest('tr').show();
			$('#id_model').empty();
			$('#id_model')["0"].options[0] = new Option('ETP', 'ETP');
			$('#id_model')["0"].options[1] = new Option('ETW', 'ETW');
			$('#id_zenith').closest('tr').show();
			break;
        case "shuttleworthwallace":
			$('#id_albedo').closest('tr').show();
			$('#id_subsurfres').closest('tr').show();
			$('#id_stomres').closest('tr').show();
			$('#id_leafwidth').closest('tr').show();
			$('#id_roughlength').closest('tr').show();
			$('#id_vegheight').closest('tr').show();
			$('#id_leafarea_0').removeClass("hidden");
			$('#id_leafarea_0').closest('tr').show();
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
			$('#id_albedo').closest('tr').show();
			$('#id_centlong').closest('tr').show();
			$('#id_sunangle').closest('tr').show();
			//$('#id_temporalresolution')["0"].options[4] = new Option('hourly', 'hourly');
			break;
		default:
	}
}

function resetParameters() {
	$('#id_albedo').closest('tr').hide();
	$('#id_centlong').closest('tr').hide();
	$('#id_sunangle').closest('tr').hide();
	$('#id_emissivity').closest('tr').hide();
	$('#id_model').closest('tr').hide();
	$('#id_zenith').closest('tr').hide();
	$('#id_lakesurfarea').closest('tr').hide();
	$('#id_lakedepth').closest('tr').hide();
	$('#id_subsurfres').closest('tr').hide();
	$('#id_stomres').closest('tr').hide();
	$('#id_leafwidth').closest('tr').hide();
	$('#id_roughlength').closest('tr').hide();
	$('#id_vegheight').closest('tr').hide();
	$('#id_leafarea_0').addClass("hidden");
	$('#id_airtemps_0').addClass("hidden");
	$('#id_leafarea_0').closest('tr').hide();
	$('#id_airtemps_0').closest('tr').hide();
	/*
	$('#id_temporalresolution').empty();
	$('#id_temporalresolution')["0"].options[0] = new Option('default', 'default');
	$('#id_temporalresolution')["0"].options[1] = new Option('daily', 'daily');
	$('#id_temporalresolution')["0"].options[2] = new Option('weekly', 'weekly');
	$('#id_temporalresolution')["0"].options[3] = new Option('monthly', 'monthly');*/
}