jQuery.noConflict();

var list;
var chemicals = {};
var marvinSketcherInstance;

//var property_tables = {
//  init: function(msi) {
//    marvinSketcherInstance = msi;
//  },
//};

//= dialog.js
//= dynamic_table.js
function errorHandler(response) {
  //alert(response.getElementsByTagName(SOAP.errorElementName).item(0).firstChild.nodeValue);
}

function getContent(smile, mol, imgsOn) {
  var jchemData = REST.Util.ImageBySmiles(smile);
  var iupac = jchemData.data[0].iupac;

  if (iupac.length > 25) {
    iupac = iupac.substring(0,17) + " [...]";
  }

  var title = jchemData.data[0].iupac + "&#13;";
  for (prop in mol) {
    if (mol.hasOwnProperty(prop)) {
      if (prop != "metabolites" && prop != "generation") {
        title += "&#13;" + prop + ": "  + mol[prop];
      }
    }
  }

  var result = {};
  
  if (imgsOn) {
    result.html = '<img id="image" src="' + jchemData.data[0].image.imageUrl + '" title="' + title + '" border="1" /><br />';
    result.html += iupac;
    result.html += '<br/><input class="degradation-products" type="checkbox" value="' + smiles +'" checked="checked" />Save';
  } else {// this option is disabled in html so we always get the title attributes
    result.html = jchemData.data[0].iupac;
  }

  result.iupac = jchemData.data[0].iupac;

  return result;
}

function reaction() {
  chemicals = {};
  list = "";
  GUI.chemicalList = {};

  // Clear the selection list and results table
  document.getElementById("molQuerySel").options.length = 0;
  document.getElementById("molQsarSel").options.length = 0;
  document.getElementById("spreadsheetResult").innerHTML = "";
  document.getElementById("numResults").innerHTML = "Ready";
  document.getElementById("qsarResults").innerHTML = "";

  resetDynamicTable();

  // make ajax call with these params
  var metabProducts = REST.Metabolizer.getMetabolites({
    smiles: jQuery('#molecule').val(),
    genLimit : jQuery('#genLimit').val(),
    popLimit : jQuery('#popLimit').val(),
    likelyLimit : jQuery('#lklyLimit').val(),
    transLibs : ["hydrolysis","abiotic_reduction","human_biotransformation"],
    excludeCondition : "",
    generateImages : false
  });

  // if not the ajax call fails
  if (metabProducts != "Fail ") {
    var status = metabProducts.status;
    var results = metabProducts.results;
    var imgs = jQuery('#showImages').is(':checked');

    var addListItem = function(params) {
      var smiles = params.smiles;
      var iupac = params.iupac;
      var parentSmiles = params.parentSmiles;
      var routes = params.routes;
      
      // three lists for nearly the same reason, we should consolidate
      // list for pysiochemical API and saving properties
      if (list == "") {
        list = smiles + ';' + iupac;
      } else {
        list = list + ';' + smiles + ';' + iupac;
      }
      
      // list for GUI elements
      GUI.chemicalList[iupac] = smiles;

      // list for saving metabolites
      chemicals[smiles] = {};
      chemicals[smiles].parent = parentSmiles;
      chemicals[smiles].routes = routes;
      chemicals[smiles].iupac = iupac;
    };

    var metabolites = {};
    var parentSmiles = "";
    
    var recurseNodes = function(obj, treeObj, parentSmiles) {
      for (smiles in obj.metabolites) {
        if (obj.metabolites.hasOwnProperty(smiles)) {
          var content = getContent(smiles, obj.metabolites[smiles], imgs);
          addListItem({smiles:smiles,
                       parentSmiles:parentSmiles,
                       iupac:content.iupac,
                       routes:obj.metabolites[smiles].routes});/*,
                       rate:obj.metabolites[smiles].rate});*/
          
          var newObj = {};
          newObj.Content = content.html;
          newObj.Nodes = new Array();
          treeObj.Nodes.push(newObj);
          
          recurseNodes(obj.metabolites[smiles], newObj, smiles);
        }
      }
    }
    
    if (status == "success") {
      // hopefully this is only one
      // it should always be the smiles of the parent compound
      for (smiles in results) { 
        if (results.hasOwnProperty(smiles)) {
          var content = getContent(smiles, results[smiles], imgs);
          addListItem({smiles:smiles,
                       parentSmiles:null,
                       iupac:content.iupac,
                       routes:null});
          metabolites = {Content: content.html};
          metabolites.Nodes = new Array();
          recurseNodes(results[smiles], metabolites, smiles);
        }
      }
      
      DrawTree({
        Container: document.getElementById("degrade"),
        RootNode: metabolites,
        Layout: "Horizontal"
      });
      
      GUI.fillChemListControls();
    }
  }
}

