$(document).ready(function () {
    
    //Highlights collasible header on output pages during
    //mouseover event
    $('.collapsible').hover(
        function() {
            $(this).data('bgcolor', $(this).css('background-color')).css({
                'background-color': '#9AB2CB',
                'cursor': 'pointer'
            });
        },
        function() {
            $(this).css('background-color', $(this).data('bgcolor'));
        }
    );
    
});