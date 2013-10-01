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
  var browserWidth = $(window).width();
  var browserHeight = $(window).height();
  var winleft = (browserWidth / 2) - 220 + "px";
  var wintop = (browserHeight / 2) - 30 + "px";
  $("a[class^='fadeQAQC']").click(function () {
    $.blockUI({
      css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "60px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
      message: '<h2 class="popup_header">Processing Request...</h2><br/><img src="/images/loader.gif" style="margin-top:-16px">'
    });
  });
});