// if (!document.URL.split("?")[1])
// 	location.href="index.html";
var attributes = '';
var Params = {};
var regexp = /\+/g;
var surrogateArray = [];
var toxicityArray = [];
var prefixArray = [];
var xmlDocArray = [];
var varNames = [];
var ICETable = '';

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
if (name=="S") //Surrogate
	surrogateArray.push(value);
else if (name=="T") //Toxicity
	toxicityArray.push(value);
else if (name=="F") //File Family
	prefixArray.push(value);
else {
	varNames.push(name);
	Params[name]=value; }
}

for (i=0;i<surrogateArray.length;i++)
{
	if (document.implementation && document.implementation.createDocument)
		xmlDocArray[i]=document.implementation.createDocument("", "doc", null); 
	else if (window.ActiveXObject){
		xmlDocArray[i] = new ActiveXObject("Microsoft.XMLDOM");
		xmlDocArray[i].async = false;
	}
}

var fileFamily=Params['file'];
var type1 = Params['type1'];
var type2 = Params['type2'];

var surrogates = surrogateArray.join(", ");
var toxicities = toxicityArray.join(", ");

var allValues = [];

var slope;
var intercept;

if (fileFamily.substr(0,1) == 'w') {
	specType = 'Wildlife'; units = 'mg/kg bw';	}

if (fileFamily.substr(0,1) == 'a') {
	specType = 'Aquatic'; units = String.fromCharCode(956) +'g/L';	}

function loadDataAlltypes(index) {
  return function() {
  loadData(xmlDocArray[index],toxicityArray[index],index,Params);
  }
}

