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
  $('.articles a').hover(function(){
    $(this).stop().animate({ color:'#A31E39' },500);
  }, function(){
    $(this).stop().animate({ color:'#485C5A' },500);
  });
});