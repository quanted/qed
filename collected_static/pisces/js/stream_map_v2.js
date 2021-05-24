var selectedHuc;
var calc;

var updatingTable = false;
var filteredFishTables = {};
var addedFishList = {};
var removedFishList = {};
var fishData;

var thresholdList = ["Crit_Ave", "Crit_P1", "Crit_1SD", "Crit_P0", "Crit_2SD"];
var currentThreshold = thresholdList[0];
var calculatorOn = false;

$(document).ready(function () {

    $('#fishTable').closest('div').hide();
    $('#filteredFishTable').closest('div').hide();
    $('#abundance_calc').closest('div').hide();
    $('#fish_filters').closest('div').hide();
    $('#huc_calc_toggle').closest('div').hide();

    $('#selectHUC').on('change', function () {
        selectHUCs(this.value);
    });

    $('#update_fishtable').on("click", function(){
        updatingTable = true;
        startLoad();
        setTimeout(getFishData, 10);
    });

    $('#threshold_selection').on("change", function(){
        startLoad();
        setTimeout(changeThreshold, 10);
    });

    // Toggle calculator butotn
    $('#in_huc_calc_toggle').on('click', function () {
        calc = this;
        setTimeout(toggleCalculator, 100);
    });

    // Entering value in biomass weight field.
    $('#biomass_weight_field').keyup(function () {
        $('#biomass_count_field').val("");
    });

    // Entering value in biomass count field.
    $('#biomass_count_field').keyup(function () {
        $('#biomass_weight_field').val("");
    });

    // Calculate abundance for assemblage
    $('#biomass_submit').on('click', function () {
        startLoad();
        setTimeout(startCalculation, 1000);
    });

    // Reset calc_table values.
    $('#biomass_reset').on('click', function () {
        $('#biomass_weight_field').val("");
        $('#biomass_count_field').val("");
        var filteredData = $('#filteredFishTable').DataTable().data();
        populateCalcTable(filteredData);
    });

    // Save abundance calculation and assemblage to csv.
    $('#save_to_csv').on('click', function () {
        setTimeout(saveToCSV, 100);
    });

    // Click on calc_table to enable editing.
    $('#calc_table').on('click', 'td', function (e) {
        var v = this.innerHTML;
        if (!v.includes('<input') && ($(this).index() === 0 || $(this).index() === 2)) {
            this.innerHTML = "<input id='tblCell' class='tblCellEdit' onfocus='this.value = this.value;' type='text' value='" + v + "'/>";
        }
        document.getElementById('tblCell').focus();
    });

    // Stopped editing editable calc_table values.
    $('#calc_table').on('blur', 'td', function (e) {
        var v = this.childNodes[0].value;
        var row = $('#calc_table').DataTable().row($(this).closest('tr')).data();
        var orig;
        $('#filteredFishTable').DataTable().rows().every(function (rI, tL, rL) {
            var r = this.data();
            if (row["species_id"] === r["species_id"]) {
                orig = r;
            }
        });
        if (orig["thinning"] === Number(v) || orig["mean_weight"] === Number(v)) {
            $(this).removeClass("cell-edited");
        }
        else {
            $(this).addClass("cell-edited");
        }
        $('#calc_table').DataTable().cell(this).data(v).draw();
    });

    // Add/remove fish from assemblage.
    $('#fishTable').on('click', 'td.select-checkbox', function () {
        startLoad();

        $('#biomass_weight_field').val("");
        $('#biomass_count_field').val("");
        var filteredData = $('#filteredFishTable').DataTable().data();
        populateCalcTable(filteredData);

        var tr = $(this).closest('tr');
        var row = $('#fishTable').DataTable().row(tr).data();
        if (this.children[0].checked) {
            $(this).parent().removeClass('removed_fish');
            if (removedFishList.indexOf(row["species_id"]) >= 0) {
                removedFishList.splice(removedFishList.indexOf(row["species_id"]), 1);
            }
            addedFishList.push(row["species_id"]);
            addFishToFilteredList(row);
        }
        else {
            $(this).parent().addClass('removed_fish');
            removedFishList.push(row["species_id"]);
            if (addedFishList.indexOf(row["species_id"]) >= 0) {
                addedFishList.splice(addedFishList.indexOf(row["species_id"]), 1);
            }
            removeFishFromFilteredList(row);
        }

        var selection = $('#threshold_selection').val();
        var fishTableData = filteredFishTables[selection];
        var fishIDs = [];
        var f;
        for (f in fishTableData) {
            fishIDs.push(fishTableData[f]["species_id"]);
        }
        var completeFishIDList = [];
        var f0;
        for (f0 in fishData){
            var f1 = fishData[f0];
            if ((fishIDs.indexOf(f1["species_id"]) >= 0 ||
                addedFishList.indexOf(f1["species_id"]) >=0) &&
                removedFishList.indexOf(f1["species_id"]) === -1){
                completeFishIDList.push(f1["species_id"]);
                // completeFishData.push(f1);
            }
        }
        highlightFish(completeFishIDList)
        // setTimeout(updateFilterTable, 10);
    });

    $('#streamSearchSwitch').on('click', function () {
        if ($('#streamSearchSwitch').hasClass('coordSearch')) {
            $('#streamSearchSwitch').addClass('hucSearch');
            $('#streamSearchSwitch').removeClass('coordSearch');
            document.getElementById('streamSearchValue').placeholder = 'HUC 8 ID';
            document.getElementById('streamSearchValue').value = "";
            document.getElementById('streamSearchValue').title = "Search for specific HUC8 by HUC ID";
        }
        else {
            $('#streamSearchSwitch').removeClass('hucSearch');
            $('#streamSearchSwitch').addClass('coordSearch');
            document.getElementById('streamSearchValue').placeholder = 'Lat, Lon';
            document.getElementById('streamSearchValue').value = "";
            document.getElementById('streamSearchValue').title = "Search for specific stream segment by lat,lon values";
        }
    });

    $('.fishSearchButton').on('click', function () {
        document.getElementById('searchError').innerHTML = "";
        if ($('#streamSearchSwitch').hasClass('coordSearch')) {
            var latLon = document.getElementById('streamSearchValue').value;
            var llA = latLon.split(',');
            if (isNaN(llA[0]) || isNaN(llA[1])) {
                document.getElementById('searchError').innerHTML = "Invalid lat/long values";
            }
            else {
                selectStreamFromCoord(llA[0], llA[1]);
            }
            return false;
        }
        else {
            var hucID = document.getElementById('streamSearchValue').value;
            if (hucID.length !== 8 || isNaN(hucID)) {
                document.getElementById('searchError').innerHTML = "Invalid HUC ID";
            }
            else {
                var huc8 = getStreamHuc(hucID);
                var huc8geom;
                if (huc8[0][0] < 0) {
                    huc8geom = huc8.map(function (c) {
                        return c.reverse();
                    });
                }
                else {
                    huc8geom = huc8;
                }

                if (map.hasLayer(selectedStream) || map.hasLayer(streamHuc)) {
                    map.removeLayer(selectedStream);
                    map.removeLayer(streamHuc);
                }

                streamHuc = L.polygon(huc8geom, {
                    color: 'white',
                    weight: 2,
                    opacity: 0.9,
                    fillColor: '#9ecae1',
                    fillOpacity: 0.3
                }).addTo(map);
                map.fitBounds(streamHuc.getBounds());
            }
            return false;
        }
    });

    $('#filteredFishTable').on("mouseenter", "tr", function () {
        var index = this.rowIndex;
        $('#calc_table tr:nth-child(' + index + ')').css("background-color", "rgba(160, 160, 160, 1.0)");
    });
    $('#filteredFishTable').on("mouseleave", "tr", function () {
        var index = this.rowIndex;
        var background;

        if (index % 2 === 0)
            background = "white";
        else {
            background = "lightgray";
        }
        $('#calc_table tr:nth-child(' + index + ')').css("background-color", background);
    });
});

