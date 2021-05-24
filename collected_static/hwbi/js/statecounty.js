$(document).ready(function(){
    var stateObject = {};
    $.getJSON('/static_qed/hwbi/json/statecounty.json', function (data) {
        $.each(data, function(index, val) {
            stateObject[index] = val;
        });

        var stateSel = document.getElementById("stateSel");
        var countySel = document.getElementById("countySel");

        for (var state in stateObject) {
            stateSel.options[stateSel.options.length] = new Option(state, state);
        }

         stateSel.onchange = function () {
             countySel.length = 1; // remove all options bar first
             if (this.selectedIndex < 1) return; // done
             for (var county in stateObject[this.value]) {
                 countySel.options[countySel.options.length] = new Option(stateObject[this.value][county], stateObject[this.value][county]);
            }
        }
    });


    //on county selection, send ajax POST call sending state and county name to server
    $('#countySel').change(function () {

        $.blockUI({
          //css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "60px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
          message: '<h2 class="popup_header">Loading...</h2><br/><img src="/static_qed/images/loader.gif" style="margin-top: -16px">',
          fadeIn:  500
        });

        //old GET request
        // $.getJSON('/hwbi/rest/hwbi/locations/' + state + '/' + county, function(data) {
        //     $.unblockUI();
        //     updateRIVWeights(data.outputs.domains);
        //     updateDomainScores(data.outputs.domains);
        //     updateDomainScores2(data.outputs.domains);
        //     updateServiceScores(data.outputs.services);
        // });

        var stateVal = $('#stateSel').val();
        var countyVal = $('#countySel').val();

        var poststateData = {
            "state":stateVal,"county":countyVal
            };

        console.log(poststateData);

        var postUrl = "/hwbi/rest/locations/run/";
        $.post(
            postUrl,
            JSON.stringify(poststateData),                  // data (as JS object)
            function(data) {                                // success (callback) function
                $.unblockUI();
                updateRIVWeights(data.outputs.domains);
                updateDomainScores(data.outputs.domains);
                updateDomainScores2(data.outputs.domains);
                updateServiceScores(data.outputs.services);
            },
        "json");                                            // data type returned from server

    });
});


    //function to update RIV domain weight values
    function updateRIVWeights(domains) {
        //console.log(domains);
        $('#ConnectionToNatureDomainWeight').val(domains[0].Weight);
        $('#CulturalFulfillmentDomainWeight').val(domains[1].Weight);
        $('#EducationDomainWeight').val(domains[2].Weight);
        $('#HealthDomainWeight').val(domains[3].Weight);
        $('#LeisureTimeDomainWeight').val(domains[4].Weight);
        $('#LivingStandardsDomainWeight').val(domains[5].Weight);
        $('#SafetyAndSecurityDomainWeight').val(domains[6].Weight);
        $('#SocialCohesionDomainWeight').val(domains[7].Weight);
    }
