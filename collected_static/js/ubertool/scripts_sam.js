$(document).ready(function() {
	// Call function to setup tabbed nav
	uberNavTabs(
		["Chemical", "Application", "Simulation", "Output"],
		{   "isSubTabs":false   }
	);

    // BETA disclaimer
    //setTimeout(function() {alert("Disclaimer: " +
    //    "Ecological risk calculations contained here should be used for no purpose other than quality " +
    //    "assurance and peer review of the presented web applications. This web site is under " +
    //    "development. It is available for the purposes of receiving feedback and quality assurance from " +
    //    "personnel in the EPA Office of Chemical Safety and Pollution Prevention and from interested " +
    //    "members of the ecological risk assessment community."
    //)}, 500);


	// Default inputs
	$('#id_sim_type_0, #id_output_format_0, #id_output_format_1, #id_output_format_2').prop('checked', true);
	// $('#id_region').val('NHD Region 07');
	//$('#id_crop_number').css('color', 'grey');
	//$('#id_crop').closest('tr').after('<tr><th>Chosen Crop(s):</th><td id="crop1"></td></tr>');
	// $('#id_output_tox_value').closest('tr').after(
	// 	'<tr><th>Output Summary:</th><td>21-d Average Concentrations - 90<sup>th</sup> percentile</td></tr>' +
	// 	'<tr><th></th><td>60-d Average Concentrations - 90<sup>th</sup> percentile</td></tr>' +
	// 	'<tr><th></th><td>Toxicity Threshold - Average Duration of Daily Exceedances</td></tr>' +
	// 	'<tr><th></th><td>Toxicity Threshold - Percentage of Days with Exceedances</td></tr>'
	// );
	// Formatting
	$('#id_crop_list_no').closest('tr').hide();
	$('#id_coefficient').children().css('display', 'inline');
    var output_pref_trs = $(
        '#id_output_avg_days, #id_output_time_avg_option, #id_output_time_avg_conc,' +
        '#id_output_tox_value, #id_output_tox_thres_exceed'
        ).closest('tr');
	$('#id_output_type').change(function() {
		// Output Preference
		var val = $(this).find('input:checked').val();
		if (val == "1") {
            // Daily Concentrations
            output_pref_trs.hide();
		} else {
            // Time-Averaged Concentrations
            output_pref_trs.show();
        }left
	});
	$('#id_output_time_avg_option').change(function() {
		// Time-Averaged Results
		var val = $(this).find('input:checked').val();
		if (val == "1") {
			
		}
	});
	
	var cropsArray_soybeans = ['Soybeans', 'Soybeans/cotton', 'Soybeans/wheat', 'Soybeans/grains'];
	var cropsArray_corn = ['Corn', 'Corn/soybeans', 'Corn/wheat', 'Corn/grains'];
	var crop_list_array = [];
	var crop_list_no_array = ["10", "14", "15", "18"];
	var samScenarioInputs_atrazine_corn = ["1", "Chemical A", "100", "1", "2", "123", "10 14 15 18", "0", "4", "1", "1", "1.3", "04/20/1984", "uniform_step", "7", "50", "43", "50", "Ohio Valley", "eco", "dwr", "dwf", "01/01/1984", "12/31/2013", "1", "2", "4", "1", "2", "", "4", "4", "1", "2", "3"];
	var samScenarioInputs_chlorpyrifos_corn = ["2", "Chemical B", "6040", "1", "2", "109", "", "0", "4", "1", "1", "1.1", "04/20/1984", "uniform", "30", "100", "", "", "Ohio Valley", "eco", "dwr", "dwf", "01/01/1984", "12/31/2013", "1", "2", "4", "1", "2", "", "4", "4", "1", "2", "3"];
	var samScenarioInputs_chlorpyrifos_soybeans = ["3", "Chemical C", "6040", "1", "2", "109", "", "0", "4", "1", "1", "1.1", "04/20/1984", "uniform", "42", "100", "", "", "Ohio Valley", "eco", "dwr", "dwf", "01/01/1984", "12/31/2013", "1", "2", "4", "1", "2", "", "4", "4", "1", "2", "3"];
	var samScenarioInputs_fipronil_corn = ["4", "Chemical D", "727", "1", "2", "128", "", "0", "4", "1", "1", "0.1", "04/20/1984", "uniform_step", "7", "50", "43", "50", "Ohio Valley", "eco", "dwr", "dwf", "01/01/1984", "12/31/2013", "1", "2", "4", "1", "2", "", "4", "4", "1", "2", "3"];
	var samScenarioInputs_metolachlor_corn = ["5", "Chemical E", "181", "1", "2", "49", "", "0", "4", "1", "1", "1.05", "04/20/1984", "uniform_step", "7", "50", "43", "50", "Ohio Valley", "eco", "dwr", "dwf", "01/01/1984", "12/31/2013", "1", "2", "4", "1", "2", "", "4", "4", "1", "2", "3"];
	var selectedScenarioValue = $('#id_scenario_selection').val();
	if (selectedScenarioValue !== '0') {
		$(':input:not(#id_scenario_selection, :input.submit)').attr('disabled', true);
		switch (selectedScenarioValue) {
			case '1':
				samFillScenarioCrops('1');
				break;
			case '2':
				samFillScenarioCrops('2');
				break;
			case '3':
				samFillScenarioCrops('3');
				break;
			case '4':
				samFillScenarioCrops('4');
				break;
			case '5':
				samFillScenarioCrops('5');
				break;
			default:
				samFillScenarioCrops('0');
		}
	}
	else {
		samFillScenarioCrops('0');
	}

	// Set default start date
	startDate = $("#id_sim_date_start").val();
	$( "#id_sim_date_start" ).datepicker({
		changeYear: true,
		minDate: new Date(1984, 0, 1),
		maxDate: new Date(2013, 11, 31),
		yearRange: '1984:+2013',
		defaultDate: startDate
	});
	// Set default end date
	endDate = $("#id_sim_date_end").val();
	$( "#id_sim_date_end" ).datepicker({
		changeYear: true,
		minDate: new Date(1984, 0, 1),
		maxDate: new Date(2014, 5, 2),
		yearRange: '1960:+nn',
		defaultDate: endDate
	});
	// Set default first app date
	firstAppDate = $("#id_sim_date_1stapp").val();
	$( "#id_sim_date_1stapp" ).datepicker({
		changeYear: true,
		minDate: new Date(1984, 0, 1),
		maxDate: new Date(2013, 11, 31),
		yearRange: '1960:+nn',
		defaultDate: firstAppDate
	});

	// Scenario Selector
	function samFillScenarioValues(scenario) {
		$('form.inputs_form :input').not(':button').each(function(i) {
			$(this).val(scenario[i]);
		});
	}	
	function samFillScenarioCrops(scenario) {
		//resetCropRows();
		var cropsArray;
		
		switch (scenario) {

			case '1':
				$(':input:not(#id_scenario_selection, :input.submit)').attr('disabled', true);
				$('input.submit').attr('disabled', false);
				$('#id_refine_time_window2, #id_refine_percent_applied2').closest('tr').show();
				samFillScenarioValues(samScenarioInputs_atrazine_corn);
                $('#id_crop').val("10 14 15 18");
				//cropsArray = cropsArray_corn;
				//for (i=0;i<cropsArray.length;i++) {
				//	cropArrayGenerator(cropsArray[i]);
				//}
				break;
			case '2':
				$(':input:not(#id_scenario_selection, :input.submit)').attr('disabled', true);
				$('input.submit').attr('disabled', false);
				$('#id_refine_time_window2, #id_refine_percent_applied2').closest('tr').hide();
				samFillScenarioValues(samScenarioInputs_chlorpyrifos_corn);
                $('#id_crop').val("10 14 15 18");
				//cropsArray = cropsArray_corn;
				//for (i=0;i<cropsArray.length;i++) {
				//	console.log(i);
				//	cropArrayGenerator(cropsArray[i]);
				//}
				//cropArrayNumberGenerator(crop_list_array); // Delete this line???
				break;
			case '3':
				$(':input:not(#id_scenario_selection, :input.submit)').attr('disabled', true);
				$('input.submit').attr('disabled', false);
				$('#id_refine_time_window2, #id_refine_percent_applied2').closest('tr').hide();
				samFillScenarioValues(samScenarioInputs_chlorpyrifos_soybeans);
                $('#id_crop').val("40 42 45 48 14");
				//cropsArray = cropsArray_soybeans;
				//for (i=0;i<cropsArray.length;i++) {
				//	cropArrayGenerator(cropsArray[i]);
				//}
				break;
			case '4':
				$(':input:not(#id_scenario_selection, :input.submit)').attr('disabled', true);
				$('input.submit').attr('disabled', false);
				$('#id_refine_time_window2, #id_refine_percent_applied2').closest('tr').show();
				samFillScenarioValues(samScenarioInputs_fipronil_corn);
                $('#id_crop').val("10 14 15 18");
				//cropsArray = cropsArray_corn;
				//for (i=0;i<cropsArray.length;i++) {
				//	cropArrayGenerator(cropsArray[i]);
				//}
				break;
			case '5':
				$(':input:not(#id_scenario_selection, :input.submit)').attr('disabled', true);
				$('input.submit').attr('disabled', false);
				$('#id_refine_time_window2, #id_refine_percent_applied2').closest('tr').show();
				samFillScenarioValues(samScenarioInputs_metolachlor_corn);
                $('#id_crop').val("10 14 15 18");
				//cropsArray = cropsArray_corn;
				//for (i=0;i<cropsArray.length;i++) {
				//	cropArrayGenerator(cropsArray[i]);
				//}
				break;
			default:
				$(':input:not(#id_scenario_selection)').attr('disabled', false);
                $('#id_output_time_avg_conc, ' +
                '#id_output_time_avg_option_0, #id_output_time_avg_option_1,' +
                '#id_sim_type_0, #id_sim_type_1, #id_sim_type_2').attr('disabled', true);
                $('#id_workers').attr('readonly', true).val('16');
                $('#id_processes').attr('readonly', true).val('1');
                $('#id_output_tox_thres_exceed').val('1');
                $('#id_region').attr('readonly', true);
                // Force Refinement method to be 'Uniform with Step'
                $('#id_refine').val('uniform_step');
								$('#id_chemical_name').val('Custom');
				// $('input.submit').attr('disabled', true);
				// Add 'crop_list_no_array' array to 'crop_list_no' input field before submit
				// $('input.submit').click(function(e) {
				$('form').submit(function(e) {
					// console.log(isCropListNoArraySet());
					// e.preventDefault();
					// if (isCropListNoArraySet()) {
					// 	$(this).submit();
					// } else {
					// 	$('#id_crop_list_no').val(crop_list_no_array);
					// 	console.log($('#id_crop_list_no').val());
					// }

                    $('#id_output_time_avg_conc, #id_output_type_0, id_output_type_1' +
                    '#id_output_time_avg_option_0, #id_output_time_avg_option_1,' +
                    '#id_sim_type_0, #id_sim_type_1, #id_sim_type_2').attr('disabled', false);

					$('#id_crop_list_no').val(crop_list_no_array);
					console.log($('#id_crop_list_no').val());
				});
				function isCropListNoArraySet() {

					// var form_crop_list_no_string = $('#id_crop_list_no').val();
					var form_crop_list_no_array = $('#id_crop_list_no').val().split(',');

					for (i;i<crop_list_no_array.length;i++) {
						var crop_id = crop_list_no_array[i];
						if (crop_id == form_crop_list_no_array[i]) {

						} else {
							return false;
						}
						return true;
					}
				}
		}
	}

	$('#id_scenario_selection').change(function() {
			samFillScenarioCrops($(this).val());
	});

	// Selected Crops Rows
	//function cropArrayGenerator(crop) {
		//var scenario = $('#id_scenario_selection').val();
		//if (crop_list_array.length < 4) {
		//	if ($('#crop1').text() == '') {
		//		if (scenario == '0') {
		//			// CUstom scenario
		//			$('#crop1').html(crop + " <span class='deleteCrop'>[x]</span>");
		//		}
		//		else {
		//			// Pre-canned scenario
		//			$('#crop1').html(crop);
		//		}
		//		crop_list_array.push(crop);
		//	} else {
		//		if ($.inArray(crop, crop_list_array) == -1) {
		//			if (scenario == '0') {
		//				// CUstom scenario
		//				$('#crop1').closest('tr')
		//					.after('<tr><th></th><td>' + crop + " <span class='deleteCrop'>[x]</span>" + '</td></tr>');
		//			}
		//			else {
		//				// Pre-canned scenario
		//				$('#crop1').closest('tr')
		//					.after('<tr><th></th><td>' + crop + '</td></tr>');
		//			}
		//			crop_list_array.push(crop);
		//		}
		//	}
		//}
		//if (crop_list_array.length == 4) {
		//	$('#id_crop').prop('disabled', true);
		//}
		//$('#id_crop_number').val(crop_list_array.length);
	//}
	//function cropArrayNumberGenerator(crop_list_array){
	//	// Generate JS array of Crop IDs
	//	for (i=0; i<crop_list_array.length; i++) {
	//		var crop_id = $('#id_crop option:selected').val();
    //
	//		if ($.inArray(crop_id, crop_list_no_array) == -1) {
	//			console.log('i = ' + i);
	//			console.log('crop_id = ' + crop_id);
	//			crop_list_no_array.push(crop_id);
	//		}
	//	}
	//	console.log(crop_list_no_array);
	//}
	$('#id_crop').change(function() {
        crop_list_no_array.length = 0; // Clear existing array
        var crop_IDs_list = $(this).val(); // Get selected crop id values

        for (i=0; i<crop_IDs_list.length; i++) {
            var crop_IDs = crop_IDs_list[i].split(" ");
            for (j=0; j<crop_IDs.length; j++) {
                crop_list_no_array.push(crop_IDs[j]);
            }
        }
        console.log(crop_list_no_array);
        $('#id_crop_number').val(crop_list_no_array.length);
		//if ($(this).val() !== '0') {
		//	//var crop = $("#id_crop option:selected").text();
         //   var crop_IDs = $("#id_crop option:selected").val();
         //   //cropArrayGenerator(crop);
		//	//cropArrayNumberGenerator(crop_list_array);
         //   crop_list_no_array = crop_IDs.split(" ");
         //   //console.log(crop_list_no_array);
         //   $('#id_crop_number').val(crop_list_no_array.length);
		//}
	});
	function resetCropRows() {
		// Remember first row ('tr') is hidden
		var tr1st = $('#crop1').closest('tr').index() + 1;
		var trLast = $('#id_crop_number').closest('tr').index() + 1;
		if (tr1st !== -1) {
			var noOfCrops = trLast - tr1st;
			if (noOfCrops > 1) {
				for (i=0; i<noOfCrops; i++) {
					if (i == 0) {
						$('#crop1').text('');
					}
					else {
						try {
							$('.tab_Application tr')[3].remove();
						}
						catch(e) {
								// IE support
								var appTable = document.getElementsByClassName('tab_Application')[0].children(0);
								var childToRemove = appTable.children(3);
								appTable.removeChild(childToRemove);
						}
					}
				}
				$('#id_crop_number').val('0');
				crop_list_array = [];
			}
		}
	}
	//$('table').on('click', 'span', function() {
	//	// '[x]' to delete crops from "Choosen Crop(s)" list
	//	var removedCropName = $(this).closest('td').text().split(' ')[0];
	//	var removedCropName_index = $.inArray(removedCropName, crop_list_array);
	//	if (removedCropName_index < 4) {
	//		$('#id_crop').prop('disabled', false);
	//	}
	//	if ($(this).closest('td').prop('id') == 'crop1') {
	//		if (crop_list_array.length > 1) {
	//			$(this).closest('tr').next().find('th').text('Chosen Crop(s):');
	//			$(this).closest('tr').next().find('td').attr('id', 'crop1');
	//			$(this).closest('tr').remove();
	//			crop_list_array.splice(removedCropName_index, 1);
	//			crop_list_no_array.splice(removedCropName_index, 1);
	//		}
	//	} else {
	//		$(this).closest('tr').remove();
	//		crop_list_array.splice(removedCropName_index, 1);
	//		crop_list_no_array.splice(removedCropName_index, 1);
	//	}
	//	$('#id_crop_number').val(crop_list_array.length);
	//});

	// Refinements
	$('#id_refine').change(function() {
		var refinement = $(this).val();
		if (refinement == "uniform") {
            refine_warning();
            console.log('1');
			$('#id_refine_time_window2, #id_refine_percent_applied2')
				.attr('disabled', true).closest('tr').hide();
			$('#id_refine_percent_applied1')
				.attr('disabled', false).closest('tr').show();
		}
		else if (refinement == "uniform_step") {
            console.log('2');
			$('#id_refine_percent_applied1, #id_refine_time_window2, #id_refine_percent_applied2')
				.attr('disabled', false).closest('tr').show();
		}
		else if (refinement == "triangular") {
            refine_warning();
            console.log('3');
			$('#id_refine_percent_applied1, #id_refine_time_window2, #id_refine_percent_applied2')
				.attr('disabled', true).closest('tr').hide();
		}
	});

    function refine_warning() {
        alert("Only 'Uniform Step Application over Window' is currently allowed.  Upon model submission," +
        "the 'Refinement' will automatically switch to that option.");
    }

	$(".Chemical").trigger("click");

});