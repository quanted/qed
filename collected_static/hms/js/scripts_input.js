$( document ).ready(function() {

  // BlockUI on Form Submit
  $(".submit").click(function (e) {
    e.preventDefault();
    // var form_valid = $("form").valid();
    var form_valid;
    if (typeof form_valid == 'undefined'){
      $.blockUI({
//        css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "60px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
        css: {"padding": "8px"},
				message: '<h2 class="popup_header">Processing Model Submission...</h2><br/><img src="/static_qed/images/loader.gif" style="margin-top:-16px">',
        fadeIn:  500
      });
      setTimeout(function() {$('form').submit();}, 500);
    }

    // if (typeof form_valid !== 'undefined' && form_valid !== false){
    else {
      e.preventDefault();
      // ES Mapper check
      if (model == "es_mapping") {
        var html_input = $("form").html();
        localStorage.html_input=html_input;

        var html_new = $("form").serialize();

        localStorage.html_new=html_new;
        console.log(localStorage);
      }
      $.blockUI({
//        css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "60px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
        css: {"padding": "8px"},
        message: '<h2 class="popup_header">Processing Model Submission...</h2><br/><img src="/static_qed/images/loader.gif" style="margin-top:-16px">',
        fadeIn:  500
      });
      setTimeout(function() {$('form').submit();}, 500);
    }
  });

  $('#resetbutton').click(
    function(){
      var values = [];
      var selected = $("input:checkbox").each(
       function(){
        values.push( $(this).is(':checked'));
      });
      this.form.reset();
      for (i=0;i<selected.length;i++) {
        $(selected[i]).prop('checked', values[i]);
      }
  });

  $('#clearbutton').click(
    function(){
    $(this.form).find(':input').each(function() {
      switch(this.type) {
        case 'text':
        case 'textarea':
          $(this).val('');
          break;
        case 'radio':
          this.checked = false;
      }
    });
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