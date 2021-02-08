function performSearch(smiles)
{
  jQuery("#loading").show();
  jQuery("#numResults").html("Getting table data...");
  jQuery("#spreadsheetResult").html();

  var params = buildRequest(smiles);
  var result = REST.DB.AdvancedSearch(params);

  processResponse(result);
}

function buildRequest(smiles)
{
  // grab search conditions from the UI
  // formula criteria
  var formulaCriteria = "";
  var formulaCondition = jQuery("#molformulaSel").val();
  if (formulaCondition != "")
  {
    if (formulaCondition == "$between")
    {
      formulaCriteria = "\"cd_formula\":{\"$between\":[\"" + jQuery("#formulaOpt1").val() + "\",\"" + jQuery("#formulaOpt2").val() +"\"]}";
    }
    else
    {
      formulaCriteria = "\"cd_formula\":{\""+ formulaCondition +"\":\"" + jQuery("#formulaOpt1").val() + "\"}";
    }
  }

  // mol weight criteria
  var molCriteria = "";
  var molCondition = jQuery("#molweightSel").val();
  if (molCondition != "")
  {
    if (molCondition == "$between")
    {
      molCriteria = "\"cd_molweight\":{\"$between\":[" + jQuery("#weightOpt1").val() + "," + jQuery("#weightOpt2").val() +"]}";
    }
    else
    {
      molCriteria = "\"cd_molweight\":{\""+ molCondition +"\":" + jQuery("#weightOpt1").val() + "}";
    }
  }

  var params = new Object();
  params.smiles = smiles;
  params.searchType = jQuery("#searchTypeSel").val();

  if ((formulaCriteria != "") && (molCriteria != ""))
  {
    params.conditions = JSON.parse("{" + formulaCriteria + "," + molCriteria + "}");
  }
  else if (molCriteria == "")
  {
    params.conditions = JSON.parse("{" + formulaCriteria + "}");
  }
  else if (formulaCriteria == "")
  {
    params.conditions = JSON.parse("{" + molCriteria + "}");
  }
  else
  {
    params.conditions = JSON.parse("{}");
  }

  if (jchemSearch.debug) {
    console.log(formulaCriteria);
    console.log(molCriteria);
  }

  return params;
}

function processResponse(result)
{
  jQuery("#numResults").html("Processing Response...");

  var resultHTML = "<table><tr><th width='150px'>Structure</th><th>Chemical</th><th width='150px'>Formula</th><th width='150px'>Mol Weight</th></tr>";

  for (resultMol in result.data)
  {
    if (result.data.hasOwnProperty(resultMol))
    {
      var id = result.data[resultMol].cd_id;
      var formula = result.data[resultMol].cd_formula;
      var weight = result.data[resultMol].cd_molweight;
      var imgUrl = REST.DB.ImageById(id);
      var molDetails = REST.DB.SimpleDetails(id);
      var iupac = molDetails.format.iupac;
      var smiles = molDetails.format.smiles;

      resultHTML += "<tr>";
      resultHTML += "<td align='center'><img src='" + imgUrl + "' alt='molecule image'></td>";
      resultHTML += "<td><a href='#' onclick='importMol(\"" + smiles + "\")'>" + smiles + "</a><br/>" + iupac + "</td>";
      resultHTML += "<td align='center'>" + formula + "</td>";
      resultHTML += "<td align='center'>" + weight + "</td>";
      resultHTML += "</tr>";
    }
  }

  resultHTML += "</table>";

  jQuery("#loading").hide();
  jQuery("#spreadsheetResult").html(resultHTML);
  jQuery("#numResults").html(result.total + " Results");
}

var jchemSearch = {
  init: function() {
  },

  debug: false
}