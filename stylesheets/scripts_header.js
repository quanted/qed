// Default values
var name = 'ubercookie';
var days = 7;
var mouseOn, mouseOff;
getCookie('ubercookie');

// Enable/Disable Stylesheets      <--- NOT USED ANYMORE
function SetStyle(value)
{
  var i, link_tag;
  for (i = 0, link_tag = document.getElementsByTagName("link");
    i < link_tag.length ; i++ ) {
    if (link_tag[i].rel.indexOf( "stylesheet" ) != -1) {
      link_tag[i].disabled = true;
      if (link_tag[i].className == value) {
        link_tag[i].disabled = false;
      } else {
        link_tag[i].disabled = true;
      }
    }
    if (value == "EPA") {
      mouseOff = '#4289AA';
      mouseOn = '#356697';
    } else {
      mouseOff = '#79973F';
      mouseOn = '#FFA500';
    }
    setCookie(name,value,days);
  }
}
// Set EPA Skin Cookie
function setCookie(name,value,days) {
  if (days) {
    var date = new Date();
    date.setTime(date.getTime()+(days*24*60*60*1000));
    var expires = "; expires="+date.toGMTString();
  }
  else var expires = "";
  document.cookie = name+"="+value+expires+"; path=/";
}
// Get EPA Skin Cookie Value      <--- NOT USED ANYMORE
function getCookie(name) {
  var c_value = document.cookie;
  var c_start = c_value.indexOf(" " + name + "=");
  if (c_start == -1) {
    c_start = c_value.indexOf(name + "=");
    }
  if (c_start == -1) {
    c_value = null;
    }
  else {
    c_start = c_value.indexOf("=", c_start) + 1;
    var c_end = c_value.indexOf(";", c_start);
    if (c_end == -1)
    {
  c_end = c_value.length;
  }
  c_value = unescape(c_value.substring(c_start,c_end));
  }
  // Setup initial link text hover values
  if (c_value == "EPA") {
    mouseOff = '#4289AA';
    mouseOn = '#356697';
  } else {
    mouseOff = '#79973F';
    mouseOn = '#FFA500';
  }
  return c_value;
}
// Delete Cookie       <--- NOT USED ANYMORE
function delCookie(name) {
  setCookie(name,"default",7);
}
//
// jQuery
//
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
    $(this).stop().animate({ color: mouseOn },500);
  }, function(){
    $(this).stop().animate({ color: mouseOff },500);
  });
  // EPA Skin Set
  $("#epaSkin").click(function () {
    setCookie('ubercookie','EPA',7);
    $('.ssMain').attr({href:"/stylesheets/styleEPA.css"});
    $('.ssSkin').attr({href:"/stylesheets/style_ecoEPA.css"});
    $('.fadeMenu').css( {backgroundColor:'#dee7ef', 'color':'#1F262A'} );
    $('.articles a:link, .articles_input a:link, articles_output a:link').css( {'color':'#356697'} );
    mouseOff = '#4289AA';
    mouseOn = '#356697';
  });
  // Default Skin Set
  $("#defSkin").click(function () {
      $('.ssMain').attr({href:"/stylesheets/style.css"});
      $('.ssSkin').attr({href:"/stylesheets/style_eco.css"});
      $('.fadeMenu').css( {'backgroundColor':'rgb(201,224,179)', 'color':'#333333'} );
      $('.articles a:link, .articles_input a:link, articles_output a:link').css( {'color':'#79973F'} );
      mouseOff = '#79973F';
      mouseOn = '#FFA500';
      setCookie('ubercookie','default',7);
  });
  // Save Metadata
  $('#metaDataTxtArea').prop('disabled', true);
  $('#metaDataToggle').change(function() {
    if ($('#metaDataToggle').prop( "checked" )) {
      $('#metaDataTxtArea').prop('disabled', false);
      $('#metaDataDiv').slideDown();
    } else {
      $('#metaDataDiv').slideUp();
      $('#metaDataTxtArea').prop('disabled', true);
    }
  });
});
