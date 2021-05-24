
// Div list that all contain the quote class
var quoteDivs = document.getElementsByClassName('quote');
var quoteIndex = 0;
var searchBox;

$(document).ready(function(){

    // Run cycleQuote after 500ms delay on page load.
    setTimeout(cycleQuote, 500);
    google.maps.event.addDomListener(window, 'load', initializeAutocomplete);

});

// cycleQuote: continuously cycles through the divs on the page which have the quote class.
function cycleQuote() {
    var currentQuote = $(quoteDivs).eq(quoteIndex);
    $(currentQuote).fadeIn(1200);
    currentQuote.delay(4000);
    $(currentQuote).fadeOut(1200, cycleQuote);
    currentQuote.delay(1200);
    quoteIndex = ++quoteIndex % quoteDivs.length;
}

// initializeAutocomplete: Initializes google maps search places function with a restriction to only us locations.
function initializeAutocomplete(){
    var input = document.getElementById('community_search_field');
    searchBox = new google.maps.places.Autocomplete(input);
    searchBox.setComponentRestrictions({'country': ['us']});
    searchBox.addListener('place_changed', setLocationValue);
}

function setLocationValue(){
    var place = searchBox.getPlace();
    var county = place.address_components[1]['long_name'].replace(" County", "");
    var state = place.address_components[2]['long_name'];
    var json_value = {};
    json_value["county"] = county;
    json_value["state"] = state;
    $('#location_value').val(JSON.stringify(json_value));
}

function submitSearchForm(){
    document.forms["community_search_form"].submit();
}
