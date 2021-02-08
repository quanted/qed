// if (!document.URL.split("?")[1])
// 	location.href="index.html"; 
var attributes = '';
attributes = document.URL.split("?")[1];
attribute1 = attributes.split("&")[0];
attribute2 = attributes.split("&")[1];
attribute3 = attributes.split("&")[2];
var fileFamily = attribute3.split("=")[1];
var regexp = /\+/g;
var chosenSurrogate = unescape(attribute1.split("=")[1].replace(regexp, " "));
var chosenPredicted = unescape(attribute2.split("=")[1].replace(regexp, " "));
var xmlDoc;

var slope;
var intercept;
var r2;
var df;
var pVal;
var xAvg;
var xMin;
var xMax;
var Sxx;
var MSE;
var Bootstrap;
var taxDist;
var t90CI;
var t95CI;
var t99CI;


if (fileFamily.substr(0,1) == 'w')
{
	specType = 'Wildlife'; units = 'mg/kg bw';	
}

if (fileFamily.substr(0,1) == 'a')
{
  specType = 'Aquatic'; units =  String.fromCharCode(956) +'g/L';	
}

if (fileFamily.substr(0,1) == 'l')
{
  specType = 'Algae'; units =  String.fromCharCode(956) +'g/L';	
}

function begin()
{
	// Changed DIR by J. Flaishans
	file = 'http://s3.amazonaws.com/webice/data/'+fileFamily+'Surr'+chosenSurrogate+'.xml?rand='+Math.random();
	importFile(file);
}

function importFile(fileName) {
	
	if (document.implementation && document.implementation.createDocument)
	{
		var xmlhttp = new window.XMLHttpRequest();
		xmlhttp.open("GET",file,false);
		xmlhttp.send(null);
		xmlDoc = xmlhttp.responseXML.documentElement;
		loadData();

//		xmlDoc=document.implementation.createDocument("", "doc", null) 
//		xmlDoc.load(file); 
//		xmlDoc.onload = loadData; 
	}
	else if (window.ActiveXObject)
	{
		xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
		xmlDoc.onreadystatechange = function () {
			if (xmlDoc.readyState == 4) loadData() };
		xmlDoc.load(file); 
 	}
}

function log10(val)
{
	return Math.log(val)/Math.LN10;
}

function valueByLeafTag (pnode,leafname) 
{
  return pnode.getElementsByTagName(leafname)[0].childNodes[0].nodeValue;
}

function loadData()
{
  nCount = 0; extraNode = 1;
  if(xmlDoc.getElementsByTagName("cross")[0].childNodes.length > 25) 
    extraNode = 2;
  predictedNode = (extraNode*nCount++)+(extraNode-1);
  r2Node = (extraNode*nCount++)+(extraNode-1);
  pValNode = (extraNode*nCount++)+(extraNode-1);
  dfNode = (extraNode*nCount++)+(extraNode-1);
  interceptNode = (extraNode*nCount++)+(extraNode-1);
  slopeNode = (extraNode*nCount++)+(extraNode-1);
  xAvgNode = (extraNode*nCount++)+(extraNode-1);
  xMinNode = (extraNode*nCount++)+(extraNode-1);
  xMaxNode = (extraNode*nCount++)+(extraNode-1);
  SxxNode = (extraNode*nCount++)+(extraNode-1);
  MSENode = (extraNode*nCount++)+(extraNode-1);
  t90CINode = (extraNode*nCount++)+(extraNode-1);
  t95CINode = (extraNode*nCount++)+(extraNode-1);
  t99CINode = (extraNode*nCount++)+(extraNode-1);
  BootstrapNode = (extraNode*nCount++)+(extraNode-1);
  taxDistNode = (extraNode*nCount++)+(extraNode-1);

  for (i=0;i<(xmlDoc.getElementsByTagName("cross").length>500?500:xmlDoc.getElementsByTagName("cross").length);i++) 
    {
      var row = xmlDoc.getElementsByTagName("cross")[i];
      if (valueByLeafTag(row,'predicted') == chosenPredicted)
	{
	  slope = row.childNodes[slopeNode].childNodes[0].nodeValue;
	  intercept = row.childNodes[interceptNode].childNodes[0].nodeValue;
	  r2 = valueByLeafTag(row,'r2');
	  df = valueByLeafTag(row,'df');
	  pVal = valueByLeafTag(row,'pVal');
	  xAvg = valueByLeafTag(row,'xAvg');
	  xMin = valueByLeafTag(row,'xMin');
	  xMax = valueByLeafTag(row,'xMax');
	  Sxx = valueByLeafTag(row,'Sxx');
	  MSE = valueByLeafTag(row,'MSE');
	  Bootstrap = valueByLeafTag(row,'Bootstrap');
	  taxDist = valueByLeafTag(row,'taxDist');
	  t90CI = valueByLeafTag(row,'t90CI');
	  t95CI = valueByLeafTag(row,'t95CI');
	  t99CI = valueByLeafTag(row,'t99CI');
	}
    }
  
  document.getElementById("inputToxCell").insertBefore(document.createTextNode(units), document.getElementById('inputToxLog'));
  
  showModelInfo();
}