function saveToCSV() {
    var calc_table = $('#calc_table').DataTable().rows({order: 'index'}).data();

    var csv_data = "";
    calc_table.map(function (r, i) {
        csv_data += r["genus"] + " " + r["species"] + ", " + r["common_name"] + ", " + r["thinning"] + ", " + r["thin_adj"] +
            ", " + r["mean_weight"] + ", " + r["biomass"] + ", " + r["count"] + "\n";
    });
    var header = "scientific name, common name, thinning coefficient, thinning adjustment, mean weight(g), biomass(kg), count\n";

    var d = new Date();
    var metadata_header = "\nmetadata\nsource, com id, huc id, rarity, stream depth (cm), stream width (m), drainage area (ha)," +
        " slope (%), tss (mg/l), pH (SU), conductivity (uS/cm^2), dissolved oxygen (%), total biomass (kg), total count, date retrieved\n";
    var metadata = "EPA Pisces Fish Assemblage Calculator, " + $('#comid').html() + ", " + $('#huc8').html() +
        ", " + $('#rarity_value').val() + ", " + $('.depth_value').val() + ", " + $('.width_value').val() +
        ", " + $('.area_value').val() + ", " + $('.slope_value').val() + ", " + $('.tss_value').val() +
        ", " + $('.ph_value').val() + ", " + $('.cond_value').val() + ", " + $('.do_value').val() +
        ", " + $('#biomass_weight_field').val() + ", " + $('#biomass_count_field').val() + ", " + d.toISOString() + "\n";

    var file_name = $('#comid').html() + "_epa_fish_assemblage";

    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:data:text/csv;charset=utf-8,' + encodeURIComponent(header + csv_data + metadata_header + metadata));
    pom.setAttribute('download', file_name + '.csv');
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

function toggleCalculator() {
    var button = $(calc).closest('div');
    if (!button[0].classList.contains("calculator")) {
        button.removeClass("fishHucTable");
        button.addClass("calculator");
        document.getElementById('fish_assemblage_estimator').style.float = 'left';
        document.getElementById('fish_assemblage_estimator').style.margin = '0px 0px 0px 5%';

        $('#hucFish').closest('div').hide();
        $('#abundance_calc').closest('div').show();
        calculatorOn = true;
    }
    else {
        button.removeClass("calculator");
        button.addClass("fishHucTable");
        document.getElementById('fish_assemblage_estimator').style.float = 'right';
        document.getElementById('fish_assemblage_estimator').style.margin = '0px 5% 0px 0px';

        $('#abundance_calc').closest('div').hide();
        $('#hucFish').closest('div').show();
        calculatorOn = false;
    }
}

function selectStreamFromCoord(lat, lon) {
    document.getElementById('table-focus').focus();
    $('#latVal').html(lat);
    $('#lngVal').html(lon);
    setTimeout(getStreamData, 10);
}

function onStreamMapClick(e) {
    startLoad();
    $(".area_value").val("");
    $(".slope_value").val("");
    $(".elevation_value").val("");
    $(".iwi_value").val("");
    $(".bmmi_value").val("");
    $('#latVal').html(Number(e.latlng.lat).toFixed(6));
    $('#lngVal').html(Number(e.latlng.lng).toFixed(6));
    setTimeout(getStreamData, 10);
}

function getStreamData() {
    if ($(document.getElementById('huc_calc_toggle')).hasClass("calculator")) {
        $('#in_huc_calc_toggle').trigger("click");
    }
    var lat = $('#latVal').html();
    var lng = $('#lngVal').html();
    var url = "https://ofmpub.epa.gov/waters10/PointIndexing.Service";
    var latitude = lat.toString();
    var longitude = lng.toString();
    ptIndexParams = {
        'pGeometry': 'POINT(' + longitude + ' ' + latitude + ')'
        , 'pGeometryMod': 'WKT,SRSNAME=urn:ogc:def:crs:OGC::CRS84'
        , 'pPointIndexingMethod': 'DISTANCE'
        , 'pPointIndexingMaxDist': 25
        , 'pOutputPathFlag': 'TRUE'
        , 'pReturnFlowlineGeomFlag': 'TRUE'
        , 'optOutCS': 'SRSNAME=urn:ogc:def:crs:OGC::CRS84'
        , 'optOutPrettyPrint': 0
    };

    $.ajax({
        type: "GET",
        url: url,
        jsonp: true,
        data: ptIndexParams,
        async: false,
        success: function (data, status, jqXHR) {
            var streamData = data;
            if(!typeof(data) === "object") {
                streamData = JSON.parse(data);
            }
            var huc8ID = streamData.output.ary_flowlines[0].wbd_huc12.substring(0, 8);
            $('#comid').html(streamData.output.ary_flowlines[0].comid);
            $('#huc8').html(huc8ID);
            $('#streamMapInfo').html("<strong>Stream Segment Selected: </strong><a href='https://watersgeo.epa.gov/watershedreport/?comid=" +
                streamData.output.ary_flowlines[0].comid + "' title='Get more information on this stream segment.' target='_blank'>" + streamData.output.ary_flowlines[0].comid + "</a>");
            addStreamSeg(streamData);
            // getStreamProperties();
            getFishData();
            // endLoad();
            return data;
        },
        error: function (jqXHR, status) {
            $('#comId').html("Error attempting to get river data.");
            endLoad();
            return null;
        }
    });
}

function getFishData() {
    var huc8 = selectedHuc;
    var lat = $('#latVal').html();
    var lng = $('#lngVal').html();
    var comid = $('#comid').html();
    var url = "/pisces/rest/api/v2/fish/models/?huc=" + huc8 + "&comid=" + comid + "&latitude=" + lat + "&longitude=" + lng;
    if(updatingTable){
        var bmmi = $('#bmmi_value').val();
        var iwi = $('#iwi_value').val();
        url = "/pisces/rest/api/v2/fish/models/?huc=" + huc8 + "&comid=" + comid + "&latitude=" + lat + "&longitude=" + lng + "&bmmi=" + bmmi + "&iwi=" + iwi;
        updatingTable = false;
    }
    $.ajax({
        type: "GET",
        url: url,
        crossDomain: true,
        success: function (data, status, jqXHR) {
            $('#error_msg').html("");
            if(calculatorOn){
                $('#in_huc_calc_toggle').trigger("click");
            }
            fishData = data["species"];
            removedFishList = [];
            addedFishList = [];
            $('#fish_filters').closest('div').show();
            $('#envelope_toggle').closest('div').show();
            $('#huc_calc_toggle').closest('div').show();

            $('#wa_value').val(Number(data["stream"]["attributes"]["wa"]).toFixed(1));
            $('#slope_value').val(Number(data["stream"]["attributes"]["slope"]).toFixed(3));
            $('#elev_value').val(Number(data["stream"]["attributes"]["elevation"]).toFixed(1));
            $('#iwi_value').val(Number(data["stream"]["attributes"]["iwi"]).toFixed(2));
            $('#bmmi_value').val(Number(data["stream"]["attributes"]["bmmi"]).toFixed(2));
            assignFilterTables(data["species"]);
            populateFishTable(data["species"]);

            changeThresholdColumn();
            updateFilterTable();
        },
        error: function (jqXHR, status, errorThrown) {
            console.log("ERROR: ajax call failed. " + status);
            $('#error_msg').html("Error: failed to get fish data for the selected huc.");
            stopLoader();
            return null;
        }
    });
}

function updateFilterTable(){
    var selection = $('#threshold_selection').val();
    var fishTableData = filteredFishTables[selection];

    var fishIDs = [];
    var f;
    for (f in fishTableData) {
        fishIDs.push(fishTableData[f]["species_id"]);
    }
    var completeFishIDList = [];
    var completeFishData = [];
    var f0;
    for (f0 in fishData){
        var f1 = fishData[f0];
        if ((fishIDs.indexOf(f1["species_id"]) >= 0 ||
            addedFishList.indexOf(f1["species_id"]) >=0) &&
            removedFishList.indexOf(f1["species_id"]) === -1){
            completeFishIDList.push(f1["species_id"]);
            completeFishData.push(f1);
        }
    }

    populateFilteredFishTableV2(completeFishData);
    populateCalcTable(completeFishData);

    highlightFish(completeFishIDList);
    endLoad();
}

function changeThreshold(){
    var selection = $('#threshold_selection').val();
    var fishTableData = filteredFishTables[selection];

    var fishIDs = [];
    var f;
    for (f in fishTableData) {
        fishIDs.push(fishTableData[f]["species_id"]);
    }
    var completeFishIDList = [];
    var completeFishData = [];
    var f0;
    for (f0 in fishData){
        var f1 = fishData[f0];
        if ((fishIDs.indexOf(f1["species_id"]) >= 0 ||
            addedFishList.indexOf(f1["species_id"]) >=0) &&
            removedFishList.indexOf(f1["species_id"]) === -1){
            completeFishIDList.push(f1["species_id"]);
            completeFishData.push(f1);
        }
    }

    var fishTable = $('#fishTable').DataTable();
    $('#filteredFishTable').DataTable().clear().draw();
    $('#calc_table').DataTable().clear().draw();
    fishTable.rows().every(function (rowIdx, tableLoop, rowLoop) {
        var r = JSON.parse(JSON.stringify(this.data()));
        if (completeFishIDList.indexOf(r["species_id"]) >= 0) {
            $('#filteredFishTable').DataTable().row.add(r).draw();
            $('#calc_table').DataTable().row.add(r).draw();
        }
    });
    highlightFish(completeFishIDList);
    changeThresholdColumn();
    endLoad();
}

function changeThresholdColumn(){
    var dt = $('#fishTable').DataTable();
    var thresholdColumns = {
        "Crit_Ave": 28,
        "Crit_P1": 30,
        "Crit_1SD": 26,
        "Crit_P0": 29,
        "Crit_2SD": 27
    };

    dt.column(thresholdColumns[currentThreshold]).visible(false);
    currentThreshold = $('#threshold_selection').val();
    dt.column(thresholdColumns[currentThreshold]).visible(true);
}

function addFishToFilteredList(data){
    $('#filteredFishTable').DataTable().row.add(data).draw();
    $('#calc_table').DataTable().row.add(data).draw();
    endLoad();
}

function removeFishFromFilteredList(data){
    var table = $('#filteredFishTable').DataTable();
    var indexes = table.rows().eq(0).filter( function (rowIdx) {
        return table.cell( rowIdx, 4 ).data() === data["species_id"] ? true : false;
    });
    $('#filteredFishTable').DataTable().row(indexes[0]).remove().draw();
    $('#calc_table').DataTable().row(indexes[0]).remove().draw();
    endLoad();
}

function highlightFish(fishList){

    var fishTable = $('#fishTable').DataTable();
    fishTable.rows().nodes().to$().removeClass('filteredInFishTable');

    // Iterates through rows of fishTable and adds highlighting class to each row in assemblage.
    fishTable.rows({order: 'index'}).data().filter(function (value, index) {
        var id = value["species_id"];
        if (fishList.indexOf(id) >= 0) {
            var row = fishTable.row(index).node();
            $('input[type="checkbox"]', row).prop("checked", true);
            fishTable.row(index).nodes().to$().addClass('filteredInFishTable');
        }
        else{
            var row = fishTable.row(index).node();
            $('input[type="checkbox"]', row).prop("checked", false);
        }
    });
}

function assignFilterTables(data){
    var t;
    for (t in thresholdList){
        var k = thresholdList[t];
        filteredFishTables[k] = [];
    }

    var d;
    for (d in data){
        var t1;
        var d0 = data[d];
        for (t1 in thresholdList){
            var k1 = thresholdList[t1];
            if (d0[k1] === 1){
                filteredFishTables[k1].push(d0);
            }
        }
    }
}

function populateFishTable(data) {
    $('#fishTable').DataTable().destroy();
    $('#fishTable').empty();
    var config = {
        data: data,
        "columns": [
            {
                title: "Add/Remove",
                name: "add_remove"
            },
            {
                data: "common_name",
                title: "Common Name",
                name: "common_name"
            },
            {
                data: "species",
                title: "Scientific Name",
                name: "scientific_name"
            },
            {
                data: "genus",
                title: "Genus",
                name: "genus"
            },
            {
                data: "genusID",
                title: "Genus Id",
                name: "genus_id"
            },
            {
                data: "species_id",
                title: "Species Id",
                name: "species_id"

            },
            {
                data: "mean_weight",
                title: "Mean Weight",
                name: "mean_weight"
            },
            {
                data: "rarity",
                title: "Rarity",
                name: "rarity"
            },
            {
                data: "thinning",
                title: "&beta;",
                name: "beta"
            },
            {
                data: "thin_adj",
                title: "&Delta;",
                name: "delta"
            },
            {
                data: "slope_l",
                title: "Slope Lower",
                name: "slope_l"
            },
            {
                data: "slope_u",
                title: "Slope Upper",
                name: "slope_u"
            },
            {
                data: "area_l",
                title: "Area Lower",
                name: "area_l"
            },
            {
                data: "area_u",
                title: "Area Upper",
                name: "area_u"
            },
            {
                data: "elev_l",
                title: "Elevation Lower",
                name: "elev_l"
            },
            {
                data: "elev_u",
                title: "Elevation Upper",
                name: "elev_u"
            },
            {
                data: "iwi_l",
                title: "IWI Lower",
                name: "iwi_l"
            },
            {
                data: "iwi_u",
                title: "IWI Upper",
                name: "iwi_u"
            },
            {
                data: "bmmi_l",
                title: "BMMI Lower",
                name: "bmmi_l"
            },
            {
                data: "bmmi_u",
                title: "BMMI Upper",
                name: "bmmi_u"
            },
            {
                data: "probability",
                title: "Probability",
                name: "probability"
            },
            {
                data: "Crit_1SD",
                title: "Crit_1SD",
                name: "Crit_1SD"
            },
            {
                data: "Crit_2SD",
                title: "Crit_2SD",
                name: "Crit_2SD"
            },
            {
                data: "Crit_Ave",
                title: "Crit_Ave",
                name: "Crit_Ave"
            },
            {
                data: "Crit_P0",
                title: "Crit_P0",
                name: "Crit_P0"
            },
            {
                data: "Crit_P1",
                title: "Crit_P1",
                name: "Crit_P1"
            },
            {
                data: "crit_1sd",
                title: "1SD",
                name: "crit_1sd"
            },
            {
                data: "crit_2sd",
                title: "2SD",
                name: "crit_2sd"
            },
            {
                data: "crit_ave",
                title: "Ave",
                name: "crit_ave"
            },
            {
                data: "crit_p0",
                title: "P0",
                name: "crit_p0"
            },
            {
                data: "crit_p1",
                title: "P1",
                name: "crit_p1"
            }
        ],
        "columnDefs": [
            {
                "targets": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                "visible": false
            },
            {
                "render": function (data, type, row) {
                    return row["genus"] + " " + data;
                },
                "targets": 2
            },
            {
                width: 50, targets: [0]
            },
            {
                "targets": 0,
                'searchable': false,
                'orderable': false,
                'className': 'select-checkbox',
                'render': function (data, type, full, meta) {
                    return '<input type="checkbox" checked>';
                }
            },
            {
                "render": function(data, type, row){
                    return Number(data).toFixed(2);
                },
                "targets": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
            }
        ],
        select: {
            style: 'os',
            selector: 'td:first-child'
        },
        searching: false,
        paging: false,
        bInfo: false,
        "order": [[1, 'asc']]

    };
    $('#fishTable').closest('div').show();
    $('#fishTable').DataTable(config);
}

function populateFilteredFishTableV2(data) {
    $('#filteredFishTable').DataTable().destroy();
    $('#filteredFishTable').empty();
    var config = {
        data: data,
        "columns": [
            {
                data: "common_name",
                title: "Common Name",
                name: "common_name"
            },
            {
                data: "species",
                title: "Scientific Name",
                name: "scientific_name"
            },
            {
                data: "genus",
                title: "Genus",
                name: "genus"
            },
            {
                data: "genusID",
                title: "Genus Id",
                name: "genus_id"
            },
            {
                data: "species_id",
                title: "Species Id",
                name: "species_id"

            },
            {
                data: "mean_weight",
                title: "Mean Weight",
                name: "mean_weight"
            },
            {
                data: "rarity",
                title: "Rarity",
                name: "rarity"
            },
            {
                data: "thinning",
                title: "&beta;",
                name: "beta"
            },
            {
                data: "thin_adj",
                title: "&Delta;",
                name: "delta"
            },
            {
                data: "slope_l",
                title: "Slope Lower",
                name: "slope_l"
            },
            {
                data: "slope_u",
                title: "Slope Upper",
                name: "slope_u"
            },
            {
                data: "area_l",
                title: "Area Lower",
                name: "area_l"
            },
            {
                data: "area_u",
                title: "Area Upper",
                name: "area_u"
            },
            {
                data: "elev_l",
                title: "Elevation Lower",
                name: "elev_l"
            },
            {
                data: "elev_u",
                title: "Elevation Upper",
                name: "elev_u"
            },
            {
                data: "iwi_l",
                title: "IWI Lower",
                name: "iwi_l"
            },
            {
                data: "iwi_u",
                title: "IWI Upper",
                name: "iwi_u"
            },
            {
                data: "bmmi_l",
                title: "BMMI Lower",
                name: "bmmi_l"
            },
            {
                data: "bmmi_u",
                title: "BMMI Upper",
                name: "bmmi_u"
            },
            {
                data: "probability",
                title: "Probability",
                name: "probability"
            },
            {
                data: "Crit_1SD",
                title: "Crit_1SD",
                name: "Crit_1SD"
            },
            {
                data: "Crit_2SD",
                title: "Crit_2SD",
                name: "Crit_2SD"
            },
            {
                data: "Crit_Ave",
                title: "Crit_Ave",
                name: "Crit_Ave"
            },
            {
                data: "Crit_P0",
                title: "Crit_P0",
                name: "Crit_P0"
            },
            {
                data: "Crit_P1",
                title: "Crit_P1",
                name: "Crit_P1"
            },
            {
                data: "crit_1sd",
                title: "crit_1sd",
                name: "crit_1sd"
            },
            {
                data: "crit_2sd",
                title: "crit_2sd",
                name: "crit_2sd"
            },
            {
                data: "crit_ave",
                title: "crit_ave",
                name: "crit_ave"
            },
            {
                data: "crit_p0",
                title: "crit_p0",
                name: "crit_p0"
            },
            {
                data: "crit_p1",
                title: "crit_p1",
                name: "crit_p1"
            }
        ],
        "columnDefs": [
            {
                "targets": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
                "visible": false
            },
            {
                "render": function (data, type, row) {
                    return row["genus"] + " " + data;
                },
                "targets": 1
            },
            {
                "bSortable": false,
                "aTargets": [0, 1]
            },
            {
                "render": function(data, type, row){
                    return Number(data).toFixed(2);
                },
                "targets": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
            }
        ],
        sorting: false,
        searching: false,
        paging: false,
        bInfo: false,
        "order": [[0, 'asc']]
    };
    $('#filteredFishTable').closest('div').show();
    $('#filteredFishTable').DataTable(config);
}

function populateCalcTable(data) {
    var d2 = JSON.parse(JSON.stringify(data));
    $('#calc_table').DataTable().destroy();
    $('#calc_table').empty();
    var config = {
        data: d2,
        "columns": [
            {
                data: "common_name",
                title: "Common Name",
                name: "common_name"
            },
            {
                data: "thinning",
                title: "Thin Coef.",
                name: "beta"
            },
            {
                data: "thin_adj",
                title: "Thin Adj",
                name: "delta"
            },
            {
                data: "mean_weight",
                title: "Mean Weight(g)",
                name: "mean_weight"
            },
            {
                data: "biomass",
                title: "Biomass(kg)",
                name: "biomass",
                defaultContent: ''
            },
            {
                data: "count",
                title: "Count",
                name: "count",
                defaultContent: ''
            }
        ],
        "columnDefs": [
            {
                "targets": [0],
                "visible": false
            },
            {
                "bSortable": false,
                "aTargets": [0, 1, 2, 3, 4, 5]
            }
        ],
        sorting: false,
        searching: false,
        paging: false,
        bInfo: false,
        "order": [[0, 'asc']]
    };
    $('#calc_table').DataTable(config);
}

function addStreamSeg(streamData) {
    var latlon = streamData.output.ary_flowlines[0].shape.coordinates.map(function (c) {
        return c.reverse();
    });
    var huc8 = getStreamHuc(streamData.output.ary_flowlines[0].wbd_huc12);
    var huc8geom;
    if (huc8[0][0] < 0) {
        huc8geom = huc8.map(function (c) {
            return c.reverse();
        });
    }
    else {
        huc8geom = huc8;
    }

    if (map.hasLayer(selectedStream)) {
        map.removeLayer(selectedStream);
        map.removeLayer(streamHuc);
    }

    selectedStream = L.polyline(latlon, {
        color: '#02bfe7',
        weight: 5,
        opacity: 0.9,
        lineJoin: 'round'
    }).addTo(map);
    streamHuc = L.polygon(huc8geom, {
        color: 'white',
        weight: 2,
        opacity: 0.9,
        fillColor: '#9ecae1',
        fillOpacity: 0.3
    }).addTo(map);
    map.fitBounds(selectedStream.getBounds());
}

function getStreamHuc(hucID) {
    var huc8 = null;
    L.geoJSON(huc8s, {
        filter: function (feature, layer) {
            if (feature.properties.HUC_CODE === hucID.substring(0, 8)) {
                huc8 = feature.geometry.coordinates[0];
            }
        }
    });
    selectedHuc = hucID.substring(0, 8);
    return huc8;
}

function startCalculation() {
    if ($('#biomass_weight_field').val() !== "") {
        calculateAbundanceFromBiomass(10000);
    }
    else if ($('#biomass_count_field').val() !== "") {
        calculateAbundanceFromCount(Number($('#biomass_count_field').val()));
    }
    endLoad();
}

function calculateAbundanceFromCount(c) {
    var fishList = $('#calc_table').DataTable();
    var beta = fishList.column(1).data();
    var delta = fishList.column(2).data();
    var mW = fishList.column(3).data();

    // Calculating abundance for each fish.
    var A = mW.map(function (W, i) {
        return Math.pow(W, -(beta[i] - delta[i]));
    });
    // Sum of abundance
    var sumA = A.reduce(function (pv, cv) {
        return pv + cv;
    }, 0);

    // Relative abundance
    var RA = A.map(function (a) {
        return a / sumA;
    });

    // Species Count
    var count = RA.map(function (ra) {
        return Math.round(ra * c);
    });

    // Biomass for each species
    var BM = count.map(function (cnt, i) {
        return Number(((cnt * mW[i]) / 1000).toFixed(1));
    });

    var sumBM = BM.reduce(function (sum, v) {
        return sum + v;
    });

    $('#biomass_weight_field').val(sumBM.toFixed(1));

    $("#calc_table").DataTable().rows().every(function (rowIdx, tableLoop, rowLoop) {
        var rowData = this.data();
        rowData["biomass"] = BM[rowIdx];
        rowData["count"] = count[rowIdx];
        $('#calc_table').DataTable().row(this).data(rowData).draw();
    });
    $("#calc_table").DataTable().draw();
}

function calculateAbundanceFromBiomass(c) {
    var B = Number($('#biomass_weight_field').val());

    var fishList = $('#calc_table').DataTable();
    var beta = fishList.column(1).data();
    var delta = fishList.column(2).data();
    var mW = fishList.column(3).data();

    // Calculating abundance for each fish.
    var A = mW.map(function (W, i) {
        return Math.pow(W, -(beta[i] - delta[i]));
    });
    // Sum of abundance
    var sumA = A.reduce(function (pv, cv) {
        return pv + cv;
    }, 0);

    // Relative abundance
    var RA = A.map(function (a) {
        return a / sumA;
    });

    var E = 0; // ERROR value;
    while (E < 0.95 || E > 1.05) {
        // Species Count
        var count = RA.map(function (ra) {
            return Math.round(ra * c);
        });

        var BM = count.map(function (cnt, i) {
            return Number(((cnt * mW[i]) / 1000).toFixed(1));
        });
        // Sun of biomass
        var sumBM = BM.reduce(function (pv, cv) {
            return pv + cv;
        }, 0);

        // Adjustment of ERROR. Count is modified by the ERROR value.
        E = B / sumBM;
        c = E * c;
    }

    $('#biomass_count_field').val(Math.round(c));
    $("#calc_table").DataTable().rows().every(function (rowIdx, tableLoop, rowLoop) {
        var rowData = this.data();
        rowData["biomass"] = BM[rowIdx];
        rowData["count"] = count[rowIdx];
        $('#calc_table').DataTable().row(this).data(rowData).draw();
    });
    $("#calc_table").DataTable().draw();
}

var loadScreen;

function startLoad() {
    document.getElementById("loader").style.display = "block";
    document.getElementById("loader_background").style.display = "block";
    loadScreen = setTimeout(endLoad, 30000)
}

function endLoad() {
    document.getElementById("loader").style.display = "none";
    document.getElementById("loader_background").style.display = "none";
    clearTimeout(loadScreen);
}