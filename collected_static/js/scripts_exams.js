$(document).ready(function() {

    var i = 1;
    $('.n_ph').append('<tr id="n_ph_header" style="display:none"><th>pH</th><th>Half-life (days)</th></tr>');

    $('#n_ph').val(3);
    $('tr[id*="n_ph_header"]').show();
    while (i <= 3) {
            $('.n_ph').append('<tr class="tab_n_ph"><td><input type="text" size="5" name="ph' + i + '" id="id_ph' + i + '"/></td><td><input type="text" size="5" name="hl' + i + '" id="id_hl' + i + '"/></td></tr>');
        i = i + 1;
    }
    while (i-1 > 3) {
        $(".n_ph tr:last").remove();
        i=i-1
    }
    $('</table>').appendTo('.n_ph');

    $('#id_ph1').val(5);
    $('#id_ph2').val(7);
    $('#id_ph3').val(9);
    $('#id_hl1').val(0);
    $('#id_hl2').val(0);
    $('#id_hl3').val(0);

    $('#n_ph').change(function () {
    	var total = $(this).val();
    	$('tr[id*="n_ph_header"]').show();
    	while (i <= total) {
                $('.n_ph').append('<tr class="tab_n_ph"><td><input type="text" size="5" name="ph' + i + '" id="id_ph' + i + '"/></td><td><input type="text" size="5" name="hl' + i + '" id="id_hl' + i + '"/></td></tr>');
    		i = i + 1;
    	}
    	while (i-1 > total) {
    		$(".n_ph tr:last").remove();
    		i=i-1
    	}
    	$('</table>').appendTo('.n_ph');
    })
});