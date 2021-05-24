var marvinSketcherInstance;

$(document).ready(function handleDocumentReady (e) {});

function initiateMarvinInstance(jchem_server) {
  try {

    MarvinJSUtil.getEditor("#sketch").then(function (sketcherInstance) {
      marvinSketcherInstance = sketcherInstance;
      var services = localGetDefaultServices(jchem_server);  // sets jchem server settings
      marvinSketcherInstance.setServices(services);
      loadCachedChemical();
      // initControl(); //binds action to initControl() function
    }, function (error) {
      alert("Cannot retrieve sketcher instance from iframe:"+error);
    });
  }
  catch (e) {
    console.log("no marvin sketch instance here");
    return;
  }
  $('#setSmilesButton').on('click', importMol); // map button click to function
  $('#getSmilesButton').on('click', importMolFromCanvas);
  var browserWidth = $(window).width();
  var browserHeight = $(window).height();
  var winleft = (browserWidth / 2) - 220 + "px";
  var wintop = (browserHeight / 2) - 30 + "px";
  // Removes error styling when focused on textarea or input:
  $('textarea, input').focusin(function() {
      if ($(this).hasClass('formError')) {
        $(this).removeClass("formError").val("");
      }
  });
}

function localGetDefaultServices(new_base) {
  /*
  This function is straight from marvin4js webservices.js in static_qed/cts/js/efs
  */
  if (!new_base) { return; }
  var base = new_base + "/webservices";
  var services = {
      "clean2dws" : base + "/rest-v0/util/convert/clean",
      "clean3dws" : base + "/rest-v0/util/convert/clean",
      "molconvertws" : base + "/rest-v0/util/calculate/molExport",
      "stereoinfows" : base + "/rest-v0/util/calculate/cipStereoInfo",
      "reactionconvertws" : base + "/rest-v0/util/calculate/reactionExport",
      "hydrogenizews" : base + "/rest-v0/util/convert/hydrogenizer",
      "automapperws" : base + "/rest-v0/util/convert/reactionConverter"
  };
  return services;
}

// "wait" cursor during ajax events
$(document).ajaxStart(function () {
    $('body').addClass('wait');
}).ajaxComplete(function () {
    $('body').removeClass('wait');
});

function loadCachedChemical() {
  var cachedMolecule = JSON.parse(sessionStorage.getItem('molecule'));
  if (cachedMolecule !== null) {
    populateChemEditDOM(cachedMolecule);
  }
  // Checking for missing MarvinSketch, if there isn't
  // <cml> data for it, then it requests it:
  checkForMarvinSketchData(cachedMolecule);
}

function checkForMarvinSketchData(cachedMolecule) {
  // Checks for missing MarvinSketch, if there isn't
  // <cml> data for it, then it requests it:
  if (!('structureData' in cachedMolecule)) {
    var chemicalObj = {'chemical': cachedMolecule.chemical, 'get_structure_data': true};
    getChemDetails(chemicalObj, function (molecule_info) {
      sessionStorage.setItem('molecule', JSON.stringify(molecule_info.data)); // set current chemical in session cache
      populateChemEditDOM(molecule_info.data);
    });
  }
}

function importMol(chemical) {
  // Gets formula, iupac, smiles, mass, and marvin structure
  // for chemical in Lookup Chemical textarea
  if (typeof chemical !== 'string') {
    chemical = $('#id_chem_struct').val().trim();
  }
  if (chemical == "") {
    displayErrorInTextbox("Enter a chemical or draw one first");
    return;
  }
  var chemical_obj = {'chemical': chemical, 'get_structure_data': true};  // script for chmical editor tab needs structureData <cml> image for marvin sketch 
  getChemDetails(chemical_obj, function (molecule_info) {
    sessionStorage.setItem('molecule', JSON.stringify(molecule_info.data)); // set current chemical in session cache
    populateChemEditDOM(molecule_info.data);
    // Scrolls to the top of the MarvinSketch div, plus the width of the 
    // Heading table row (where it says "Draw Chemical Structure", etc.)
    var chemHeader = $('#chemEditDraw').children('table')
                .children('tbody').children('tr')[0];
    var headerHeight = $(chemHeader).height();
    $('html,body').animate({
      scrollTop: $('#chemEditDraw').offset().top + headerHeight
    }, 'slow');

  });
  clearChemicalEditorContent();  // clears marvinsketch and results table
}

