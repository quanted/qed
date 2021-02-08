$(document).ready(function () {

    $('#id_stationID').closest('tr').hide();

    $('#id_source').on("change", function () {
        var source = this.selectedIndex;
        if (this[source].value === "ncdc") {
            $('#id_latitude').closest('tr').hide();
            $('#id_longitude').closest('tr').hide();
            $('#id_stationID').closest('tr').show();
        }
        else {
            $('#id_latitude').closest('tr').show();
            $('#id_longitude').closest('tr').show();
            $('#id_stationID').closest('tr').hide();
        }
    });


    $(window).bind('beforeunload', function () {
        $(":reset").click();
    });

});