// needs chemicals from reaction()
function saveReaction() {
  var metabolitesToSave = {};

  jQuery('.degradation-products').each(function() {
    if (jQuery(this).is(':checked')) {
      var smiles = jQuery(this).attr('value');
      metabolitesToSave[smiles] = {};
      metabolitesToSave[smiles].parentSmiles = chemicals[smiles].parent;
      metabolitesToSave[smiles].parentIupac = (chemicals[smiles].parent == null) ? null : chemicals[chemicals[smiles].parent].iupac;
      metabolitesToSave[smiles].iupac = chemicals[smiles].iupac;
      metabolitesToSave[smiles].respiration_name = document.getElementById("obi").value;
      metabolitesToSave[smiles].media_name = document.getElementById("med").value;;
      metabolitesToSave[smiles].qsar_id = 0;
      metabolitesToSave[smiles].routes = chemicals[smiles].routes;
      metabolitesToSave[smiles].rate = 0;
    }
  });

  var result = REST.Metabolizer.saveMetabolites({metabolites:metabolitesToSave});
  
  // if save metabolites succeeds
  // we want to save any and all new molecules to jchem too
  if (result.status == "sucess") {
    for (smiles in metabolitesToSave) {
      if (metabolitesToSave.hasOwnProperty(smiles)) {
        // imports new structure into jchem db
        // duplicates are auto-handled
        REST.DB.SmilesToId(smiles);
      }
    }
  }
}

function resetDynamicTable()
{
  jQuery("#apiButton").empty();
  jQuery("#dynamic-table-1").remove();

  _globalXML = {};
  window.App = null;
  dyn_Table();
}

function importMol(smiles) {
  if(smiles) document.SmilesForm.MolTxt.value = smiles;

  var mol = document.SmilesForm.MolTxt.value;

  if (mol != "") // entered value in textbox
  {
    var jchemData = REST.Util.DetailsBySmiles(mol);

    marvinSketcherInstance.importAsMrv(jchemData.data[0].structureData.structure);
//    msi.importAsMrv(jchemData.data[0].structureData.structure);

    document.SmilesForm.molecule.value = jchemData.data[0].smiles;
    document.SmilesForm.formula.value = jchemData.data[0].formula;
    document.SmilesForm.IUPAC.value = jchemData.data[0].iupac;
    document.SmilesForm.mass.value = jchemData.data[0].mass;
  }

  if (smiles)
  {
    setTimeout(function() {jQuery("#doDump1").click();}, 1000);
  }
}

function importMolFromCanvas(s) {
  var jchemData = REST.Util.MrvToSmiles(marvinSketcherInstance.exportAsMrv());
  //var jchemData = REST.Util.MrvToSmiles(msi.exportAsMrv());
  var smiles = jchemData['structure'];

  document.SmilesForm.MolTxt.value = smiles;
  importMol(null);
}

function setElementValueAndBackgroundColor(elementID, value, booleanExpression, trueColor, falseColor) {
  document.getElementById(elementID).innerHTML = value;
  if (booleanExpression) {
    document.getElementById(elementID).style.backgroundColor = trueColor;
  } else {
    document.getElementById(elementID).style.backgroundColor = falseColor;
  }
}


function propertyChange(prop) {
  if (prop.indexOf('mol=') != -1) {
    setFields();
  }
}

