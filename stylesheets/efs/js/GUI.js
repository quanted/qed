function checkValues(content) {
  var level2 = content.parentNode;
  var level3 = level2.parentNode;
  var level4 = level3.parentNode;
  var level5 = level4.parentNode;
  var level6 = level5.parentNode;
  //alert(level6.id);

  var api = false;
  var chemical = false;

  jQuery("div#" + level6.id + " input").each(function() {
    if (this.name == "API" && this.checked == true)
      api = true;
    if (this.name == "chemical" && this.checked == true)
      chemical = true;
  });

  if (api && chemical) {
    toggleCheckOn("link-" + level6.id);
  } else {
    toggleCheckOff("link-" + level6.id);
  }
}

function toggleCheckOn(id) {
  document.getElementById(id).style.color = 'green';
}

function toggleCheckOff(id) {
  document.getElementById(id).style.color = 'black';
}

function commitValues() {
  // I suck at jQuery so I did this
  // It makes the UL easy to grab later.. ish
  jQuery("div#dynamic-table-1 ul").each(function() {
    this.id = "propertyUL";
  });

  // Find the newly identified UL and get number of li elements
  numProperties = jQuery("#propertyUL li").length;

  // For each property in 'dynamic-table-1'
  for ( i = 1; i <= numProperties; i++) {
    var api = false;
    var chem = false;
    var numProperties;
    var propName = "foo";
    var apis = new Array();
    var chemicals = new Array();
    var propName = "";
    var prop = "#property-" + i;

    // Find the checked 'apis' and 'chemicals' on each 'prop' div
    jQuery("div" + prop + " input").each(function() {
      if (this.name == "API" && this.checked == true) {
        apis.push(this.value);
        api = true;
      }
      if (this.name == "chemical" && this.checked == true) {
        chemicals.push(this.value);
        chem = true;
      }
    });

    // If both API and CHEM were checked, we have a good property
    if (api && chem) {
      // Find the name of the property
      jQuery("a").each(function() {
        if (jQuery(this).attr('href') == prop)
          propName = jQuery(this).text().trim();
      });

      for ( y = 0; y < chemicals.length; y++) {
        var casid = getCASID(chemicals[y]);
        for ( j = 0; j < apis.length; j++) {
          var chem = chemicals[y]
          postValues(propName, apis[j], chemicals[y], casid);
        }
      } 
    } 
  } 
}

function postValues(propName, apiName, chemName, casid) {
  var xml = _globalXML[apiName];
  jQuery(xml).find("property").each(function() {
    var propertyName, chemicalRefShort, chemicalRefLong;
    propertyName = jQuery(this).find("name").text();
    chemicalRefShort = jQuery(this).find("refShort").text();
    chemicalRefLong = jQuery(this).find("refLong").text();
    if (propertyName == propName) {
      jQuery(this).find("chemical").each(function() {
        var chemicalName, chemicalValue, chemicalSmiles;
        chemicalName = jQuery(this).find("iupac").text();
        if (chemicalName == chemName) {
          chemicalSmiles = jQuery(this).find("smiles").text();
          chemicalValue = parseFloat(jQuery(this).find("value").text());
          if (isNaN(chemicalValue) == true) {
            chemicalValue = null;
          } else {
            alert("Commiting to database\n\n" +
            "  Propname: " + propName + "\n" +
            "         CASID: " + casid + "\n" +
            "         IUPAC: " + chemName + "\n" +
            "         SMILE: " + chemicalSmiles + "\n" +
            "         Value: " + chemicalValue + "\n" +
            "  Reference: " + chemicalRefShort + "\n" +
            "Description: " + chemicalRefLong);

            // build the string to be POST
            var postData =
              "property=" + propName +
              "&api=" + apiName +
              "&iupac=" + chemName +
              "&n_casid=" + casid +
              "&value=" + chemicalValue +
              "&smiles=" + chemicalSmiles +
              "&refShort=" + chemicalRefShort +
              "&refLong=" + chemicalRefLong;
            jQuery.ajax({
              type : "POST",
              url : "commit.jsp",
              data : postData,
              dataType : "html",
              success : function(response) {
                // imports new structure into jchem db
                // duplicates are auto-handled
                REST.DB.SmilesToId(chemicalSmiles);
              }
            });
          }
        }
      });
    }
  });
}

function getCASID(chemName) {
  var retVal;
  
  // These fixes may not be necessary
  var chemNameFixed = chemName.replace(",", "%2C");
  chemNameFixed = chemNameFixed.replace(" ", "%20");
  chemNameFixed = chemNameFixed.replace("(", "%28");
  chemNameFixed = chemNameFixed.replace(")", "%29");

  // example - "http://cactus.nci.nih.gov/chemical/structure/benzene/cas";
  var url = "http://cactus.nci.nih.gov/chemical/structure/" + chemNameFixed + "/cas";
  
  jQuery.ajax({
    url : url,
    async : false,
    success : function(result) {
      retVal = result;
    }, // success
    error : function(jqXHR, textStatus, errorThrown) {
      retVal = "none";
    } // error
  });

  return retVal;
}

