$(document).ready(function() {
  // Remove Log-in
  $('#topheader_p p, .logreg').hide();
  // Index link
  $('.index_link').click(function(e) {
    e.preventDefault();
    var destination = $(this).attr('href');
    setTimeout(function() { window.location.href = destination; }, 500);
    $('#topheader_pic, #topheader_p').animate({
      height:'240px'
    }, 500);
    $('#topheader_p p, .logreg').fadeIn(500);
  });
  // BlockUI setup
  var browserWidth = $(window).width();
  var browserHeight = $(window).height();
  var winleft = (browserWidth / 2) - 220 + "px";
  var wintop = (browserHeight / 2) - 30 + "px";
  // BlockUI on QAQC
  $("a[class^='fadeQAQC']").click(function (e) {
    e.preventDefault();
    $(document).ajaxStart(function(){
      $.blockUI({
        css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "60px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
        message: '<h2 class="popup_header">Processing QA/QC...</h2><br/><img src="/images/loader.gif" style="margin-top:-16px">'
      });
    });
      var retStatus;
      var currPage = pathSlice.slice(0, -5).split('_');
      var model = currPage[0];
      $.ajax({
          cache: false,
          complete: function(xhr) { 
            retStatus = xhr.status;
          },
          success: function() {
            // $.unblockUI();
            window.location.href = model+"_qaqc.html";
          },
          error: function() {
            $.unblockUI();
            alert('There is a problem about your submission.')
          }
        });
      if(retStatus == 200)
            return false;
      else
          return true;
  });
  // BlockUI on Form Submit
  $("input[value='Submit']").click(function (e) {
    e.preventDefault();
    $.blockUI({
      css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "60px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
      message: '<h2 class="popup_header">Processing Model Submission...</h2><br/><img src="/images/loader.gif" style="margin-top:-16px">'
    });
    setTimeout(function() { $('form').submit(); }, 500);
  });
});