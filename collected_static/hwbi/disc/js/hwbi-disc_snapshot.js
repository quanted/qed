var searchBox;
var acc = document.getElementsByClassName("accordion");
var acc_i;
var hwbi_disc_data;

$(document).ready(function () {

    google.maps.event.addDomListener(window, 'load', initializeAutocomplete);
    setAccordion();
    setRankSliders();
    setTimeout(getScoreData, 600);

    // Events
    $('#community_pdf').on("click", notImplementedAlert);
    $('#rank_btn').on("click", toggleRank);
    $('#rank-exit').on("click", function () {
        $('#rank-window').hide();
    });
    $('.rank-slider').on("slidestop", calculateScore);
});

function getScoreData() {
    var location_data = $('#location_value').val().toString();
    if (location_data === "{}") {
        var locationCookie = getCookie("EPAHWBIDISC");
        if(locationCookie !== ""){
            location_data = locationCookie;
        }
        else{
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
            setScoreData(data);
            hwbi_disc_data = JSON.parse(data);
            setCookie('EPAHWBIDISC', location_data, 1);
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

function setScoreData(data) {
    data = JSON.parse(data);
    document.getElementById('score_indicator_span').style.transform = "rotate(0deg) skew(45deg, -45deg)";
    // Set location info
    $('#location').html("Snapshot results for:<br>" + data["inputs"][1]["value"] + " County, " + data["inputs"][0]["value"]);
    $('#wellbeing-score-location').html("Nation: " + data["outputs"]["nationhwbi"].toFixed(1) + ", State: " +
        data["outputs"]["statehwbi"].toFixed(1));

    // Set location score
    var score = Math.round(data["outputs"]["hwbi"]);
    $('#wellbeing-score').html(score);
    document.getElementById('score_indicator_span').style.transform = "rotate(" + Math.round(score * 90 / 50) + "deg) skew(45deg, -45deg)";

    // Set Domain scores
    // Nature
    var nature_score = data["outputs"]["domains"][0]["score"].toFixed(1);
    $('#nature_score').html(nature_score);
    $('#nature_score_bar').attr('data-percent', nature_score + "%");
    $('#nature_location').html("[Nation: " + data["outputs"]["domains"][0]["stateScore"].toFixed(1) +
        ", State: " + data["outputs"]["domains"][0]["stateScore"].toFixed(1) + "]");
    // Culture
    var cultural_score = data["outputs"]["domains"][1]["score"].toFixed(1);
    $('#cultural_score').html(cultural_score);
    $('#cultural_score_bar').attr('data-percent', cultural_score + "%");
    $('#cultural_location').html("[Nation: " + data["outputs"]["domains"][1]["stateScore"].toFixed(1) +
        ", State: " + data["outputs"]["domains"][1]["stateScore"].toFixed(1) + "]");
    // Education
    var education_score = data["outputs"]["domains"][2]["score"].toFixed(1);
    $('#education_score').html(education_score);
    $('#education_score_bar').attr('data-percent', education_score + "%");
    $('#education_location').html("[Nation: " + data["outputs"]["domains"][2]["stateScore"].toFixed(1) +
        ", State: " + data["outputs"]["domains"][2]["stateScore"].toFixed(1) + "]");
    // Education
    var health_score = data["outputs"]["domains"][3]["score"].toFixed(1);
    $('#health_score').html(health_score);
    $('#health_score_bar').attr('data-percent', health_score + "%");
    $('#health_location').html("[Nation: " + data["outputs"]["domains"][3]["stateScore"].toFixed(1) +
        ", State: " + data["outputs"]["domains"][3]["stateScore"].toFixed(1) + "]");
    // Leisure Time
    var leisure_score = data["outputs"]["domains"][4]["score"].toFixed(1);
    $('#leisure_score').html(leisure_score);
    $('#leisure_score_bar').attr('data-percent', leisure_score + "%");
    $('#leisure_location').html("[Nation: " + data["outputs"]["domains"][4]["stateScore"].toFixed(1) +
        ", State: " + data["outputs"]["domains"][4]["stateScore"].toFixed(1) + "]");
    // Living Standards
    var living_score = data["outputs"]["domains"][5]["score"].toFixed(1);
    $('#living-std_score').html(living_score);
    $('#living-std_score_bar').attr('data-percent', living_score + "%");
    $('#living-std_location').html("[Nation: " + data["outputs"]["domains"][5]["stateScore"].toFixed(1) +
        ", State: " + data["outputs"]["domains"][5]["stateScore"].toFixed(1) + "]");
    // Safety and Security
    var safety_score = data["outputs"]["domains"][6]["score"].toFixed(1);
    $('#safety_score').html(safety_score);
    $('#safety_score_bar').attr('data-percent', safety_score + "%");
    $('#safety_location').html("[Nation: " + data["outputs"]["domains"][6]["stateScore"].toFixed(1) +
        ", State: " + data["outputs"]["domains"][6]["stateScore"].toFixed(1) + "]");
    // Social Cohesion
    var cohesion_score = data["outputs"]["domains"][7]["score"].toFixed(1);
    $('#cohesion_score').html(cohesion_score);
    $('#cohesion_score_bar').attr('data-percent', cohesion_score + "%");
    $('#cohesion_location').html("[Nation: " + data["outputs"]["domains"][7]["stateScore"].toFixed(1) +
        ", State: " + data["outputs"]["domains"][7]["stateScore"].toFixed(1) + "]");

    setTimeout(loadSkillbar, 600);
}

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

function setAccordion() {
    for (acc_i = 0; acc_i < acc.length; acc_i++) {
        acc[acc_i].addEventListener("click", function () {
            this.classList.toggle("active");
            var panel = $(this.parentNode).find('.domain-description')[0];
            if (panel.style.display === "block") {
                panel.style.display = "none";
            } else {
                panel.style.display = "block";
            }
        });
    }
}

function loadSkillbar() {
    $('.domain-score-bar').each(function () {
        $(this).find('.score-bar').animate({
            width: jQuery(this).attr('data-percent')
        }, 2000);
    });
}

function setRankSliders() {
    var sliderOptions = {
        animate: "fast",
        max: 5,
        min: 1,
        orientation: "horizontal",
        step: .1
    };
    $('#nature-slider-bar').slider(sliderOptions);
    $('#cultural-slider-bar').slider(sliderOptions);
    $('#education-slider-bar').slider(sliderOptions);
    $('#health-slider-bar').slider(sliderOptions);
    $('#leisure-slider-bar').slider(sliderOptions);
    $('#living-std-slider-bar').slider(sliderOptions);
    $('#safety-slider-bar').slider(sliderOptions);
    $('#cohesion-slider-bar').slider(sliderOptions);

}

function toggleRank() {
    var rWindow = $('#rank-window');
    if (rWindow.is(':visible')) {
        rWindow.hide();
    }
    else {
        rWindow.show();
    }
}

function calculateScore() {
    var weights = document.getElementsByClassName('rank-slider');
    var totalWeightArray = $(weights).map(function () {
        return $(this).slider("value");
    });
    var totalWeight = totalWeightArray.toArray().reduce(sumArray);

    var natureScore = hwbi_disc_data["outputs"]["domains"][0]["score"];
    var natureWeight = $('#nature-slider-bar').slider("value");
    var adjustedNatureScore = natureScore * natureWeight;
    var culturalScore = hwbi_disc_data["outputs"]["domains"][1]["score"];
    var culturalWeight =  $('#cultural-slider-bar').slider("value");
    var adjustedCulturalScore = culturalScore * culturalWeight;
    var educationScore = hwbi_disc_data["outputs"]["domains"][2]["score"];
    var educationWeight = $('#education-slider-bar').slider("value");
    var adjustedEducationScore = educationScore * educationWeight;
    var healthScore = hwbi_disc_data["outputs"]["domains"][3]["score"];
    var healthWeight = $('#health-slider-bar').slider("value");
    var adjustedHealthScore = healthScore * healthWeight;
    var leisureScore = hwbi_disc_data["outputs"]["domains"][4]["score"];
    var leisureWeight = $('#leisure-slider-bar').slider("value");
    var adjustedLeisureScore = leisureScore * leisureWeight;
    var livingStdScore = hwbi_disc_data["outputs"]["domains"][5]["score"];
    var livingStdWeight = $('#living-std-slider-bar').slider("value");
    var adjustedLivingStdScore = livingStdScore * livingStdWeight;
    var safetyScore = hwbi_disc_data["outputs"]["domains"][6]["score"];
    var safetyWeight = $('#safety-slider-bar').slider("value");
    var adjustedSafetyScore = safetyScore * safetyWeight;
    var cohesionScore = hwbi_disc_data["outputs"]["domains"][7]["score"];
    var cohesionWeight = $('#cohesion-slider-bar').slider("value");
    var adjustedCohesionScore = cohesionScore * cohesionWeight;
    var totalScore = adjustedNatureScore + adjustedCulturalScore + adjustedEducationScore + adjustedHealthScore +
        adjustedLeisureScore  + adjustedLivingStdScore + adjustedSafetyScore + adjustedCohesionScore;

    var newScore = totalScore / totalWeight;
    $('#wellbeing-score').html(Math.round(newScore));
    document.getElementById('score_indicator_span').style.transform = "rotate(" + Math.round(newScore * 90 / 50) + "deg) skew(45deg, -45deg)";
}

function sumArray(total, num){
    return total + num;
}

function notImplementedAlert(){
    alert("This feature has not yet been implemented.");
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
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
