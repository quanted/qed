$(document).ready(function() {
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
  $('#about').hover(
    function() {
        $('#about_text').stop().animate({width: '3.5em' }, {duration: 500, queue: false}).fadeTo(500,1);
    },
    function () {
        $('#about_text').stop().animate({width:0}, {duration: 500, queue: false}).fadeTo(500,0);
    }
  );
});