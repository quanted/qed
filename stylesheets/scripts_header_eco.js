$(document).ready(function() {
  $('#topheader_p p, .logreg').hide();
  $('.index_link').click(function(e) {
    e.preventDefault();
    var destination = $(this).attr('href');
    setTimeout(function() { window.location.href = destination; }, 500);
    $('#topheader_pic, #topheader_p').animate({
      height:'240px'
    }, 500);
    $('#topheader_p p, .logreg').fadeIn(500);
  });
  $('.articles a, .articles_input a, articles_output a').hover(function(){
    $(this).stop().animate({ color:'#FFA500' },500);
  }, function(){
    $(this).stop().animate({ color:'#79973F' },500);
  });
});