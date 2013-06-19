$(document).ready(function() {
  $('#l_menu a, .logreg').click(function(e) {
    e.preventDefault();
    var destination = $(this).attr('href');
    setTimeout(function() { window.location.href = destination; }, 500);
    $('#topheader_pic_main, #topheader_p_main').animate({
      height:'140px'
    }, 500);
    $('#topheader_p_main p, .logreg').fadeIn(500);
  });
  $('.articles a').hover(function(){
    $(this).stop().animate({ color:'#586B73' },500);
  }, function(){
    $(this).stop().animate({ color:'#EDB200' },500);
  });
});