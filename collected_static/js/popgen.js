$("#productH2").css("display", "none");

$("input[name=inlineRadioOptions]").change(function() {
  var divId = $(this).attr("id");
  $("div.pc").hide();
  $("." + divId).show();
});