function showRef(el) {
  var xml = _globalXML[el.innerHTML];
  jQuery(xml).find("property").each(function() {
    var propName1, propName2, refShort, refLong;
    propName1 = jQuery(el).attr("prop");
    propName2 = jQuery(this).find("name").text();
    refShort = jQuery(this).find("refShort").text();
    refLong = jQuery(this).find("refLong").text();
    if (propName1 == propName2) {
      alert("Reference:  " + propName1 + "\n\n" +
      "API: " + el.innerHTML + "\n" +
      "Name: " + refShort + "\n" +
      "Description: " + refLong);
    }
  });
  return;
}

function encodeURL(smiles) {
  var ajaxURI = "http://pnnl.cloudapp.net/ajax/index.html?t=0&q=";
  var params = smiles + " |c:0,2,4|";
  var eParams = encodeURIComponent(params);

  return ajaxURI + eParams;
}



function submitQuery() {
  var i = document.getElementById("molQuerySel").selectedIndex;

  // Makes sure the user selected a chemical
  if (i != -1) {
    var sel = document.getElementById("molQuerySel").options;
    var smiles = sel[i].value;
    var ap = document.getElementById("ajaxPage");

    performSearch(smiles);
  } else {
    alert("Please select a chemical from the list.");
  }
}

function submitQsarCalc() {
  var qsar_id = jQuery("#molQsarCalcSel").val();

  // Makes sure the user selected a chemical
  if (qsar_id != -1) {
    executeQsar(qsar_id);
  } else {
    alert("Please select a QSAR calculation from the list.");
  }
}

function clearQsarResults() {
  jQuery('#qsarResults').html("");
}

function removeQsarCalc()
{
  var i = document.getElementById("molQsarCalcSel").selectedIndex;

  // Makes sure the user selected a chemical
  if (i != -1) {
    removeQsar(i);
  } else {
    alert("Please select a QSAR calculation from the list.");
  }
}

function bindMolSearchEvents(field) {
  // makes sure these reset on page refresh
  document.getElementById("molformulaSel").selectedIndex = 0;
  document.getElementById("molweightSel").selectedIndex = 0;

  // id = #formulaOpt1 OR #weightOpt1
  var opt1 = jQuery('#' + field + 'Opt1');
  var optAnd = jQuery('#' + field + 'OptAnd');
  var opt2 = jQuery('#' + field + 'Opt2');

  // This always gets called on load to bind the event
  jQuery('#mol' + field + 'Sel').change(function() {
    var sel = document.getElementById('mol' + field + 'Sel');
    if (sel.options[sel.selectedIndex].value == "$between") {
      opt1.show();
      optAnd.show();
      opt2.show();
    } else if (sel.options[sel.selectedIndex].value != "") {
      opt1.show();
      optAnd.hide();
      opt2.hide();
    } else {
      opt1.hide();
      optAnd.hide();
      opt2.hide();
    }
  });
}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds) {
      break;
    }
  }
}

function supports_html5_storage()
{
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
  } catch (e) {
    return false;
  }
}

var GUI = {
  chemicalList: {},

  init: function() {
    bindMolSearchEvents("formula");
    bindMolSearchEvents("weight");
  },

  fillChemSelector: function(elementId, smiles, name) {
    var sel = document.getElementById(elementId);
    var opt = document.createElement("option");

    opt.text = name;
    opt.value = smiles;

    // for IE earlier than version 8
    try {
      sel.add(opt, sel.options[null]);
    } catch (e) {
      sel.add(opt, null);
    }
  },

  fillChemListControls: function() {
    var chemNames = [];
    var distinctChemNames = [];

    // loop chemlist and grab only the names
    for (name in GUI.chemicalList)
    {
      if (GUI.chemicalList.hasOwnProperty(name))
      {
        chemNames.push(name);
      }
    }

    // loop names and find only distinct
    jQuery.each(chemNames, function(i, el) {
        if(jQuery.inArray(el, distinctChemNames) === -1) distinctChemNames.push(el);
    });

    // for each distinct name get the smiles from chemlist
    // fill the selection controls
    jQuery.each(distinctChemNames, function(i, el) {
      GUI.fillChemSelector("molQuerySel",GUI.chemicalList[el],el);
      GUI.fillChemSelector("molQsarSel",GUI.chemicalList[el],el);
    });
  }
};
