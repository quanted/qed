var marvinSketcherInstance;

var chemInfo = {

	requestParams: {
		url: '/cts/rest/molecule',
		timeout: 5000,
		retries: 3,
		postObj: {
			'chemical': null,
			'get_structure_data': null
		},

	},

	chemInput: $('#id_chem_struct'),
	resultsTable: $('#chem-results-table'),


	init: function() {
		setup();
	},

	setup: function() {

	},

	importMolecule: function(chemical) {
		/*
		Gets formula, iupac, smiles, mass, and marvin structure
	  for chemical in Lookup Chemical textarea
	  */

	  if (typeof chemical !== 'string') {
	    chemical = $('#id_chem_struct').val().trim();
	  }

	  if (chemical == "") {
	    displayErrorInTextbox("Enter a chemical or draw one first");
	    return;
	  }

	  // var chemical_obj = {'chemical': chemical};
	  var chemical_obj = {'chemical': chemical, 'get_structure_data': true};  // script for chmical editor tab needs structureData <cml> image for marvin sketch 
	  
	  getChemDetails(chemical_obj, function (molecule_info) {
	    sessionStorage.setItem('molecule', JSON.stringify(molecule_info.data)); // set current chemical in session cache
	    populateChemEditDOM(molecule_info.data);
	    // marvinSketcherInstance.importStructure("mrv", molecule_info.data.structureData.structure);
	  });
	},

	importMoleculeFromCanvas: function() {

	}

}

$(document).ready(function () {
	chemInfoHandler.init();
});