function clearInfo ()
{
	if (document.getElementById('inputToxLog').childNodes[0])
		document.getElementById('inputToxLog').removeChild(document.getElementById('inputToxLog').childNodes[0]);
	if (document.getElementById('predictedTox').childNodes[0])
		document.getElementById('predictedTox').removeChild(document.getElementById('predictedTox').childNodes[0]);
	if (document.getElementById('lowerLimit').childNodes[0])
		document.getElementById('lowerLimit').removeChild(document.getElementById('lowerLimit').childNodes[0]);
	if (document.getElementById('upperLimit').childNodes[0])
		document.getElementById('upperLimit').removeChild(document.getElementById('upperLimit').childNodes[0]);
	if (document.getElementById('msgCell').childNodes[0])
		document.getElementById('msgCell').removeChild(document.getElementById('msgCell').childNodes[0]);
	document.getElementById('msgCell').className = "";
}

function showImage()
{
	var picName;
	if (fileFamily.substr(0,1) != 'l')
	{
		if (fileFamily.substr(0,1) == 'a')
		{
			if (chosenSurrogate.indexOf('(') > 0)
				picName = chosenSurrogate.substring(chosenSurrogate.indexOf('(')+1,chosenSurrogate.length-1);
			else
				picName = chosenSurrogate;
			if (chosenPredicted.indexOf('(') > 0)
				picName += chosenPredicted.substring(chosenPredicted.indexOf('(')+1,chosenPredicted.length-1);
			else
				picName += chosenPredicted;
			picName = picName.replace(/\s/g, "");
			picName = picName.replace(/-/g, "");
			picName += '.gif';
		}
		else
		{
			if (chosenSurrogate.indexOf('(') > 0)
				picName = chosenSurrogate.substring(0,chosenSurrogate.indexOf('(')-1);
			else
				picName = chosenSurrogate;
			if (chosenPredicted.indexOf('(') > 0)
				picName += chosenPredicted.substring(0,chosenPredicted.indexOf('(')-1);
			else
				picName += chosenPredicted;
			picName = picName.replace(/\s/g, "");
			picName = picName.replace(/-/g, "");
			picName += '.gif';
		}
		pic = document.createElement('img');
		pic.setAttribute('src','http://s3.amazonaws.com/webice/images/'+picName);
		pic.setAttribute('alt','ICE model graph for this species pair');
		//pic.setAttribute('width','375');
		document.getElementById('graphImage').appendChild(pic);
	}
}

function showModelInfo()
{
	document.getElementById('interceptText').appendChild(document.createTextNode(showSigDig(intercept,6)));
	document.getElementById('slopeText').appendChild(document.createTextNode(showSigDig(slope,6)));
	document.getElementById('dfText').appendChild(document.createTextNode(parseInt(df)));
	document.getElementById('r2Text').appendChild(document.createTextNode(showSigDig(r2,6)));
	document.getElementById('pValText').appendChild(document.createTextNode(showSigDig(pVal,6)));
	document.getElementById('xAvgText').appendChild(document.createTextNode(showSigDig(Math.pow(10,xAvg),6)+" ("+showSigDig(xAvg,6)+")"));
	document.getElementById('xMinText').appendChild(document.createTextNode(showSigDig(Math.pow(10,xMin),6)+" ("+showSigDig(xMin,6)+")"));
	document.getElementById('xMaxText').appendChild(document.createTextNode(showSigDig(Math.pow(10,xMax),6)+" ("+showSigDig(xMax,6)+")"));
	document.getElementById('MSEText').appendChild(document.createTextNode(showSigDig(MSE,6)));
	document.getElementById('SxxText').appendChild(document.createTextNode(showSigDig(Sxx,6)));
	if (Bootstrap == 'na')
		document.getElementById('BootText').appendChild(document.createTextNode(Bootstrap));
	else
		document.getElementById('BootText').appendChild(document.createTextNode(showSigDig(Bootstrap,6)));
	document.getElementById('taxDistText').appendChild(document.createTextNode(parseInt(taxDist)));
	showImage();
}

function showSigDig(value, noDig)
{
	//Note: never returns less than 1 after decimal
	if (noDig < 1 || isNaN(noDig)) 
		if (value < 1) 
			noDig = 3;
		else
			noDig = 2;
	var textVal = value+"";
	if (textVal.indexOf("e")>0) return value;
	textVal = textVal.split(".");
	if (textVal[2])
		return;
	if (textVal[0] != '')
		if (parseInt(textVal[0]) != 0)
			noDig = 2;
	if (textVal[1])
		textVal[1]=	textVal[1].substr(0,noDig);
	else
		textVal[1]="00";
	return textVal[0]+"."+textVal[1];
}

