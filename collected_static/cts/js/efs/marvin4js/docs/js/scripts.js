var formatXml = this.formatXml = function (xml) {
        var reg = /(>)(<)(\/*)/g;
        var wsexp = / *(.*) +\n/g;
        var contexp = /(<.+>)(.+\n)/g;
        xml = xml.replace(reg, '$1\n$2$3').replace(wsexp, '$1\n').replace(contexp, '$1\n$2');
        var pad = 0;
        var formatted = '';
        var lines = xml.split('\n');
        var indent = 0;
        var lastType = 'other';
        // 4 types of tags - single, closing, opening, other (text, doctype, comment) - 4*4 = 16 transitions 
        var transitions = {
            'single->single': 0,
            'single->closing': -1,
            'single->opening': 0,
            'single->other': 0,
            'closing->single': 0,
            'closing->closing': -1,
            'closing->opening': 0,
            'closing->other': 0,
            'opening->single': 1,
            'opening->closing': 0,
            'opening->opening': 1,
            'opening->other': 1,
            'other->single': 0,
            'other->closing': -1,
            'other->opening': 0,
            'other->other': 0
        };

        for (var i = 0; i < lines.length; i++) {
            var ln = lines[i];
            var single = Boolean(ln.match(/<.+\/>/)); // is this line a single tag? ex. <br />
            var closing = Boolean(ln.match(/<\/.+>/)); // is this a closing tag? ex. </a>
            var opening = Boolean(ln.match(/<[^!].*>/)); // is this even a tag (that's not <!something>)
            var type = single ? 'single' : closing ? 'closing' : opening ? 'opening' : 'other';
            var fromTo = lastType + '->' + type;
            lastType = type;
            var padding = '';

            indent += transitions[fromTo];
            for (var j = 0; j < indent; j++) {
                padding += '\t';
            }
            if (fromTo == 'opening->closing')
                formatted = formatted.substr(0, formatted.length - 1) + ln + '\n'; // substr removes line break (\n) from prev loop
            else
                formatted += padding + ln + '\n';
        }

        return formatted;
    };


	function updateAuthInfo(state, username) {
		if (state==true) {
			$(".login_info").html("You are authenticated as " + username);
		} else {
			$(".login_info").html("You are not authenticated");			
		}
	}	
	
$(function() {
	var form_username = $( "#username" ),
	form_password = $( "#password" );

	$( "#dialog-form" ).dialog({
	  autoOpen: false,
	  height: 320,
	  width: 400,
	  modal: true,
	  buttons: {
		Login: function() {
			$.ajax({
				url: serviceConfig.contextPath + "/rest-v0/login",
				type: 'POST',
				data: JSON.stringify({"username": form_username.val(), "password": form_password.val()}),
				dataType: "json",
				contentType: 'application/json'})
			.done(function(data){
				authenticated=true;
				updateAuthInfo(true, data.username); 
				alert("Authentication was successful! Now you can test the interactive functionality!")
			})
			.fail(function(data){
				authenticated=false;
				updateAuthInfo(false, "");
				alert("Authentication was NOT successful!")
			});
			$(this).dialog( "close" );
		},
		Cancel: function() {
		  $(this).dialog( "close" );
		}
	  },
	  close: function() {
	  }
	});

	$.getJSON( serviceConfig.contextPath + "/rest-v0/").done(function( data ) {
		if ("authInfo" in data){
			authenticated=true;
			updateAuthInfo(authenticated, data.authInfo.username);
		}
	});

	if (serviceConfig && serviceConfig.contextPath !== '${contextPath}') {
		var serviceUrl = serviceConfig.contextPath + serviceConfig.serviceLocation;
		$("#baseurl").val(serviceUrl);
	}

	var baseurl;
	$("#baseurl").on("keyup", function() {
		baseurl = $(this).val();

		$("input[data-baseurl]").each(function() {
			var self = $(this);
			var value = self.val();

			if (typeof self.data("original-value") == "undefined") {
				self.data("original-value", value);
			} else {
				value = self.data("original-value");
			}
			self.val(baseurl + value);
		});
	}).keyup();

	$("form").on("submit", function() {
		$("input[type='button']:first").click();
		return false;
	});


	var indentAmount = 4;

	var handleFail = function(outputDiv, jqXHR, textStatus, errorThrown){
			var editor = ace.edit(outputDiv.get(0));
			if(jqXHR.status == 401){
				var errorInfo = JSON.parse(jqXHR.responseText);
				$( "#dialog-message" ).html(errorInfo.errorMessage);
				$( "#dialog-form" ).dialog( "open" );
				editor.getSession().setValue("");
			} else {
				outputDiv.addClass('error');
				editor.getSession().setValue(jqXHR.responseText=="" ? jqXHR.statusText : jqXHR.responseText);				
			}
		};
	
	var startLoading = function(outputDiv){
			outputDiv.removeClass('error');
			var editor = ace.edit(outputDiv.get(0));
			editor.getSession().setValue('Loading...');
		};
		
	var handleDone = function(outputDiv, data, textStatus, jqXHR){
			var editor = ace.edit(outputDiv.get(0));
			if (outputDiv.is(".text")) {
				editor.getSession().setValue(formatXml(data));
			} else {
				var resptext = JSON.stringify(data, null, indentAmount);
				editor.getSession().setValue(resptext);
			}
		};

	$('.GET').on("click", function(evt) {
		evt.preventDefault();
		var form = $(this).parents("form");
		var outputDiv = $('.output_div', form);
		startLoading(outputDiv);

		$.ajax({
			url: $.trim(encodeURI($.trim($(".url", form).val()))),
			type: 'GET'
		}).done(function(data, textStatus, jqXHR) {
			handleDone(outputDiv, data, textStatus, jqXHR);
		}).fail(function(jqXHR, textStatus, errorThrown) {
			handleFail(outputDiv, jqXHR, textStatus, errorThrown);
		}); 
	});

	$('.POST').on("click", function(evt) {
		evt.preventDefault();

		var form = $(this).parents("form");
		var outputDiv = $('.output_div', form);
		startLoading(outputDiv);

		var paramsDiv = $('.params_div', form);
		if(paramsDiv.length > 0){
			var paramsEditor = ace.edit(paramsDiv.get(0));
			var params = paramsEditor.getSession().getValue();
		}
		
		$.ajax({
			url: $.trim(encodeURI($.trim($(".url", form).val()))),
			type: 'POST',
			data: params,
			dataType: outputDiv.is(".text") ? "text" : "json",
			contentType: paramsDiv.is(".any") ? '*/*' : 'application/json'
		}).done(function(data, textStatus, jqXHR) {
			handleDone(outputDiv, data, textStatus, jqXHR);
		}).fail(function(jqXHR, textStatus, errorThrown) {
			handleFail(outputDiv, jqXHR, textStatus, errorThrown);
		});		
	});

});
