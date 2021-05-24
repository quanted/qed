function define_functions(){

    //slider label function
    $(function slider_label()
    {
        $('.slider_bar').on('input change', function(){
            $(this).next($('.slider_label')).html(this.value);
        });
        $('.slider_label').each(function(){
            var value = $(this).prev().attr('value');
            $(this).html(value);
        });
    }).trigger('input change');

}


$(document).ready(function(){
    $("#id_min_replicate_hits").before("<p>");
    $("#id_min_replicate_hits").after("<span  class='slider_label'></span></p>");
    $("#id_parent_ion_mass_accuracy").before("<p>");
    $("#id_parent_ion_mass_accuracy").after("<span  class='slider_label'></span></p>");
    define_functions();
    //$("#id_min_replicate_hits").after("<p> text</p>");
});