function snToDecText(number)
{
	var returnVal = "";
	textVal = number.toLowerCase()+"";
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
	if (textVal.indexOf("e")>0||textVal.indexOf("E")>0)
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
	var linkname = "iceSSDSpecies.html?filename=ws";
	if (specType == 'Aquatic') {
		linkname = "iceSSDSpecies.html?filename=as"
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

function file2fetch (prefix,surr) 
{
	//  Changed dir by J. Flaishans
	return 'http://s3.amazonaws.com/webice/data/'+prefix+'Surr'+surr+'.xml?rand='+Math.random();
}

function begin()
{
    popHeader();

    document.getElementById('speciesIn').appendChild(document.createTextNode(" "+surrogates));
    document.getElementById('toxValIn').appendChild(document.createTextNode(" "+toxicities+" "+units));

    if (specType == 'Aquatic') {
	var hcs = document.getElementById('Percent');
	hcs.options[0].text='HC1';
	hcs.options[1].text='HC5';
	hcs.options[2].text='HC10';
    } 
 
   for (usv=0;usv<varNames.length;usv++)
	if (document.getElementById(varNames[usv]))
		document.getElementById(varNames[usv]).value=Params[varNames[usv]];
 
   for (a=0;a<surrogateArray.length;a++)
   {
	var file=file2fetch(prefixArray[a],surrogateArray[a]);
	importFile(xmlDocArray[a],file,'all',toxicityArray[a],a);
	}
}

		
function importFile(xmlDoc,fileName,type,tox,index) 
{	 
	if (document.implementation && document.implementation.createDocument)
	{ 
		var xmlhttp = new window.XMLHttpRequest();
		xmlhttp.open("GET",fileName,false);
		xmlhttp.send(null);
		xmlDoc = xmlhttp.responseXML.documentElement;
		xmlDocArray[index]=xmlDoc;
		loadData(xmlDocArray[index],toxicityArray[index],index,Params);

//		xmlDoc.load(fileName);
//		xmlDoc.onload = loadDataAlltypes(index);
	}
	else if (window.ActiveXObject) 
	{
		xmlDoc.load(fileName);
		//xmlDoc.async = false;
		xmlDocArray[index]=xmlDoc;
		loadData(xmlDocArray[index],toxicityArray[index],index,Params);
 	}
}

function log10(val)
{
	return Math.log(val)/Math.LN10;
}

function valueByLeafTag (pnode,leafname) 
{
  	if (pnode.getElementsByTagName(leafname)[0].childNodes[0])
  		return pnode.getElementsByTagName(leafname)[0].childNodes[0].nodeValue;
  	else 
		return ''; 
}

function loadData(xmlDoc,txcity,index,Params)
{
	var useRow = 1;

	type="all";
	for (i=0;i<(xmlDoc.getElementsByTagName("cross").length>500?500:xmlDoc.getElementsByTagName("cross").length);i++) 
	{
	  var surrogateName = surrogateArray[index];
	  var row = xmlDoc.getElementsByTagName("cross")[i];
	  var predicted = valueByLeafTag(row,'predicted');
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
	 //      if (type !=xrowType && type !='all') continue;
	  var predTox = runCalculation(txcity,slope,intercept);
	  var diff = t95CI * Math.sqrt( MSE * (1/(df+2) + Math.pow(log10(txcity) - xAvg, 2)/Sxx));
	  var lower = showSigDig(Math.pow(10,(log10(predTox) - diff)));
	  var upper = showSigDig(Math.pow(10,(log10(predTox) + diff)));
	  var msg = '';
	  if (txcity > xMax) {
	      msg = '* Input toxicity greater than model maximum of '+showSigDig(xMax);
	    } else if (txcity < xMin) {
		    msg = '* Input toxicity less than model minimum of '+showSigDig(xMin);
           } else { void(0); }    
		//showSSDRow(predicted, showSigDig(predTox), msg, lower, upper,txcity,type);

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
		checkSSDRow(predicted, predTox,Math.pow(10,(log10(predTox) - diff)),Math.pow(10,(log10(predTox) + diff)), showSigDig(predTox), lower, upper, txcity, type, surrogateName, parseInt(df), showSigDig(r2,2), showSigDig(pVal,4), showSigDig(MSE,2), showSigDig(Bootstrap,6), parseInt(taxDist), showSigDig(slope,2), showSigDig(intercept,2), msg);

	 useRow = 1;
	}
}

function runCalculation(input, slope, intercept)
{

	var sigDig = 0;
    var result = 0;
	
	if (input != '')
		result = Math.pow(10,intercept+slope*log10(input));

	return result;
}


function findRow(idVal)
{
	var inputFields;
	var checkBoxes = [];
	
	inputFields = document.getElementsByTagName('input');
	for (p=0; p < inputFields.length; p++) 
		if (inputFields[p].type == 'checkbox' || inputFields[p].type == 'radio') temp = checkBoxes.push(inputFields[p]);
	for (q=0; q < checkBoxes.length; q++)
		if (checkBoxes[q].id == idVal) return q;

	return null;
}

function createRow(species, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg, checkBox)
{
	var nowTime = new Date();
	nowTime = nowTime.getTime();
	if (species.indexOf('(')>1)
		var idVal = species.substring(species.indexOf('(')+1,species.indexOf(')'));
	else
		var idVal = species.substring(species);
	

	if (!msg)
		msg='';

	newRow = document.createElement('tr');

	chkBoxCell = document.createElement('td');
	radioCell = document.createElement('td');
	if (checkBox) 
		try { 
			selectOption = document.createElement('<input type="checkBox" checked="1" id="'+idVal+'" value="'+fullTox+','+fullLower+','+fullUpper+','+toxValue+','+lowerValue+','+upperValue+','+surrTox +','+type+','+surrogateName+','+df+','+r2+','+pVal+','+MSE+','+Bootstrap+','+taxDist+','+slope+','+intercept+'" defaultChecked="true"/>');
			selectOption.onclick = checkBoxClick;
			chkBoxCell.appendChild(selectOption);}			
		catch(err){
			selectOption = document.createElement('input');
			selectOption .setAttribute('value',fullTox+','+fullLower+','+fullUpper+','+toxValue+','+lowerValue+','+upperValue+','+surrTox +','+type+','+surrogateName+','+df+','+r2+','+pVal+','+MSE+','+Bootstrap+','+taxDist+','+slope+','+intercept);
			selectOption.setAttribute('type','checkbox');
			selectOption.defaultChecked = true;
			selectOption.setAttribute('id',idVal);
			selectOption.onclick = checkBoxClick;
			chkBoxCell.appendChild(selectOption);}
	else
		try { 
			selectOption = document.createElement('<input type="radio" name="'+idVal+'" id="'+idVal+'!'+nowTime+Math.random()+'" value="'+fullTox+','+fullLower+','+fullUpper+','+toxValue+','+lowerValue+','+upperValue+','+surrTox +','+type+','+surrogateName+','+df+','+r2+','+pVal+','+MSE+','+Bootstrap+','+taxDist+','+slope+','+intercept+'" />');
			selectOption.onclick = radioClick;
			radioCell.appendChild(selectOption);}			
		catch(err){
			selectOption = document.createElement('input');
			selectOption .setAttribute('value',fullTox+','+fullLower+','+fullUpper+','+toxValue+','+lowerValue+','+upperValue+','+surrTox +','+type+','+surrogateName+','+df+','+r2+','+pVal+','+MSE+','+Bootstrap+','+taxDist+','+slope+','+intercept);
			selectOption.setAttribute('type','radio');
			selectOption.setAttribute('id',idVal+"!"+nowTime+Math.random());
			selectOption.setAttribute('name',idVal);
			selectOption.onclick = radioClick;
			radioCell.appendChild(selectOption); }
	spec1Cell = document.createElement('td');
	spec1Cell.appendChild(document.createTextNode(species.substr(0,species.indexOf('(')-1)));
	spec2Cell = document.createElement('td');
	if (species.indexOf('(')>1)
		spec2Cell.appendChild(document.createTextNode(species.substring(species.indexOf('(')+1,species.indexOf(')'))));
	else
		spec2Cell.appendChild(document.createTextNode(species.substring(species)));
	toxCell = document.createElement('td');
	toxCell.setAttribute('align','center');
	if (msg != '')
		toxCell.className = 'outsideRange';
	toxCell.appendChild(document.createTextNode(toxValue));
	lowerCell = document.createElement('td');
	lowerCell.setAttribute('align','center');
	lowerCell.appendChild(document.createTextNode(lowerValue+' - '+upperValue));
	surrCell = document.createElement('td');
	surrCell.setAttribute('align','center');
	surrCell.appendChild(document.createTextNode(surrogateName));
	dfCell = document.createElement('td');
	dfCell.setAttribute('align','center');
	dfCell.appendChild(document.createTextNode(df));
	r2Cell = document.createElement('td');
	r2Cell.setAttribute('align','center');
	r2Cell.appendChild(document.createTextNode(r2));
	pValCell = document.createElement('td');
	pValCell.setAttribute('align','center');
	pValCell.appendChild(document.createTextNode(pVal));
	MSECell = document.createElement('td');
	MSECell.setAttribute('align','center');
	MSECell.appendChild(document.createTextNode(MSE));
	BootCell = document.createElement('td');
	BootCell.setAttribute('align','center');
	BootCell.appendChild(document.createTextNode(Bootstrap));
	TDCell = document.createElement('td');
	TDCell.setAttribute('align','center');
	TDCell.appendChild(document.createTextNode(taxDist));
	slopeCell = document.createElement('td');
	slopeCell.setAttribute('align','center');
	slopeCell.appendChild(document.createTextNode(slope));
	IntCell = document.createElement('td');
	IntCell.setAttribute('align','center');
	IntCell.appendChild(document.createTextNode(intercept));
	msgCell = document.createElement('td');
	msgCell.appendChild(document.createTextNode(msg));
	msgCell.className = 'outsideRange';
	newRow.appendChild(chkBoxCell);
	newRow.appendChild(radioCell);
	newRow.appendChild(spec1Cell);
	newRow.appendChild(spec2Cell);
	newRow.appendChild(toxCell);
	newRow.appendChild(lowerCell);
	newRow.appendChild(surrCell);
	newRow.appendChild(dfCell);
	newRow.appendChild(r2Cell);
	newRow.appendChild(pValCell);
	newRow.appendChild(MSECell);
	newRow.appendChild(BootCell);
	newRow.appendChild(TDCell);
	newRow.appendChild(slopeCell);
	newRow.appendChild(IntCell);
	newRow.appendChild(msgCell);

	return newRow;
}

function addNewSubRow (species, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg)
{
	rowObject = createRow(species, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg, 0);
	if (species.indexOf('(')+1)
		parentID = species.substring(species.indexOf('(')+1,species.indexOf(')'))+"!";
	else
		parentID = species+"!";
	
	document.getElementById("ssdResults").tBodies[0].insertBefore(rowObject,document.getElementById("ssdResults").rows[findRow(parentID)+2]);
}

function newDuplicate (species)
{
	var nowTime = new Date();
	nowTime = nowTime.getTime();

	if (species.indexOf('(')+1)
		boxID = species.substring(species.indexOf('(')+1,species.indexOf(')'));
	else
		boxID = species;

	rowNum = findRow(boxID);
	rowVal = document.getElementById(boxID).value;

//	try { radioObj = document.createElement('<input type="radio" name="'+boxID+'" value="'+rowVal+'" />');}
//	catch(err){  
	radioObj = document.createElement('input');
	radioObj.setAttribute('type','radio');
	radioObj.setAttribute('value',rowVal);
	radioObj.setAttribute('id',boxID+"!"+nowTime+Math.random());
	radioObj.setAttribute('name',boxID);
	radioObj.onclick = radioClick;
	document.getElementById(boxID).parentNode.nextSibling.appendChild(radioObj);
	document.getElementById(boxID).parentNode.removeChild(document.getElementById(boxID));

	newRow = document.createElement('tr');

	chkBoxCell = document.createElement('td');
	radioCell = document.createElement('td');
	selectOption = document.createElement('input');
	selectOption.onclick = checkBoxClick;
	selectOption.setAttribute('value',rowVal);
	selectOption.setAttribute('type','checkbox');
	selectOption.defaultChecked = true;
	selectOption.setAttribute('id',boxID+'!');
	chkBoxCell.appendChild(selectOption);
	spec1Cell = document.createElement('td');
	if (species.indexOf('(')+1)
		spec1Cell.appendChild(document.createTextNode(species.substr(0,species.indexOf('(')-1)));
	spec2Cell = document.createElement('td');
	if (species.indexOf('(')+1)
		spec2Cell.appendChild(document.createTextNode(species.substring(species.indexOf('(')+1,species.indexOf(')'))));
	else
		spec2Cell.appendChild(document.createTextNode(species));
	newRow.appendChild(chkBoxCell);
	newRow.appendChild(radioCell);
	newRow.appendChild(spec1Cell);
	newRow.appendChild(spec2Cell);
	
	document.getElementById("ssdResults").tBodies[0].insertBefore(newRow,document.getElementById("ssdResults").rows[rowNum+1]);	
}

function checkSSDRow (species, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg)
{
	if (surrogates.indexOf(species)>=0) return 0;
	if (species.indexOf('(')+1)
		idVal = species.substring(species.indexOf('(')+1,species.indexOf(')'));
	else
		idVal = species;
	if (document.getElementById(idVal))
	{
		valuesToCompare=document.getElementById(idVal).value.split(',');
		newDuplicate(species);
		addNewSubRow (species, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg);
		pickNewSub(idVal+"!");
	}
	else if (document.getElementById(idVal+"!"))
	{
		addNewSubRow (species, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg);
		pickNewSub(idVal+"!");
	}
	else
		showSSDRow (species, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg, 0);
}


function showSSDRow (species, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg, dup)
{
	var rowObject;

	if (dup==1)
		rowObject = createRow(species, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg, 0);
	else
		rowObject = createRow(species, fullTox, fullLower, fullUpper, toxValue, lowerValue, upperValue, surrTox, type, surrogateName, df, r2, pVal, MSE, Bootstrap, taxDist, slope, intercept, msg, 1);
	document.getElementById("ssdResults").tBodies[0].appendChild(rowObject);
	if (dup==1) makeGrey(idVal); 
	// Added by J. Flaishans
	// console.log('Called');
	// setTimeout(scrollBarInit(), 10000);
}

function showSSDData(dataPoint)
{
	var rowCount = document.getElementById('ssdResults').getElementsByTagName('tr').length;
	var startCell = 5;
	var cellsPerRow = 7;
	for (q=0;q<rowCount-1;q++) 
	{
		cellNumber = cellsPerRow*q+startCell;
		document.getElementById('ssdResults').getElementsByTagName('td')[cellNumber].removeChild(document.getElementById('ssdResults').getElementsByTagName('td')[cellNumber].firstChild);
		var newDataValue = document.createTextNode(document.getElementById('ssdResults').getElementsByTagName('tr')[q+1].getElementsByTagName('input')[0].value.split(',')[dataPoint]);
		document.getElementById('ssdResults').getElementsByTagName('td')[cellNumber].appendChild(newDataValue);
	}
}

function checkBoxClick()
{
	if (!this.checked) makeGrey(this.id); else makeLive(this.id); reCompute();
}

function radioClick()
{
	if (this.checked) document.getElementById(this.id.substring(0,this.id.indexOf("!")+1)).value = this.value; 
	for (k=0;k<document.ssdResultsForm[this.name].length;k++)
		if (document.ssdResultsForm[this.name][k] != this) turnGrey(document.ssdResultsForm[this.name][k].id);
		else turnLive(document.ssdResultsForm[this.name][k].id);
	reCompute();
}

function pickNewSub(idVal)
{
	inputFields = document.getElementsByTagName('input');
	choices = [];
	for (p=0; p < inputFields.length; p++) 
		if (inputFields[p].type == 'radio' && inputFields[p].id.indexOf(idVal) != -1) temp = choices.push(inputFields[p]);

	idToKeep = choices[0].id;
	for (n=0; n < choices.length; n++) {
		document.getElementById(choices[n].id).checked=false;
		turnGrey(choices[n].id);
		oldValues=document.getElementById(idToKeep).value.split(',');
		newValues=document.getElementById(choices[n].id).value.split(',');
		if(oldValues[2]/oldValues[0] > newValues[2]/newValues[0])
			idToKeep = choices[n].id;
	}
	document.getElementById(idToKeep).checked="true";
	turnLive(idToKeep);
	document.getElementById(idVal).value = document.getElementById(idToKeep).value;
}

function makeGrey(idVal)
{
	if (idVal.indexOf("!") != -1)
	{
		inputFields = document.getElementsByTagName('input');
		checkBoxes = [];
		for (p=0; p < inputFields.length; p++) 
			if (inputFields[p].type == 'checkbox' || inputFields[p].type == 'radio') temp = checkBoxes.push(inputFields[p]);
		for (q=0; q < checkBoxes.length; q++)
			if (checkBoxes[q].id.indexOf(idVal) != -1) turnGrey(checkBoxes[q].id);
	}
	turnGrey(idVal);
}

function turnGrey(idVal)
{
	boxNum = document.getElementById(idVal);
	if (boxNum.type == 'checkbox')
		boxNum.defaultChecked = false;
	tdParent = boxNum.parentNode;
	trParent = tdParent.parentNode;
	trParent.className = 'greyedOut';
}

function makeLive(idVal)
{
	if (idVal.indexOf("!") != -1)
	{
		inputFields = document.getElementsByTagName('input');
		checkBoxes = [];
		for (p=0; p < inputFields.length; p++) 
			if (inputFields[p].type == 'checkbox' || inputFields[p].type == 'radio') temp = checkBoxes.push(inputFields[p]);
		for (q=0; q < checkBoxes.length; q++)
			if (checkBoxes[q].id.indexOf(idVal) != -1 && checkBoxes[q].checked) turnLive(checkBoxes[q].id);
	}
	turnLive(idVal);
}

function turnLive(idVal)
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

var tableID = "ssdResults";

function createExcelSheet(allRows)
{

	if (window.ActiveXObject) 
	{
		try 
		{
			var inputFields;
			var checkBoxes = [];
			var offSet = 0;
		
			inputFields = document.getElementsByTagName('input');
			for (p=0; p < inputFields.length; p++) 
				if (inputFields[p].type == 'checkbox' || inputFields[p].type == 'radio') temp = checkBoxes.push(inputFields[p]);

			var xlApp = new ActiveXObject("Excel.Application"); 
			var xlBook = xlApp.Workbooks.Add();
	
			xlBook.worksheets("Sheet1").activate;
			var XlSheet = xlBook.activeSheet;
			xlApp.visible = true; 

			var rowChecked = 0;

			for (i=0; i < document.getElementById(tableID).rows.length; i++)
			{
				if (document.getElementById(tableID).rows[i].cells[0].childNodes.length && i != 0)
					if (checkBoxes[i-1].checked) rowChecked = 1; else rowChecked = 0;

				if ((allRows || i==0 || (checkBoxes[i-1].checked && rowChecked)) && document.getElementById(tableID).rows[i].cells[4]) {
				for (j=2; j < document.getElementById(tableID).rows[i].cells.length; j++) 
				{
					mycellValue = document.getElementById(tableID).rows[i].cells[j].innerText;
					if (i==0) mycellValue = mycellValue.substring(0,mycellValue.indexOf('Sort')-2); 
					XlSheet.Cells(i+1-offSet,j-1).Value = mycellValue; 
				} }
				else offSet++;
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
	var inputFields;
	var checkBoxes = [];

	inputFields = document.getElementsByTagName('input');
	for (p=0; p < inputFields.length; p++) 
		if (inputFields[p].type == 'checkbox' || inputFields[p].type == 'radio') temp = checkBoxes.push(inputFields[p]);

	//alert('To save the data for Excel from a non-IE browser, save the newly opened window/tab as "text" with an extension of ".xls"');

	var rowChecked = 0;

	for (i=0; i < document.getElementById('ssdResults').rows.length; i++) 
	{
		if (document.getElementById('ssdResults').rows[i].cells[0].childNodes.length && i != 0)
			if (checkBoxes[i-1].checked) rowChecked = 1; else rowChecked = 0;

		if ((allRows || i==0 || (checkBoxes[i-1].checked && rowChecked)) && document.getElementById('ssdResults').rows[i].cells[4])
		{
			newRow = ICETable.document.getElementById('ICEOutput').insertRow(ICETable.document.getElementsByTagName('tr').length);
			for (j=2; j < document.getElementById('ssdResults').rows[i].cells.length; j++) 
			{
				newCell = ICETable.document.createElement('td');
				if (document.getElementById('ssdResults').rows[i].cells[j].childNodes[0]) 
				{
					mycellValue = document.getElementById('ssdResults').rows[i].cells[j].childNodes[0].nodeValue;
					if (i==0 && mycellValue.indexOf('Sort') > 0) mycellValue.substring(0,mycellValue.indexOf('Sort')-2); 
						newCell.appendChild(ICETable.document.createTextNode(mycellValue )); 
				}
				newRow.appendChild(newCell); 
			} 
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