function displayMedia(media) {
  var obi = document.getElementById("obi").value;
  document.getElementById("med").value = media;

  document.getElementById("Reduction").checked = false;
  document.getElementById("Oxidation").checked = false;
  document.getElementById("Hydrolysis").checked = false;
  document.getElementById("Photolysis").checked = false;
  document.getElementById("AerobicBio").checked = false;
  document.getElementById("AnaerobicBio").checked = false;
  document.getElementById("Metabolism").checked = false;

  document.getElementById("Reduction").disabled = false;
  document.getElementById("Oxidation").disabled = false;
  document.getElementById("Hydrolysis").disabled = false;
  document.getElementById("Photolysis").disabled = false;
  document.getElementById("AerobicBio").disabled = false;
  document.getElementById("AnaerobicBio").disabled = false;
  document.getElementById("Metabolism").disabled = false;

  if (obi == "Aerobic") {
    document.getElementById("Hydrolysis").checked = true;
    if (media != "Water Treatment & Distribution") {
      document.getElementById("AerobicBio").checked = true;
    } else {
      document.getElementById("Oxidation").checked = true;
    }
    if (media == "Surface Water" || media == "Surface Soil" || media == "Solid Waste") {
      document.getElementById("Photolysis").checked = true;
    }
//    if (media == "Human Liver") {
//      document.getElementById("Metabolism").checked = true;
//    }
  } else {
    if (media == "Water Treatment & Distribution") {
      document.getElementById("Hydrolysis").disabled = true;
      document.getElementById("Oxidation").disabled = true;
    }
    if (media == "Surface Soil") {
      document.getElementById("Reduction").disabled = true;
      document.getElementById("Hydrolysis").disabled = true;
      document.getElementById("AnaerobicBio").disabled = true;
    }
    if (media != "Surface Soil" && media != "Water Treatment & Distribution" && media != "Human Liver") {
      document.getElementById("Reduction").checked = true;
      document.getElementById("Hydrolysis").checked = true;
      document.getElementById("AnaerobicBio").checked = true;
    }
    if (media == "Surface Water" || media == "Solid Waste") {
      document.getElementById("Photolysis").checked = true;
    }
//    if (media == "Human Liver") {
//      document.getElementById("Metabolism").checked = true;
//    }
  }
  loadQsars();
}

function loadQsars()
{
  var respiration_name = document.getElementById("obi").value;
  var media_name = document.getElementById("med").value;

  document.getElementById("molQsarCalcSel").options.length = 0;
  document.getElementById("qsarDisclaimer").innerHTML = "Displaying QSARs for " + respiration_name + " respiration and " + media_name + " media.<br/><b style='color:red'>Note:</b> Results table is cleared when degradation products are generated.";

  loadQsarFromDB({
    respiration_name : respiration_name,
    media_name : media_name
  });
}

function displayObic(obic) {
  document.getElementById("obi").value = obic;
  displayMedia(document.getElementById("med").value);
}

function isValidXml(xml) {
  var isValid = false;

  try {
    isValid = jQuery.parseXML(xml);
  } catch (e) {
  }

  return isValid;
}

function show(el) {
  jQuery(el).html("-");
  jQuery(el).parent().next().show();

  return false;
}

function hide(el) {
  jQuery(el).html("+");
  jQuery(el).parent().next().hide();

  return false;
}

function toggle(el) {
  if (jQuery(el).html() == "+") {
    show(el);
  } else {
    hide(el);
  }

  return false;
}

function loadEnv() {
  (function($) {
    $.ajax({
      type : "POST",
      url : "envdump.jsp",
      data : {
        address : $('#address').val()
      },
      //async: false,
      dataType : "html",
      success : function(envdata) {
        $('#T').val(parseFloat($(envdata).find('#T').html()).toFixed(2));
        $('#pH').val(parseFloat($(envdata).find('#pH').html()).toFixed(2));
        $('#foc').val(parseFloat($(envdata).find('#foc').html()).toFixed(2));
        $('#sFe').val(parseFloat($(envdata).find('#sFe').html()).toFixed(2));
        resetDynamicTable();
      },
      error : function(xhr, status, error) {
        var breakhere = true;
      }
    });
  })(jQuery);
}

function reloadPropertiesAndSelectActiveTab() {
  (function($) {
    var url = $('#doDump2').attr("href");

    $.ajax({
      type : "POST",
      url : url,
      dataType : "html",
      success : function(tabData) {
        var activeHref;

        activeHref = $('.ui-state-active > a').attr("href");
        loadProperties(tabData, "#propertyTable");

        $('#tabs').tabs();
        $('a[href="' + activeHref + '"]').click();
      }
    });
  })(jQuery);
}

function bindToggle() {
  jQuery('.doToggle').unbind('click').click(function(event) {
    toggle(this);
  });
}

function bindUpdatePropertyRef() {
  (function($) {
    $('a.selectRef').unbind("click").click(function(event) {
      var url = $(this).attr("href");

      $.ajax({
        type : "POST",
        url : url,
        dataType : "html",
        success : function(data) {
          reloadPropertiesAndSelectActiveTab();
          $().simpleDialog('hideDialog', 100);
        },
        error : function(data) {
          var breakhere = true;
        }
      });

      return false;
    });
  })(jQuery);
}

