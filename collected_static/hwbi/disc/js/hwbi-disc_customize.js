var searchBox;
var hwbi_disc_data;
var active_domain;

$(document).ready(function () {

    google.maps.event.addDomListener(window, 'load', initializeAutocomplete);
    setTimeout(getScoreData, 600);

    // Events
    $('.domain-icon').on('click', selectDomain);

});

// initializeAutocomplete: Initializes google maps search places function with a restriction to only us locations.
function initializeAutocomplete() {
    var input = document.getElementById('community_search_field');
    searchBox = new google.maps.places.Autocomplete(input);
    searchBox.setComponentRestrictions({'country': ['us']});
    searchBox.addListener('place_changed', setLocationValue);
}

function setLocationValue() {
    var place = searchBox.getPlace();
    var county = place.address_components[1]['long_name'].replace(" County", "");
    var state = place.address_components[2]['long_name'];
    var json_value = {};
    json_value["county"] = county;
    json_value["state"] = state;
    $('#location_value').val(JSON.stringify(json_value));
}

function submitSearchForm() {
    document.forms["community_search_form"].submit();
}

function getScoreData() {
    var location_data = $('#location_value').val().toString();
    if (location_data === "{}") {
        var locationCookie = getCookie("EPAHWBIDISC");
        if (locationCookie !== "") {
            location_data = locationCookie;
        }
        else {
            return "";
        }
    }
    var location = JSON.parse(location_data);
    var data_url = "/hwbi/disc/rest/scores?state=" + location['state'] + "&county=" + location['county'];
    $.ajax({
        url: data_url,
        type: "GET",
        success: function (data, status, xhr) {
            console.log("getScoreData success: " + status);
            $('#customize_location').html(location['county'] + " County, " + location['state']);
            hwbi_disc_data = JSON.parse(data);
            setCookie('EPAHWBIDISC', location_data, 1);
            $('#customize_domain_score').show();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("getScoreData error: " + errorThrown);
        },
        complete: function (jqXHR, textStatus) {
            console.log("getScoreData complete: " + textStatus);
            return false;
        }
    });
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function selectDomain() {
    if (hwbi_disc_data === undefined) {
        return false;
    }
    $('#customize_domain_arrow').show();
    $('#customize_domain_bar').show();
    var domains = $('.domain-icon');
    $(domains).map(function () {
        $(this).removeClass("domain-selected");
    });
    $(this).addClass("domain-selected");
    var domainID = $(this).attr('id');
    active_domain = domainID;
    var domainScore = $(hwbi_disc_data['outputs']['domains']).map(function () {
        if (this['domainID'] === domainID) {
            return this['score'];
        }
    });
    var domainScoreRounded = Math.round(domainScore[0]);
    $('#arrow_initial').css("left", domainScoreRounded + "%");
    $('#score_initial').html(domainScore[0].toFixed(1));
    $('#score_initial').css("left", domainScoreRounded + "%");
    $('#arrow_adjusted').css("left", domainScoreRounded + "%");
    $('#score_adjusted').html(domainScore[0].toFixed(1));
    $('#score_adjusted').css("left", domainScoreRounded + "%");

    $('#customize_domain_details').html(getDomainDescription(domainID) +
        "Move slider left or right to change the indicator score to describe your community better.");
    showDomainIndicators(domainID);
    // Load domain details
    // Load domain services
    // TODO: Create json of domain:indicator service combinations with associated default weights
    // Load indicators and weights into sliders for updated calculations

}

function getDomainDescription(domainID) {
    if (domainID === "Connection") {
        return "Indicators for the Connection to Nature domain<br>Info from Smith, et al. 2012<br>"
    }
    else if (domainID === "Culture") {
        return "Indicators for the Cultural Fulfillment domain<br>Info from Smith, et al. 2012<br>"
    }
    else if (domainID === "Education") {
        return "Indicators for the Education domain<br>Info from Smith, et al. 2012<br>"
    }
    else if (domainID === "Health") {
        return "Indicators for the Health domain<br>Info from Smith, et al. 2012<br>"
    }
    else if (domainID === "Leisure") {
        return "Indicators for the Leisure Time domain<br>Info from Smith, et al. 2012<br>"
    }
    else if (domainID === "Living") {
        return "Indicators for the Living Standards domain<br>Info from Smith, et al. 2012<br>"
    }
    else if (domainID === "Safety") {
        return "Indicators for the Safety and Security domain<br>Info from Smith, et al. 2012<br>"
    }
    else if (domainID === "Social") {
        return "Indicators for the Social Cohesion domain<br>Info from Smith, et al. 2012<br>"
    }
    else {
        return "Ah Oh! Unable to find domain."
    }
}

function showDomainIndicators(domainID) {
    $('.indicators').map(function () {
        this.hide();
    });
    $('.' + domainID).map(function () {
        this.show();
    });
}

function initializeIndicatorSliders() {

    $('#capital_indicator').slider({
            animate: "fast",
            orientation: "horizontal",
            step: 0.25,
            max: hwbi_disc_data["outputs"]["services"][0]["score"] + 5,
            min: hwbi_disc_data["outputs"]["services"][0]["score"] - 5
        }
    );
    $('#consumption_indicator').slider({
            animate: "fast",
            orientation: "horizontal",
            step: 0.25,
            max: hwbi_disc_data["outputs"]["services"][1]["score"] + 5,
            min: hwbi_disc_data["outputs"]["services"][1]["score"] - 5
        }
    );
    $('#employment_indicator').slider({
            animate: "fast",
            orientation: "horizontal",
            step: 0.25,
            max: hwbi_disc_data["outputs"]["services"][2]["score"] + 5,
            min: hwbi_disc_data["outputs"]["services"][2]["score"] - 5
        }
    );
    $('#finance_indicator').slider({
            animate: "fast",
            orientation: "horizontal",
            step: 0.25,
            max: hwbi_disc_data["outputs"]["services"][3]["score"] + 5,
            min: hwbi_disc_data["outputs"]["services"][3]["score"] - 5
        }
    );
    $('#innovation_indicator').slider({
            animate: "fast",
            orientation: "horizontal",
            step: 0.25,
            max: hwbi_disc_data["outputs"]["services"][4]["score"] + 5,
            min: hwbi_disc_data["outputs"]["services"][4]["score"] - 5
        }
    );
    $('#production_indicator').slider({
            animate: "fast",
            orientation: "horizontal",
            step: 0.25,
            max: hwbi_disc_data["outputs"]["services"][5]["score"] + 5,
            min: hwbi_disc_data["outputs"]["services"][5]["score"] - 5
        }
    );
    $('#redistribution_indicator').slider({
            animate: "fast",
            orientation: "horizontal",
            step: 0.25,
            max: hwbi_disc_data["outputs"]["services"][6]["score"] + 5,
            min: hwbi_disc_data["outputs"]["services"][6]["score"] - 5
        }
    );
    $('#nature_indicator_h').slider(natureSlider, {
            max: hwbi_disc_data["outputs"]["services"][10]["score"] + 5,
            min: hwbi_disc_data["outputs"]["services"][10]["score"] - 5
        }
    );
    $('#nature_indicator_i').slider(natureSlider, {
            max: hwbi_disc_data["outputs"]["services"][20]["score"] + 5,
            min: hwbi_disc_data["outputs"]["services"][20]["score"] - 5
        }
    );
    $('#nature_indicator_j').slider(natureSlider, {
            max: hwbi_disc_data["outputs"]["services"][15]["score"] + 5,
            min: hwbi_disc_data["outputs"]["services"][15]["score"] - 5
        }
    );
}


