qsarsList = {};
var $a = 2;
var $b = 3;
qsarQueryUrl = "http://pnnl.cloudapp.net/efs/qsarQuery.jsp";

function executeQsar(qsar_id)
{
  var i = document.getElementById("molQsarSel").selectedIndex;
  var y = document.getElementById("molQsarCalcSel").selectedIndex;
  var sel = document.getElementById("molQsarSel").options;
  var qsar_id = document.getElementById("molQsarCalcSel").options[y].value;
  var chem = sel[i].text;
  var pka = findpKa(chem);
  var logk = "undefined";

  if (pka !== "undefined")
  {
    // execute qsar
    logk = execQsarUsingJsp({
      qsar_id : qsar_id,
      pka : pka
    });
  }

  // create table
  qsarResultsTable({
    chem : chem,
    alias : qsarsList[qsar_id].Alias,
    value : logk,
    respiration : qsarsList[qsar_id].Respiration,
    media : qsarsList[qsar_id].Media,
    selectedChemIndex : i,
    selectedQsarIndex : qsar_id
  });
}

function qsarResultsTable(params)
{
  if (jQuery("#qsarResults").html() == "")
  {
    var tbl = "<br/><table id='qsarResultsTable'><tbody><tr><th>Chemical</th><th>QSAR</th><th>Value</th><th>Reaction</th><th>Respiration</th><th>Media</th></tr>";
       tbl += qsarResultsTableAddRow(params);

    jQuery("#qsarResults").append(tbl);
  }
  else
  {
    // insures chem + qsar cell doesn't exist
    if (!jQuery('#' + params.selectedChemIndex + '-' + params.selectedQsarIndex + '-cell').length > 0)
    {
      jQuery('#qsarResultsTable tr:last').after(qsarResultsTableAddRow(params));
    }
  }
}

function qsarResultsTableAddRow(params)
{
  var row = "<tr><td>" + params.chem + "</td>";
     row += "<td>" + params.alias + "</td>";
     row += "<td id='" + params.selectedChemIndex + "-" + params.selectedQsarIndex + "-cell'>" + params.value + "</td>";
     row += "<td>Nucleophilic Addition</td>";
     row += "<td>" + params.respiration + "</td>";
     row += "<td>" + params.media + "</td></tr></tbody></table>";

  return row;
}

function findpKa(iupac)
{
  var pka = "undefined";
  var xml = _globalXML["ChemAxon pKa(aniline)"];

  jQuery(xml).find("property").each(function() {
    var propertyName;
    propertyName = jQuery(this).find("name").text();
    if (propertyName == "The symbol for the acid dissociation constant") {
      jQuery(this).find("chemical").each(function() {
        var chemicalName;
        chemicalName = jQuery(this).find("iupac").text();
        if (chemicalName == iupac) {
          pka = parseFloat(jQuery(this).find("value").text());
        } // chemName
      });
    } // propName
  });

  return pka;
}

function addQsarToSelector(params)
{
  var sel = document.getElementById("molQsarCalcSel");
  var opt = document.createElement("option");

  if (params !== null)
  {
    opt.text = params.name;
    opt.value = params.qsar_id;

    // for IE earlier than version 8
    try {
      sel.add(opt, sel.options[null]);
    } catch (e) {
      sel.add(opt, null);
    }
  }
}

function loadQsarFromDB(params)
{
  qsarsList = JSON.parse(loadQsarUsingJsp(params));

  for (qsar_id in qsarsList)
  {
    if (qsarsList.hasOwnProperty(qsar_id))
    {
      addQsarToSelector({
        name : qsarsList[qsar_id].Alias,
        qsar_id : qsar_id
      });
    }
  }
}

function loadQsarUsingJsp(params) {
  var results;

  jQuery.ajax({
    // for debugging. turn on to always show qsars
    //url : qsarQueryUrl + "?respiration_name=Anaerobic&media_name=Benthic Sediment",
    url : qsarQueryUrl + "?respiration_name=" + params.respiration_name + "&media_name=" + params.media_name,
    async : false,
    type : 'GET',
    success : function(response) {
        results = response;
      },
    error : function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
      }
  });
  return results;
}

function execQsarUsingJsp(params) {
  var results;

  jQuery.ajax({
    url : queryExecUrl(params),
    async : false,
    type : 'GET',
    success : function(response) {
        results = response;
      },
    error : function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
      }
  });
  return results;
}

function queryExecUrl(params) {
  var ajaxURI = "http://pnnl.cloudapp.net/efs/qsarExec.jsp?qsar_id=";
  ajaxURI += params.qsar_id;
  ajaxURI += "&pka=" + params.pka;

  return ajaxURI;
}

var QSAR = {
  init: function() {
    loadQsars();
  }
}