$(document).ready(function() {
  // Home
  $('#home').hover(
    function() {
        $('#home_text').stop().animate({width: '3.5em' }, {duration: 500, queue: false}).fadeTo(500,1);
    },
    function () {
        $('#home_text').stop().animate({width:0}, {duration: 500, queue: false}).fadeTo(500,0);
    }
  ).mousedown(function() {
    $(this).addClass('textshadow');
  }).mouseup(function() {
    $(this).removeClass('textshadow');
  }).mouseleave(function() {
    $(this).removeClass('textshadow');
  });
  // About
  $('#about').hover(
    function() {
        $('#about_text').stop().animate({width: '3.5em' }, {duration: 500, queue: false}).fadeTo(500,1);
    },
    function () {
        $('#about_text').stop().animate({width:0}, {duration: 500, queue: false}).fadeTo(500,0);
    }
  );
  // Links
  $('.articles a, .articles_input a, articles_output a').hover(function(){
    $(this).switchClass('tabUnsel', 'linkHover');
  }, function(){
    $(this).switchClass('linkHover', 'tabUnsel');
  });
});