function importMolFromCanvas() {
  //Gets smiles, iupac, formula, mass for chemical 
  //drawn in MarvinJS
  marvinSketcherInstance.exportStructure("mrv").then(function(mrv_chemical) {
    if (mrv_chemical == '<cml><MDocument></MDocument></cml>') {
      displayErrorInTextbox("Draw a chemical first..");
      return;
    }
    var chemical_obj = {'chemical': mrv_chemical, 'get_structure_data': true};
    getChemDetails(chemical_obj, function (molecule_info) {
      // put orig smiles in "lookup chemical" box for drawn chemical:
      molecule_info['data']['chemical'] = molecule_info['data']['orig_smiles'];
      sessionStorage.setItem('molecule', JSON.stringify(molecule_info.data)); // set current chemical in session cache
      populateChemEditDOM(molecule_info.data);
      // Scrolls to the top of the MarvinSketch div, plus the width of the 
      // Heading table row (where it says "Draw Chemical Structure", etc.)
      var chemHeader = $('#chemEditDraw').children('table')
            .children('tbody').children('tr')[0];
      var headerHeight = $(chemHeader).height();
      $('html,body').animate({
        scrollTop: $('#chemEditDraw').offset().top + headerHeight
      }, 'slow');
    });
  });
}

function getChemDetails(chemical_obj, callback) {
  ajaxCall(chemical_obj, function (chemResults) {
    callback(chemResults);
  });
}

function populateChemEditDOM(data) {
  //Populates Results textboxes with data:
  $('#id_chem_struct').val(data["chemical"]); //Enter SMILES txtbox
  $('#chemical').val(data['chemical']);
  $('#smiles').val(data["smiles"]); //SMILES string txtbox - results table
  $('#orig_smiles').val(data['orig_smiles']);
  $('#preferredName').val(data['preferredName']);
  $('#iupac').val(data["iupac"]); //IUPAC txtbox - results table
  $('#formula').val(data["formula"]); //Formula txtbox - results table
  $('#cas').val(data['cas']);
  $('#casrn').val(data['casrn']);
  $('#dtxsid').val(data['dsstoxSubstanceId']);
  $('#mass').val(data["mass"]); //Mass txtbox - results table
  $('#exactmass').val(data['exactMass']);
  try {
    marvinSketcherInstance.importStructure("mrv", data.structureData.structure);
  }
  catch (e) {
    console.log(e);
  }
}

function displayErrorInTextbox(errorMessage) {
  //Displays error message in Lookup Chemical textbox
  if (typeof errorMessage === 'undefined' || errorMessage == "") {
    errorMessage = "Name not recognized..";
  }
  $('#id_chem_struct').addClass("formError").val(errorMessage); //Enter SMILES txtbox
  clearChemicalEditorContent();
}

function clearChemicalEditorContent() {
  // Clears MarvinSketch instance and results table
  $('#chemical').val("");
  $('#smiles').val("");
  $('#orig_smiles').val("");
  $('#preferredName').val("");
  $('#iupac').val("");
  $('#formula').val("");
  $('#cas').val("");
  $('#casrn').val("");
  $('#dtxsid').val("");
  $('#mass').val("");
  $('#exactmass').val("");
  try {
    marvinSketcherInstance.clear(); //clear marvin sketch
  }
  catch (e) {
    return;
  }
}

function jsonRepack(jsonobj) {
  return JSON.parse(JSON.stringify(jsonobj));
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}     

var csrftoken = getCookie('csrftoken');

function ajaxCall(data_obj, callback) {
  $.ajax({
    url: '/cts/rest/molecule',
    type: 'POST',
    data: data_obj,
    dataType: 'json',
    // timeout: 10000,
    timeout: 20000,
    tryCount: 0,
    retryLimit: 1,  // retry 1 time if failure
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function(data) {
      var data = jsonRepack(data);
      if (data.status == false) {
        displayErrorInTextbox(data.error);
      }
      else {
        $('#id_chem_struct').removeClass('formError');
        callback(data);
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      if (textStatus == 'timeout' || textStatus == 'error') {
        this.tryCount++;
        if (this.tryCount <= this.retryLimit) {
          // try again
          $.ajax(this);
          return;
        }
        displayErrorInTextbox("Name not recognized");
        return;
      }
      else {
        displayErrorInTextbox("Name not recognized");
        return;
      }
    }
  });
}