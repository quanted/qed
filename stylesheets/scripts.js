$( document ).ready(function() {
  $('div#l_menu ul li a:not(aSelected)').bind('click', function(){
     $('div#l_menu ul li a.aSelected').removeClass('aSelected');
     $(this).addClass('aSelected');
  });
});