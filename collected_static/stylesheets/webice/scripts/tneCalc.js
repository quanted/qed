// if (!document.URL.split("?")[1])
// 	location.href="index.html";
var attributes = '';
var Params = {};
var regexp = /\+/g;
var surrogateArray = [];
var toxicityArray = [];
var predictedArray = [];
var filenameArray = [];
var dataToxArray = [];
var xmlDocArray = [];
var taxaSurrArray = [];
var varNames = [];

attributes = document.URL.split("?")[1];
var qs = attributes.split("&");
// we know that for this case we have no repeated
// keys, so parsing to a 1-level hash works

for (var i in qs) {
  var nmval=qs[i].split("=");
  var name=unescape(nmval[0]);
  var value;
  if (nmval.length==2)
    value = unescape(nmval[1].replace(regexp, " "));
  else
    value = name;
if (name=="S")
	surrogateArray.push(value);
else if (name=="T")
	toxicityArray.push(value);
else {
	varNames.push(name);
	Params[name]=value;
}

}

var fileFamily=Params['file'];
	
var surrogates = surrogateArray.join(", ");
var toxicities = toxicityArray.join(", ");

var allValues = [];

var slope;
var intercept;

if (fileFamily.substr(0,4) == 'tneW') {
	specType = 'Wildlife'; units = 'mg/kg bw';	}

if (fileFamily.substr(0,4) == 'tneA') {
	specType = 'Aquatic'; units = String.fromCharCode(956) +'g/L';	}

function log10(val)
{
	return Math.log(val)/Math.LN10;
}

function valueByLeafTag (pnode,leafname) 
{
  return pnode.getElementsByTagName(leafname)[0].childNodes[0].nodeValue;
}

function snToDecText(number)
{
	var returnVal = "";
	textVal = number+"";
	if (textVal.indexOf("e")<1)
		return number;
	components = textVal.split("e");
	leadNum = components[0].split(".")[0];
	remainNum = components[0].split(".")[1];
	if(components[1]<0)
	{
		returnVal = "0.";
		for(j=1;j<Math.abs(components[1]);j++)
			returnVal += "0";
		returnVal += leadNum+"";
		returnVal += remainNum+"";
	}
	else
		if (remainNum.length-components[1]>0)
		{
			returnVal = leadNum+"";
			returnVal += remainNum.substr(0,components[1]);
			returnVal += "."+remainNum.substr(components[1],remainNum.length);
		}
		else
		{
			returnVal = leadNum+""+remainNum;
			for(j=1;j<components[1]-remainNum.length;j++)
			returnVal += "0";
		}
	//alert(number+" : "+returnVal);
	return returnVal;	
}

