/**************************************************************
 * Simple dialog which becomes visible above the item clicked
 *
 * Created on 2/7/12 -- SJC
 *
 * Ex css styling:
 *   .fdialog {
 *     overflow: hidden;
 *     display: none;
 *     position: absolute;
 *     z-index: 500;
 *   }
 *   .dialogTop {background: transparent url(images/dialogTop.png) no-repeat top; height:37px;}
 *   .dialogMid {background: transparent url(images/dialogMid.png) repeat-y; padding: 0 25px 0px 25px;}
 *   .dialogBtm {background: transparent url(images/dialogBtm.png) no-repeat bottom; height: 32px;}
 *
 *
 * Ex Use:
 *   $('.some_class').simpleDialog({}, function(el, innerDialog) {
 *     var url = $(el).attr("href");
 *     var html = $("#find_some_class_tmpl").tmpl({
 *       //data
 *     });
 *
 *     $.simpleDialog('setTitle', "Some Dialog Title");
 *     $(innerDialog).html(html);
 *
 *     return false;
 *   });

 * Or with display options:
 *   $('.some_class').simpleDialog({speed: 100, delay: 50}, function(el, innerDialog){
 *     var url = $(el).attr("href");
 *     var html = $("#find_some_class_tmpl").tmpl({
 *       //data
 *     });
 *
 *     $.simpleDialog('setTitle', "Some Dialog Title");
 *     $(innerDialog).html(html);
 *
 *     return false;
 *   });
 **************************************************************/

jQuery.noConflict();
(function($) {
  $.fn.simpleDialog = function(method) {

    if ($("#simpleDialog-overlay").length < 1) {
      $("body").prepend(methods.getDialog());
    }
    if ($('#completeOverlay').length < 1) {
      methods.getCompleteOverlay().appendTo("body");
    }

    if (methods[method]) {
      return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
    } else if ( typeof method === 'object' || !method) {
      return methods.init.apply(this, arguments);
    } else {
      $.error('Method ' + method + ' does not exist on jQuery.simpleDialog');
    }
  };

  /*var overlay = $('#simpleDialog-overlay');
   var dialog = $('.simpleDialog');
   var dialogInner = $('.simpleDialog .inner');
   var closeButton = $('#simpleDialog-overlay > a.hideSimpleDialog');*/

  var defaults = {
    maxWidth : 800,
    maxHeight : 600,
    speed : 100,
    delay : 0
  };

  var methods = {
    init : function(options, contents_callback) {

      /* Give each item with the class associated with
       the plugin the ability to call the dialog    */
      return $(this).each(function() {
        var contents_func;

        var $this = $(this);

        $this.sm_options = $.extend(defaults, options);
        contents_func = contents_callback;

        /* Mouse over and out functions*/
        $this.unbind('click.simpleDialog').bind('click.simpleDialog', function() {
          contents_func($this, $('.simpleDialog .inner'));
          methods.setDialog($this.sm_options.maxHeight, $this.sm_options.maxWidth);
          setDialogTimer();
          return false;
        });
        $('.hideSimpleDialog').unbind('click.simpleDialog').bind('click.simpleDialog', function() {
          stopDialogTimer();
          methods.hideDialog($this.sm_options.speed);
          return false;
        });

        setDialogTimer = function() {
          $this.showDialogTimer = setInterval("showDialog()", $this.sm_options.delay);
        }, stopDialogTimer = function() {
          clearInterval($this.showDialogTimer);
        }
        /* This function stops the timer and creates the
         fade-in animation                          */
        showDialog = function() {
          stopDialogTimer();
          methods.showDialog($this.sm_options.speed);
        }
      });
    },

    getDialog : function() {
      var tDialog =
      '<div id="simpleDialog-overlay">' +
        '<a class="hideSimpleDialog" href="#">' +
        '<img alt="close" src="images/Button Close.png" border="0">' +
        '</a>'+
        '<h3 id="simpleDialog-title">Title</h3>' +
        '<div class="simpleDialog">' +
          '<div class="inner" />' +
        "</div>" +
      '</div>';
      return tDialog;
    },

    getCompleteOverlay : function() {
      return $('<div id="complete-overlay" />');
    },

    showDialog : function(speed) {
      $('#content').hide();
      $('#simpleDialog-overlay').hide();
      $('#simpleDialog-overlay').animate({
        "top" : "+=20px",
        "opacity" : "show"
      }, speed);
      $('#complete-overlay').css({
        'top' : $(window).scrollTop() + "px",
        'left' : $(window).scrollLeft() + "px"
      });
      $('#complete-overlay').show();
    },

    hideDialog : function(speed) {
      $('#content').show();
      $('#simpleDialog-overlay').animate({
        "opacity" : "hide"
      }, speed);
      $('#complete-overlay').hide();
    },

    setTitle : function(html) {
      $("#simpleDialog-title").html(html);
    },

    /* Delay the fade-in animation of the dialog */

    /* Position the dialog relative to the class
     associated with the dialog                */
    setDialog : function(maxHeight, maxWidth) {
      var top, leftOffset, topOffset, left, x, y;

      top = $(window).height() / 2;
      left = $(window).width() / 2;
      top += $(window).scrollTop();
      left += $(window).scrollLeft();

      $('.simpleDialog').css({
        'height' : '',
        'width' : ''
      });
      if ($('.simpleDialog').height() > maxHeight) {
        $('.simpleDialog').css({
          'height' : maxHeight + "px"
        });
      }
      if ($('.simpleDialog').width() > maxWidth) {
        $('.simpleDialog').css({
          'width' : maxWidth + "px"
        });
      }

      leftOffset = $('#simpleDialog-overlay').outerWidth() / 2;
      topOffset = $('#simpleDialog-overlay').outerHeight() / 2;
      x = (left - leftOffset);
      y = (top - topOffset);
      $('#simpleDialog-overlay').css({
        'top' : y + "px",
        'left' : x + "px"
      });
    }
  };

})(jQuery);