function bindSearchRef() {
  (function($) {
    $('#submitFindRef').unbind("submit").submit(function(event) {
      var url = $(this).attr("action");

      $.ajax({
        type : "POST",
        url : url,
        dataType : "html",
        data : {
          searchval : $('input#search-ref').val()
        },
        success : function(data) {
          $('p#ref_search_results').html(data);
          bindUpdatePropertyRef();
          $('a.change_ref').simpleDialog('setDialog', 600, 800);
        },
        error : function(data) {
          var breakhere = true;
        }
      });

      return false;
    });
  })(jQuery);
}

function bindChangeRef() {
  (function($) {
    $('a.change_ref').simpleDialog({
      avoid : {
        top : $('#content').position().top,
        left : $('#content').position().left,
        bottom : $('#content').position().top + $('#content').height(),
        right : $('#content').position().left + $('#content').width()
      }
    }, function(el, innerDialog) {//requires dialog.js
      var url = $(el).attr("href");
      var html = $("#find_ref_tmpl").tmpl({
        Url : url,
        Val : ""
      });

      $().simpleDialog('setTitle', "Change Reference");
      $(innerDialog).html(html);
      bindSearchRef();

      return false;
    });
  })(jQuery);
}

function shwRef(data, container) {
  (function($) {
    var addUrl = $(data).find("a.add_ref").attr("href");

    $(data).find("a.add_ref").remove();
    $(container).html(data);
    $(container).parent().prev().find("a.add_ref").attr("href", addUrl);
  })(jQuery);
}

function bindShowRefToolTip() {
  (function($) {
    $('.showRef').tooltip({}, function(data, inner_tip_el) {//requires referenceTooltip.js
      shwRef(data, inner_tip_el);
    });
  })(jQuery);
}

function bindShowRefDialog() {
  (function($) {
    $('.showRef').simpleDialog({
      avoid : {
        top : $('#content').position().top,
        left : $('#content').position().left,
        bottom : $('#content').position().top + $('#content').height(),
        right : $('#content').position().left + $('#content').width()
      }
    }, function(el, innerDialog) {//requires dialog.js
      var refUrl = el.attr("href");

      $().simpleDialog('setTitle', "Reference");

      $.ajax({
        type : "POST",
        url : refUrl,
        dataType : "html",
        success : function(refData) {
          var addUrl = $(refData).find("a.add_ref").attr("href");
          var sname = $(refData).find("#sname").html();
          var bname = $(refData).find("#bname").html();
          var html = $("#showRef_tmpl").tmpl({
            Url : addUrl,
            SName : sname,
            BName : bname
          });

          $(innerDialog).html(html);
        },
        error : function() {
          $(innerDialog).html("Error!");
        }
      });

      return false;
    });
  })(jQuery);
}

function bindShowUpdateRef() {
  (function($) {
    $('.updateRef').simpleDialog({
      avoid : {
        top : $('#content').position().top,
        left : $('#content').position().left,
        bottom : $('#content').position().top + $('#content').height(),
        right : $('#content').position().left + $('#content').width()
      }
    }, function(el, innerDialog) {//requires dialog.js
      var refUrl = el.attr("href");

      $.ajax({
        type : "POST",
        url : refUrl,
        dataType : "html",
        success : function(refData) {
          var addUrl = $(refData).find("a.add_ref").attr("href");
          var sname = $(refData).find("#sname").html();
          var bname = $(refData).find("#bname").html();
          var html = $("#addRef_tmpl").tmpl({
            Url : addUrl,
            SName : sname,
            BName : bname
          });

          $(innerDialog).html(html);
          bindSubmitNewRef();
        },
        error : function() {
          $(innerDialog).html("Error!");
        }
      });

      return false;
    });
  })(jQuery);
}

function bindSubmitNewRef() {
  (function($) {
    $("#submitNewRef").unbind("submit").submit(function(event) {
      var url = $(this).attr("action");

      $.ajax({
        type : "POST",
        url : url,
        data : {
          SNAME : $('#input-sname').val(),
          BNAME : $('#input-bname').val()
        },
        datatype : "html",
        success : function(data) {
          shwRef(data, $('.tip .tipMid .inner'));
          ;
          $().simpleDialog('hideDialog', 100);

          reloadPropertiesAndSelectActiveTab();
        },
        error : function(data) {
          var breakhere = true;
        }
      });

      return false;
    });
  })(jQuery);
}

