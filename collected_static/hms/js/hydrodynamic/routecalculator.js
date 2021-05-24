$(document).ready(function () {

    $('#id_date').closest('tr').hide();
    $(window).bind('beforeunload', function () {
        $(":reset").click();
    });

    $('#id_model').change(function () {
        if (this.value === "day") {
            $("#id_local_time").closest('tr').hide();
            $("#id_year").closest('tr').hide();
            $("#id_date").closest('tr').show();
        }
        else {
            $("#id_local_time").closest('tr').show();
            $("#id_year").closest('tr').show();
            $('#id_date').closest('tr').hide();
        }
    });

    $('#id_model').trigger("change");

});