function showSigDig(value, noDig)
{
	//Note: never returns less than 1 after decimal
	if (isNaN(value))
		return value; 
	if (noDig < 1 || isNaN(noDig)) 
		if (value < 1) 
			noDig = 3;
		else
			noDig = 2;
	var textVal = value+"";
	if (textVal.indexOf("e")>0)
		textVal	= snToDecText(value);	
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

function popHeader () 
{
	document.getElementById('PageName').appendChild(document.createTextNode(" - "+specType));
	document.title = surrogates + ' | ' + document.title;
	var linkname = "iceTNESpecies.html?filename=tneWs";
	if (specType == 'Aquatic') {
		linkname = "iceTNESpecies.html?filename=tneAs"
	}
	// newBClink = document.createElement('a');
	// newBClink.setAttribute('href',linkname);
	// newBClink.appendChild(document.createTextNode(specType+' Species'));
	// oldBC = document.createElement('li');
	// oldBC.appendChild(newBClink);
	// newBC = document.createElement('li');
	// newBC.appendChild(document.createTextNode('Results'));
	// if(!document.getElementById('breadcrumbs').lastChild.childNodes.length)
	// 	document.getElementById('breadcrumbs').removeChild(document.getElementById('breadcrumbs').lastChild);
	// document.getElementById('breadcrumbs').removeChild(document.getElementById('breadcrumbs').lastChild);
	// document.getElementById('breadcrumbs').appendChild(oldBC);
	// document.getElementById('breadcrumbs').appendChild(newBC);
}

function file2fetch (surr) 
{
	// Changed dir by J. Flaishans
	return 'http://s3.amazonaws.com/webice/data/'+fileFamily+surr+'.xml?rand='+Math.random();
}

function addXMLDoc()
{
	var i = xmlDocArray.length;
	if (document.implementation && document.implementation.createDocument)
		xmlDocArray[i]=document.implementation.createDocument("", "doc", null); 
	else if (window.ActiveXObject){
		xmlDocArray[i] = new ActiveXObject("Microsoft.XMLDOM");
		xmlDocArray[i].async = false;
	}
	return i;
}

function loadDataAlltypes(xmlIndex,predicted,index,filename) {
  return function() {
  loadData(xmlDocArray[xmlIndex],predicted,index,filename);
  }
}

function loadAllLookups(index) {
  return function() {
  loadLookup(xmlDocArray[index],index);
  }
}

function begin()
{
    popHeader();

	for (p=0;p<=surrogateArray.length;p++)
		addXMLDoc();
		
    document.getElementById('speciesIn').appendChild(document.createTextNode(" "+surrogates));
    document.getElementById('toxValIn').appendChild(document.createTextNode(" "+toxicities+" "+units));
 
   for (usv=0;usv<varNames.length;usv++)
	if (document.getElementById(varNames[usv]))
		document.getElementById(varNames[usv]).value=Params[varNames[usv]];
 
   for (a=0;a<surrogateArray.length;a++)
   {
	var file=file2fetch(surrogateArray[a]);
	importLookupFile(xmlDocArray[a],file,a);
	}
}

function getData(filesource, predicted, index)
{
	// Change dir by J. Flaishans
	var filename = 'http://s3.amazonaws.com/webice/data/'+filesource;
	var xmlIndex = addXMLDoc();
	
	importFile(xmlDocArray[xmlIndex],filename,predicted,index,xmlIndex);
}
		
function importLookupFile(xmlDoc,fileName,index) 
{	 
	if (document.implementation && document.implementation.createDocument)
	{ 
		var xmlhttp = new window.XMLHttpRequest();
		xmlhttp.open("GET",fileName,false);
		xmlhttp.send(null);
		xmlDoc = xmlhttp.responseXML.documentElement;
		xmlDocArray[index]=xmlDoc;
		loadLookup(xmlDocArray[index],index);


//		xmlDoc.load(fileName);
//		xmlDoc.onload = loadAllLookups(index);
	}
	else if (window.ActiveXObject) 
	{
		xmlDoc.load(fileName);
		//xmlDoc.async = false;
		xmlDocArray[index]=xmlDoc;
		loadLookup(xmlDocArray[index],index);
 	}
}

function loadLookup(xmlDoc,index)
{ 
	type="all";
	for (i=0;i<(xmlDoc.getElementsByTagName("cross").length>500?500:xmlDoc.getElementsByTagName("cross").length);i++) 
	{
	  var row = xmlDoc.getElementsByTagName("cross")[i];
	  var predicted = valueByLeafTag(row,'predicted');
	  var group = valueByLeafTag(row,'group');
	  var filesource = valueByLeafTag(row,'filesource');
	  var species = valueByLeafTag(row,'species');
	  
		if (Params['species'] && Params['species'] != 'All')
		{
			if (Params['species']==species)
			{
	  			if (taxaSurrArray[Params['species']+predicted+surrogateArray[index]])
	  				void(0);
		  		else
	  			{ 
	  				taxaSurrArray[Params['species']+predicted+surrogateArray[index]] = 1;
					getData(filesource,predicted,index);
		  		}
			}
		}
		else if (Params['group'])
		{ 
		  	if (Params['group']==group)
			{
	  			if (taxaSurrArray[Params['group']+predicted+surrogateArray[index]])
	  				void(0);
		  		else
	  			{ 
	  				taxaSurrArray[Params['group']+predicted+surrogateArray[index]] = 1;
					getData(filesource,predicted,index);
		  		}
		  	}
		 }
		 else
		 {
	  		if (taxaSurrArray[predicted+surrogateArray[index]])
	  			void(0);
		  	else
	  		{ 
	  			taxaSurrArray[predicted+surrogateArray[index]] = 1;
				getData(filesource,predicted,index);
		  	}
		  }
	  }  
}
		
function importFile(xmlDoc,fileName,predicted,index,xmlIndex) 
{ 
	if (document.implementation && document.implementation.createDocument)
	{ 
		var xmlhttp = new window.XMLHttpRequest();
		xmlhttp.open("GET",fileName,false);
		xmlhttp.send(null);
		xmlDoc = xmlhttp.responseXML.documentElement;
		xmlDocArray[xmlIndex]=xmlDoc;
		loadData(xmlDocArray[xmlIndex],predicted,index, fileName);

//		xmlDoc.load(fileName);
//		xmlDoc.onload = loadDataAlltypes(xmlIndex,predicted,index, fileName);
	}
	else if (window.ActiveXObject) 
	{
		xmlDoc.load(fileName);
		//xmlDoc.async = false;
		xmlDocArray[xmlIndex]=xmlDoc;
		loadData(xmlDocArray[xmlIndex],predicted,index, fileName);
 	}
}
http://s3.amazonaws.com/webice/data/afSurrFathead
function loadData(xmlDoc,predSpec,index, filename)
{ 
	var predFound = false;
	var level = '';
	var useRow = 1;
	// Changed by J. Flaishans (filename => filenameUber):
	filenameUberIndex = filename.indexOf("data/");
	filenameUber = filename.substring(filenameUberIndex);
	if (filenameUber.charAt(6) == 's') level = 'species';
	if (filenameUber.charAt(6) == 'f') level = 'family';
	if (filenameUber.charAt(6) == 'g') level = 'genus';
	for (p=0;p<(xmlDoc.getElementsByTagName("cross").length>500?500:xmlDoc.getElementsByTagName("cross").length);p++) 
	{
	  var row = xmlDoc.getElementsByTagName("cross")[p];
	  var predicted = valueByLeafTag(row,'predicted');
	  if (predicted == predSpec)
	  { 
		predFound = true;
		var surrogateName = surrogateArray[index];
		var txcity = toxicityArray[index];
		var slope = parseFloat(valueByLeafTag(row,'slope'));
		var intercept = parseFloat(valueByLeafTag(row,'intercept'));
		var xMin = Math.pow(10,parseFloat(valueByLeafTag(row,'xMin')));
		var xMax = Math.pow(10,parseFloat(valueByLeafTag(row,'xMax')));
		var r2 = valueByLeafTag(row,'r2');
		var df = parseInt(valueByLeafTag(row,'df'));
		var pVal = valueByLeafTag(row,'pVal');
		var xAvg = valueByLeafTag(row,'xAvg');
		var Sxx = valueByLeafTag(row,'Sxx');
		var MSE = valueByLeafTag(row,'MSE');
		var Bootstrap = valueByLeafTag(row,'Bootstrap');
		var taxDist = valueByLeafTag(row,'taxDist');
		var t95CI = parseFloat(valueByLeafTag(row,'t95CI'));
		//var xrowType= valueByLeafTag(row,'type');
		var predTox = runCalculation(txcity,slope,intercept);
		var diff = t95CI * Math.sqrt( MSE * (1/(df+2) + Math.pow(log10(txcity) - xAvg, 2)/Sxx));
		var lower = showSigDig(Math.pow(10,(log10(predTox) - diff)));
		var upper = showSigDig(Math.pow(10,(log10(predTox) + diff)));
		var msg = '';
	    if (txcity > xMax) 
	      msg = '* Input toxicity greater than model maximum of '+showSigDig(xMax);
		else if (txcity < xMin) 
    	  msg = '* Input toxicity less than model minimum of '+showSigDig(xMin);

	if (Params['dofUL'] && parseFloat(Params['dofUL'])<parseFloat(df)) useRow=0;
	if (Params['dofLL'] && parseFloat(Params['dofLL'])>parseFloat(df)) useRow=0;
	if (Params['cvsUL'] && (parseFloat(Params['cvsUL'])<parseFloat(Bootstrap)||isNaN(parseFloat(Bootstrap)))) useRow=0;
	if (Params['cvsLL'] && (parseFloat(Params['cvsLL'])>parseFloat(Bootstrap)||isNaN(parseFloat(Bootstrap)))) useRow=0;
	if (Params['r2UL'] && parseFloat(Params['r2UL'])<parseFloat(r2)) useRow=0;
	if (Params['r2LL'] && parseFloat(Params['r2LL'])>parseFloat(r2)) useRow=0;
	if (Params['tdUL'] && parseFloat(Params['tdUL'])<parseFloat(taxDist)) useRow=0;
	if (Params['tdLL'] && parseFloat(Params['tdLL'])>parseFloat(taxDist)) useRow=0;
	if (Params['pvUL'] && parseFloat(Params['pvUL'])<parseFloat(pVal)) useRow=0;
	if (Params['pvLL'] && parseFloat(Params['pvLL'])>parseFloat(pVal)) useRow=0;
	if (Params['sUL'] && parseFloat(Params['sUL'])<parseFloat(slope)) useRow=0;
	if (Params['sLL'] && parseFloat(Params['sLL'])>parseFloat(slope)) useRow=0;
	if (Params['mseUL'] && parseFloat(Params['mseUL'])<parseFloat(MSE)) useRow=0;
	if (Params['mseLL'] && parseFloat(Params['mseLL'])>parseFloat(MSE)) useRow=0;
	if (Params['intUL'] && parseFloat(Params['intUL'])<parseFloat(intercept)) useRow=0;
	if (Params['intLL'] && parseFloat(Params['intLL'])>parseFloat(intercept)) useRow=0;

	if (useRow)
		checkTNERow(predicted, level, predTox,Math.pow(10,(log10(predTox) - diff)),Math.pow(10,(log10(predTox) + diff)), showSigDig(predTox), lower, upper, txcity, type, surrogateName, parseInt(df), showSigDig(r2,2), showSigDig(pVal,4), showSigDig(MSE,2), showSigDig(Bootstrap,6), parseInt(taxDist), showSigDig(slope,2), showSigDig(intercept,2), msg);

	 useRow = 1;
	  }
	}
	if (!predFound) alert(predSpec+" not found in file "+filename);
}

function runCalculation(input, slope, intercept)
{

	var sigDig = 0;
    var result = 0;
	
	if (input != '')
		result = Math.pow(10,intercept+slope*log10(input));

	return result;
}

function checkTNERow (species, level, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg)
{
	/* alert(species);
	if (surrogates.indexOf(species)>=0) return 0;
	if (document.getElementById(species.substring(species.indexOf('(')+1,species.indexOf(')'))))
	{
		valuesToCompare=document.getElementById(species.substring(species.indexOf('(')+1,species.indexOf(')'))).value.split(',');
		if(valuesToCompare[2]/valuesToCompare[0] > upperValue/toxValue)
		{
			dropSSDRow(species.substring(species.indexOf('(')+1,species.indexOf(')')));
			showTNERow (species, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg);
		}
	}
	else */
	showTNERow (species, level, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg);
}

function createTNERow (species, level, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg)
{
	if (!msg)
		msg='';

	newRow = document.createElement('tr');
	specCell = document.createElement('td');
	specCell.appendChild(document.createTextNode(species));
	levelCell = document.createElement('td');
	levelCell.appendChild(document.createTextNode(level));
	dataCell = document.createElement('td');
	dataCell.setAttribute('align','center');
	dataCell.appendChild(document.createTextNode(surrogateName));
	toxCell = document.createElement('td');
	toxCell.setAttribute('align','center');
	if (msg != '')
		toxCell.className = 'outsideRange';
	toxCell.appendChild(document.createTextNode(toxValue));
	lowerCell = document.createElement('td');
	lowerCell.setAttribute('align','center');
	lowerCell.appendChild(document.createTextNode(lowerValue+' - '+upperValue));
	dfCell = document.createElement('td');
	dfCell.appendChild(document.createTextNode(df));
	dfCell.setAttribute('align','center');
	r2Cell = document.createElement('td');
	r2Cell.appendChild(document.createTextNode(r2));
	r2Cell.setAttribute('align','center');
	pValCell = document.createElement('td');
	pValCell.appendChild(document.createTextNode(pVal));
	pValCell.setAttribute('align','center');
	MSECell = document.createElement('td');
	MSECell.appendChild(document.createTextNode(MSE));
	MSECell.setAttribute('align','center');
	bootCell = document.createElement('td');
	bootCell.appendChild(document.createTextNode(Bootstrap));
	bootCell.setAttribute('align','center');
	taxCell = document.createElement('td');
	taxCell.appendChild(document.createTextNode(taxDist));
	taxCell.setAttribute('align','center');
	slopeCell = document.createElement('td');
	slopeCell.setAttribute('align','center');
	slopeCell.appendChild(document.createTextNode(slope));
	IntCell = document.createElement('td');
	IntCell.setAttribute('align','center');
	IntCell.appendChild(document.createTextNode(intercept));
	msgCell = document.createElement('td');
	msgCell.appendChild(document.createTextNode(msg));
	msgCell.className = 'outsideRange';
	newRow.appendChild(specCell);
	newRow.appendChild(levelCell);
	newRow.appendChild(dataCell);
	newRow.appendChild(toxCell);
	newRow.appendChild(lowerCell);
	newRow.appendChild(dfCell);
	newRow.appendChild(r2Cell);
	newRow.appendChild(pValCell);
	newRow.appendChild(MSECell);
	newRow.appendChild(bootCell);
	newRow.appendChild(taxCell);
	newRow.appendChild(slopeCell);
	newRow.appendChild(IntCell);
	newRow.appendChild(msgCell);

	return newRow;
}

function showTNERow (species, level, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg)
{
	if (!msg)
		msg='';

	rowObject = createTNERow(species, level, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg);

	document.getElementById("tneResults").tBodies[0].appendChild(rowObject);
}

function dropSSDRow(dropID)
{
	if (document.getElementById(dropID))
	{
		document.getElementById(dropID).parentNode.parentNode.parentNode.removeChild(document.getElementById(dropID).parentNode.parentNode);
	}
}

function checkBoxClick()
{
	if (!this.checked) makeGrey(this.id); else makeLive(this.id); reCompute();
}

function makeGrey(idVal)
{
	boxNum = document.getElementById(idVal);
	boxNum.defaultChecked = false;
	tdParent = boxNum.parentNode;
	trParent = tdParent.parentNode;
	trParent.className = 'greyedOut';
}

function makeLive(idVal)
{
	boxNum = document.getElementById(idVal);
	boxNum.defaultChecked = true;
	tdParent = boxNum.parentNode;
	trParent = tdParent.parentNode;
	trParent.className = null;
}

function reCompute()
{
	getHCP();
	getHCPLower();
	getHCPUpper();
}

function getAlpha()
{
    // For multi-surrogate populations, add all relevant log toxicities
    // and sum over all the logs.
  var totVal = 0;
  var valCount = 0;
  for (j=0;j<toxicityArray.length;j++)
  {
	 totVal += log10(toxicityArray[j]);
	 valCount += 1;
  }
	for (i=0;i<document.getElementsByTagName('input').length;i++)
		if (document.getElementsByTagName('input')[i].checked)
			if(document.getElementsByTagName('input')[i].type=="checkbox")
			{
				totVal += log10(parseFloat(document.getElementsByTagName('input')[i].value.split(',')[0]));
				valCount += 1;
			}
	//alert(valCount);
		//alert(totVal/valCount);
	return totVal/valCount;	
}

function getBeta(mean)
{
    var beta = 0;
    var totDiff = 0;
    var valCount = 0;
  for (j=0;j<toxicityArray.length;j++)
  {
	  totDiff += Math.pow((log10(toxicityArray[j]) - mean), 2);
	  valCount += 1;
  }
 	for (j=0;j<document.getElementsByTagName('input').length;j++)
		if (document.getElementsByTagName('input')[j].checked)
			if(document.getElementsByTagName('input')[j].type=="checkbox")
			{
				totDiff += Math.pow((log10(parseFloat(document.getElementsByTagName('input')[j].value.split(',')[0]))-mean),2);
				valCount += 1;
			}
	//	alert(totDiff);
	beta = Math.sqrt(totDiff/(valCount-1))*Math.sqrt(3)/Math.PI;
	//	alert(beta);
	return beta;
}

function getHCP()
{
	var p = parseFloat(document.getElementById('Percent').options[document.getElementById('Percent').selectedIndex].value)/100;
	var alpha = getAlpha();
	var beta = getBeta(alpha);
	var HCP = Math.log(1/p-1);
	HDVal = Math.pow(10,(HCP*(-1)*beta+alpha));
	if (HDVal < 1)
		HDVal = showSigDig(HDVal,(HDVal+'').split(".")[1].search(/[1-9]/)+3);
	else
		HDVal = showSigDig(HDVal);
	if(document.getElementById('HCPval').childNodes.length)
		document.getElementById('HCPval').removeChild(document.getElementById('HCPval').firstChild);
	document.getElementById('HCPval').appendChild(document.createTextNode(HDVal+" "+units));
}

function getAlphaLower()
{
	var totVal = 0;
	var valCount = 0;
	for (i=0;i<document.getElementsByTagName('input').length;i++)
		if (document.getElementsByTagName('input')[i].checked)
			if(document.getElementsByTagName('input')[i].type=="checkbox")
			{
				totVal += log10(parseFloat(document.getElementsByTagName('input')[i].value.split(',')[1]));
				valCount += 1;
			}
	//alert(valCount);
	return totVal/valCount;	
}

function getBetaLower(mean)
{
	var beta = 0;
	var totDiff = 0;
	var valCount = 0;
	for (j=0;j<document.getElementsByTagName('input').length;j++)
		if (document.getElementsByTagName('input')[j].checked)
			if(document.getElementsByTagName('input')[j].type=="checkbox")
			{
				totDiff += Math.pow((log10(parseFloat(document.getElementsByTagName('input')[j].value.split(',')[1]))-mean),2);
				valCount += 1;
			}
	beta = Math.sqrt(totDiff/(valCount-1))*Math.sqrt(3)/Math.PI;
	return beta;
}

function getHCPLower()
{
	var p = parseFloat(document.getElementById('Percent').options[document.getElementById('Percent').selectedIndex].value)/100;
	var alpha = getAlphaLower();
	var beta = getBetaLower(alpha);
	var HCP = Math.log(1/p-1);
	HDVal = Math.pow(10,(HCP*(-1)*beta+alpha));
	if (HDVal < 1)
		HDVal = showSigDig(HDVal,(HDVal+'').split(".")[1].search(/[1-9]/)+3);
	else
		HDVal = showSigDig(HDVal);
	if(document.getElementById('HCPLower').childNodes.length)
		document.getElementById('HCPLower').removeChild(document.getElementById('HCPLower').firstChild);
	document.getElementById('HCPLower').appendChild(document.createTextNode(" \u00a0 \u00a0 95% Confidence Interval: "+HDVal));
}

function getAlphaUpper()
{
	var totVal = 0;
	var valCount = 0;
	for (i=0;i<document.getElementsByTagName('input').length;i++)
		if (document.getElementsByTagName('input')[i].checked)
			if(document.getElementsByTagName('input')[i].type=="checkbox")
			{
				totVal += log10(parseFloat(document.getElementsByTagName('input')[i].value.split(',')[2]));
				valCount += 1;
			}
	//alert(valCount);
	return totVal/valCount;	
}

function getBetaUpper(mean)
{
	var beta = 0;
	var totDiff = 0;
	var valCount = 0;
	for (j=0;j<document.getElementsByTagName('input').length;j++)
		if (document.getElementsByTagName('input')[j].checked)
			if(document.getElementsByTagName('input')[j].type=="checkbox")
			{
				totDiff += Math.pow((log10(parseFloat(document.getElementsByTagName('input')[j].value.split(',')[2]))-mean),2);
				valCount += 1;
			}
	beta = Math.sqrt(totDiff/(valCount-1))*Math.sqrt(3)/Math.PI;
	return beta;
}

function getHCPUpper()
{
	var p = parseFloat(document.getElementById('Percent').options[document.getElementById('Percent').selectedIndex].value)/100;
	var alpha = getAlphaUpper();
	var beta = getBetaUpper(alpha);
	var HCP = Math.log(1/p-1);
	HDVal = Math.pow(10,(HCP*(-1)*beta+alpha));
	if (HDVal < 1)
		HDVal = showSigDig(HDVal,(HDVal+'').split(".")[1].search(/[1-9]/)+3);
	else
		HDVal = showSigDig(HDVal);
	if(document.getElementById('HCPUpper').childNodes.length)
		document.getElementById('HCPUpper').removeChild(document.getElementById('HCPUpper').firstChild);
	document.getElementById('HCPUpper').appendChild(document.createTextNode(" - "+HDVal));
}

var tableID = "tneResults";

function createExcelSheet(allRows)
{

	if (window.ActiveXObject) 
	{
		try 
		{
			var offSet = 0;
		
			var xlApp = new ActiveXObject("Excel.Application"); 
			var xlBook = xlApp.Workbooks.Add();
	
			xlBook.worksheets("Sheet1").activate;
			var XlSheet = xlBook.activeSheet;
			xlApp.visible = true; 

			for (i=0; i < document.getElementById(tableID).rows.length; i++)
			{
				for (j=2; j < document.getElementById(tableID).rows[i].cells.length; j++) 
				{
					mycellValue = document.getElementById(tableID).rows[i].cells[j].innerText;
					if (i==0) mycellValue = mycellValue.substring(0,mycellValue.indexOf('Sort')-2); 
					XlSheet.Cells(i+1-offSet,j-1).Value = mycellValue; 
				} 
			}

			XlSheet.columns.autofit; 
		}
		catch (e) 
		{ 
			void(0);//Do nothing; 
		} 
	}
	if (xlApp) { void(0); }
	else {
		ICETable = window.open("ICETable.html","ICETable","");
		setTimeout('populateTable('+allRows+')', 1000); }
}

function populateTable (allRows)
{
	for (i=0; i < document.getElementById(tableID).rows.length; i++) 
	{
		newRow = ICETable.document.getElementById('ICEOutput').insertRow(ICETable.document.getElementsByTagName('tr').length);
		for (j=2; j < document.getElementById(tableID).rows[i].cells.length; j++) 
		{
			newCell = ICETable.document.createElement('td');
			if (document.getElementById(tableID).rows[i].cells[j].childNodes[0]) 
			{
				mycellValue = document.getElementById(tableID).rows[i].cells[j].childNodes[0].nodeValue;
				if (i==0 && mycellValue.indexOf('Sort') > 0) mycellValue.substring(0,mycellValue.indexOf('Sort')-2); 
					newCell.appendChild(ICETable.document.createTextNode(mycellValue )); 
			}
			newRow.appendChild(newCell); 
		} 
	} 
}

function filterData()
{

	var inputFields;
	var textInputs = [];
	var pageAddress = document.URL;

	if (pageAddress.indexOf("#")>1)
		pageAddress = pageAddress.substr(0,pageAddress.length-2);

	if (pageAddress.indexOf("&dofUL")>1)
		pageAddress = pageAddress.substr(0,pageAddress.indexOf("&dofUL"));

	if (document.getElementById("dofUL"))
	{

		inputFields = document.getElementsByTagName('input');
		for (q=0; q < inputFields.length; q++) 
			if (inputFields[q].type == 'text') 
				if (inputFields[q].id!='searchbox')
				pageAddress += "&"+inputFields[q].id+"="+inputFields[q].value;
		//alert(pageAddress);
		document.location=pageAddress;
	}
}