function bindAddRef() {
  (function($) {
    $('a.add_ref').simpleDialog({
      avoid : {
        top : $('#content').position().top,
        left : $('#content').position().left,
        bottom : $('#content').position().top + $('#content').height(),
        right : $('#content').position().left + $('#content').width()
      }
    }, function(el, innerDialog) {//requires dialog.js
      var url = el.attr("href");
      var html = $("#addRef_tmpl").tmpl({
        Url : url
      });

      $().simpleDialog('setTitle', "Add Reference");
      $(innerDialog).html(html);
      bindSubmitNewRef();

      return false;
    });
  })(jQuery);
}

function removeProperty(event) {
  var url = jQuery(event.delegateTarget).attr("href");
  jQuery.ajax({
    type : "POST",
    url : url,
    datatype : "html",
    success : function(data) {
      jQuery(event.delegateTarget).parent().parent().remove();
    }
  });
  return false;
}

function bindPropertyUpdate() {
  (function($) {
    $('.input-property-update').unbind("click").click(function() {
      var url = $(this).attr("href");
      var el = $(this);
      var newVal = $(this).parent().find('input.input-property-value').val();

      $.ajax({
        type : "POST",
        url : url,
        data : {
          newVal : newVal
        },
        datatype : "html",
        success : function(data) {
          el.parent().parent().html($(data).html());
          bindPropertyEvents();
        },
        error : function(data) {
          var breakhere = true;
        }
      });

      return false;
    });
  })(jQuery);
}

function bindSubmitNewProperty(propertyID, container) {
  (function($) {
    $("#submitNewProperty").unbind("submit").submit(function() {
      var url = $(this).attr("action");
      var pid = $('#prop' + propertyID).val();
      var val = $('#input-val').val();

      $.ajax({
        type : "POST",
        url : url,
        data : {
          pid : pid,
          val : val
        },
        datatype : "html",
        success : function(data) {
          $(container).append(data);
          bindPropertyEvents();
          $().simpleDialog('hideDialog', 100);
        },
        error : function(data) {
          var breakhere = true;
        }
      });

      return false;
    });
  })(jQuery);
}

var Range, propertyRange;

Range = (function() {
  function Range() {
  }


  Range.prototype.units = "";
  Range.prototype.datatype = "";
  Range.prototype.min = "";
  Range.prototype.max = "";

  return Range;
})();

function isValidFloatRange(val, min, max) {
  if (val == "" || isNaN(val))
    return false;

  if (min != "") {
    if (parseFloat(min) > parseFloat(val)) {
      return false;
    }
  }
  if (max != "") {
    if (parseFloat(max) < parseFloat(val)) {
      return false;
    }
  }

  return true;
}

function isValidCharRange(val, min, max) {
  if (min != "") {
    if (parseFloat(min) > val.length) {
      return false;
    }
  }
  if (max != "") {
    if (parseFloat(max) < val.length) {
      return false;
    }
  }

  return true;
}

function isValidIntegerRange(val, min, max) {
  if (isNaN(val) || val.indexOf(".") != -1)//is val an integer
  {
    return false;
  }

  return isValidFloatRange(val, min, max);
}

function isValidListRange(val, min, max) {
  return min.split(",").indexOf(val) != -1;
}

function isValidPropertyRange(val) {
  if (propertyRange == null) {
    return true;
  }

  if (propertyRange.datatype.toLowerCase() == "float") {
    return isValidFloatRange(val, propertyRange.min, propertyRange.max);
  }
  if (propertyRange.datatype.toLowerCase() == "char") {
    return isValidCharRange(val, propertyRange.min, propertyRange.max);
  }
  if (propertyRange.datatype.toLowerCase() == "list") {
    return isValidListRange(val, propertyRange.min, propertyRange.max);
  }
  if (propertyRange.datatype.toLowerCase() == "int") {
    return isValidIntegerRange(val, propertyRange.min, propertyRange.max);
  }

  return true;
}

function bindCheckPropertyRange() {
  (function($) {
    $("#input-val").unbind("keyup").keyup(function() {
      var isValid = isValidPropertyRange($(this).val());

      if (isValid == true) {
        $(this).css("backgroundColor", "#CBF2D0");
      } else {
        $(this).css("backgroundColor", "#F2CBCB");
      }
    });
  })(jQuery);
}

