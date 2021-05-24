var searchBox;
var acc = document.getElementsByClassName("accordion");
var acc_i;

$(document).ready(function () {

    google.maps.event.addDomListener(window, 'load', initializeAutocomplete);

    setAccordion();
    // setTimeout(loadSkillbar, 600);

    // getScoreData if #location_value is not ""
    // else do nothing
});

function getScoreData(){
    var location_data = JSON.parse($('#location_value').value);
    var data_url = "/disc/rest/scores?state=" + location_data['state'] + "&county=" + location_data['county'];
    $.ajax({
        url: data_url,
        type: "GET",
        success: function (data, status, xhr){
            setScoreData()
        }
    });
}

function setScoreData(){
    //Set score data
    loadSkillbar();
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

function loadSkillbar(){
	$('.domain-score-bar').each(function(){
		$(this).find('.score-bar').animate({
			width:jQuery(this).attr('data-percent')
		},2000);
	});
}

function submitSearchForm(){
    document.forms["community_search_form"].submit();
}