function runCalculation()
{
	slope = parseFloat(slope);
	intercept = parseFloat(intercept);
	r2 = parseFloat(r2);
	df = parseFloat(df);
	pVal = parseFloat(pVal);
	xAvg = parseFloat(xAvg);
	Sxx = parseFloat(Sxx);
	MSE = parseFloat(MSE);
	t90CI = parseFloat(t90CI);
	t95CI = parseFloat(t95CI);
	t99CI = parseFloat(t99CI);
	xValMin = Math.pow(10,parseFloat(xMin));
	xValMax = Math.pow(10,parseFloat(xMax));

	clearInfo();
	document.getElementById("SurrToxLogText").style.display = "inline";
	document.getElementById("PredToxLogText").style.display = "inline";
	var input = document.getElementById('inputTox').value;
	if (input != '')
	{
		var chkErr = 1;
		if (input < xValMin || input > xValMax)
			chkErr = confirm('This value is outside the x-axis range for this model.\nContinue?');
		if (!chkErr)
			return;
		input = parseFloat(input);
		var surrToxLogText = document.createTextNode(" ("+showSigDig(log10(input))+")");
		document.getElementById("inputToxLog").appendChild(surrToxLogText);
		var predTox = Math.pow(10,intercept+slope*log10(input));
		if (predTox < 1)
			var resultText = document.createTextNode(showSigDig(predTox,(predTox+'').split(".")[1].search(/[1-9]/)+3)+" "+units+" ("+showSigDig(log10(predTox))+")");
		else
			var resultText = document.createTextNode(showSigDig(predTox)+" "+units+" ("+showSigDig(log10(predTox))+")");
		document.getElementById('predictedTox').appendChild(resultText);
		var CI = eval(document.getElementById('ConfInt').value);
		var diff = CI * Math.sqrt( MSE * (1/(df+2) + Math.pow(log10(input) - xAvg, 2)/Sxx));
		var lower = Math.pow(10,(log10(predTox) - diff));
		var upper = Math.pow(10,(log10(predTox) + diff));
		if (lower < 1)
			var lowerText = document.createTextNode(showSigDig(lower,(lower+'').split(".")[1].search(/[1-9]/)+3)+" "+units);
		else
			var lowerText = document.createTextNode(showSigDig(lower)+" "+units);
		if (upper < 1)
			var upperText = document.createTextNode(showSigDig(upper,(upper+'').split(".")[1].search(/[1-9]/)+3)+" "+units);
		else
			var upperText = document.createTextNode(showSigDig(upper)+" "+units);
		document.getElementById('lowerLimit').appendChild(lowerText);
		document.getElementById('upperLimit').appendChild(upperText);
		if (input < xValMin || input > xValMax)
		{
			document.getElementById('msgCell').className = "outsideRange";
			document.getElementById('msgCell').appendChild(document.createTextNode('Surrogate toxicity outside model range.'));	
		}
	}	
}

function popHeader()
{
	var fType;
	if (fileFamily == 'as') fType = 'Aquatic Species';
	if (fileFamily == 'ag') fType = 'Aquatic Genus';
	if (fileFamily == 'af') fType = 'Aquatic Family';
	if (fileFamily == 'ls') fType = 'Algae Species';
	if (fileFamily == 'lg') fType = 'Algae Genus';
	if (fileFamily == 'ws') fType = 'Wildlife Species';
	if (fileFamily == 'wf') fType = 'Wildlife Family';

	var commonSurrogate= chosenSurrogate.split("(")[0];
	var commonPredicted= chosenPredicted.split("(")[0];
	// document.title= commonSurrogate +'-' + commonPredicted + ' | ' + document.title;

	document.getElementById('PageName').appendChild(document.createTextNode(' - '+fType));

	document.getElementById('surrSpecies').appendChild(document.createTextNode(" "+chosenSurrogate));
	document.getElementById('predSpecies').appendChild(document.createTextNode(" "+chosenPredicted));
	
	// var linkname = "getPredSurr.html?filename="+fileFamily;
	// newBClink = document.createElement('a');
	// newBClink.setAttribute('href',linkname);
	// newBClink.appendChild(document.createTextNode(fType+' Taxa Selection'));
	// oldBC = document.createElement('li');
	// oldBC.appendChild(newBClink);
	// newBC = document.createElement('li');
	// newBC.appendChild(document.createTextNode('Calculator'));
	// if(!document.getElementById('breadcrumbs').lastChild.childNodes.length)
	// 	document.getElementById('breadcrumbs').removeChild(document.getElementById('breadcrumbs').lastChild);
	// document.getElementById('breadcrumbs').removeChild(document.getElementById('breadcrumbs').lastChild);
	// document.getElementById('breadcrumbs').appendChild(oldBC);
	// document.getElementById('breadcrumbs').appendChild(newBC);

}