function bindAddProperty() {
  (function($) {
    $('.addProperty').simpleDialog({
      avoid : {
        top : $('#content').position().top,
        left : $('#content').position().left,
        bottom : $('#content').position().top + $('#content').height(),
        right : $('#content').position().left + $('#content').width()
      }
    }, function(el, innerDialog) {//requires dialog.js
      var url = el.attr("href");
      var id = el.attr("id");
      var html;

      $().simpleDialog('setTitle', "Add Property");
      propertyRange = new Range();

      $.ajax({
        type : "POST",
        url : "propertyRange.jsp",
        data : {
          PROPID : $('#prop' + id + ' > option:selected').val()
        },
        datatype : "html",
        success : function(rangeData) {
          propertyRange.units = $(rangeData).find("#units").html();
          propertyRange.datatype = $(rangeData).find("#datatype").html();
          propertyRange.min = $(rangeData).find("#min").html();
          propertyRange.max = $(rangeData).find("#max").html();

          html = $("#addProperty_tmpl").tmpl({
            Url : url,
            Property : $('#prop' + id + ' > option:selected').text(),
            Units : propertyRange.units,
            Type : propertyRange.datatype,
            Min : propertyRange.min,
            Max : propertyRange.max
          });
          innerDialog.html(html);
          bindCheckPropertyRange();
          bindSubmitNewProperty(id, el.parent().parent().parent());
        },
        error : function() {
          $("#input-val").unbind("keyup");

          html = $("#addProperty_tmpl").tmpl({
            Url : url,
            Property : $('#prop' + id + ' > option:selected').text(),
            Units : propertyRange.units,
            Type : propertyRange.datatype,
            Min : propertyRange.min,
            Max : propertyRange.max
          });
          innerDialog.html(html);
          bindCheckPropertyRange();
          bindSubmitNewProperty(id, el.parent().parent().parent());
        }
      });

    });
  })(jQuery);
}

function bindPropertyEvents() {
  (function($) {
    bindShowRefDialog();
    bindAddProperty();
    bindPropertyUpdate();
    bindAddRef();
    bindChangeRef();
    $('.delProperty').unbind("click").click(removeProperty);
  })(jQuery);
}

function loadProperties(propertiesData, containerID) {
  (function($) {
    $(containerID).html(propertiesData);
    show($(containerID + "-toggle"));

    bindPropertyEvents();

    bindToggle();
  })(jQuery);
}


jQuery(document).ready(function($) {
//  var $tabs = $('#mtabs').tabs();
//  var selected = $tabs.tabs('option', 'selected');

//  $('#dialog').dialog({
//    autoOpen : false
//  });

//  jQuery("#chemEditor").click(function () {
    if(!jQuery("#sketch").length) {
      jQuery("div.resizable").html("<iframe id='sketch' src='../stylesheets/efs/marvin4js/editor.html'  class='sketcher-frame' style='min-width:600px; min-height:450px;'></iframe>");

      getMarvinPromise("#sketch").done(function (sketcherInstance) {
        marvinSketcherInstance = sketcherInstance;
      });
    }
//  });

//  google.setOnLoadCallback(showMap);

//  $('#mtabs').bind('tabsshow', function(event, ui) {
//    if (ui.panel.id == "mtabs-4") {
//      window.gmap.checkResize();
//    }
//  });

//  $('#doDump1').click(function(event) {
//    var url = "dump.jsp?smiles=";
//    url += $('#molecule').val() + "&iupac=" + $('#IUPAC').val();

//    $(this).attr("href", url);
//    $.ajax({
//      type : "POST",
//      url : url,
//      dataType : "html",
//      success : function(data) {
//        loadProperties(data, "#propertyTable");
//        $('#tabs').tabs();
//      }
//    });

//    label = "Chemical Properties (SMILES: " + $('#molecule').val() + ")";
//    $(this).html(label);
//    return false;
//  });

//  bindToggle();

//  $('#doMap').click(function(event) {
//    var response = '';
//    $.ajax({
//      type : "GET",
//      url : "http://www.getlatlon.com",
//      success : function(data) {
//        $('#doMapPage').html(data.responseText);
//        $('#doMapPage').show();
//        $('#doMapPage').prev().children().first().html("-");
//      }
//    });

//  });
});

