// if (!document.URL.split("?")[1])
// 	location.href="index.html";
var fileFamily = '';
fileFamily = document.URL.split("?")[1];
if (fileFamily)
fileFamily = fileFamily.split("&")[0].split("=")[1];
var chosenSurrogate = '';
var chosenPredicted = '';
var chosenFirst = '';
//var fileName = file.split("=")[1]+".xml";
var speciesArray = [];
var SurrogateArray = [];
var PredictedArray = [];
var groupXmlDoc; 
var dataXmlDoc; 
var surrXmlDoc; 
var predXmlDoc; 
var time1;
var time2;

var selectedSpeciesIndex = 0;
var selectedGroup = 'All';

function sortBySci(a,b)
{
	if (a.indexOf('(') > -1)
		f = a.substr(a.indexOf('('),a.length);
	else
		f = a;
	if (b.indexOf('(') > -1)
		b = b.substr(b.indexOf('('),b.length);
	if (f < b) return -1;
	if (b < f) return 1;
	return 0;
}

function valueByLeafTag (pnode,leafname) 
{
  return pnode.getElementsByTagName(leafname)[0].childNodes[0].nodeValue;
}

function tneInitData()
{
	importGroups();
	importSpecies('All');
	importSurrogate('All');
}

function importGroups() {
	// Changed DIR by J. Flaishans
	file = 'http://s3.amazonaws.com/webice/data/'+fileFamily+'AllGroups.xml';
	if (document.implementation && document.implementation.createDocument)
	{
		var xmlhttp = new window.XMLHttpRequest();
		xmlhttp.open("GET",file,false);
		xmlhttp.send(null);
		groupXmlDoc = xmlhttp.responseXML.documentElement;
		loadGroups(); 
	}
	else if (window.ActiveXObject)
	{
		groupXmlDoc = new ActiveXObject("Microsoft.XMLDOM");
		groupXmlDoc.onreadystatechange = function () {
			if (groupXmlDoc.readyState == 4) loadGroups() };
		groupXmlDoc.load(file); 
 	}
}

function loadGroups()
{
	for (i=0;i<groupXmlDoc.getElementsByTagName("group").length;i++) 
	{
		var groupName = groupXmlDoc.getElementsByTagName("group")[i].childNodes[0].nodeValue;
		addGroup(groupName);
	}
}

function importSpecies(groupName) {
	// Changed DIR by J. Flaishans
	file = 'http://s3.amazonaws.com/webice/data/'+fileFamily+groupName+'Species.xml';
	if (document.implementation && document.implementation.createDocument)
	{
		var xmlhttp1 = new window.XMLHttpRequest();
		xmlhttp1.open("GET",file,false);
		xmlhttp1.send(null);
		dataXmlDoc = xmlhttp1.responseXML.documentElement;
		loadSpecies(); 
	}
	else if (window.ActiveXObject)
	{
		dataXmlDoc = new ActiveXObject("Microsoft.XMLDOM");
		dataXmlDoc.onreadystatechange = function () {
			if (dataXmlDoc.readyState == 4) loadSpecies() };
		dataXmlDoc.load(file); 
 	}
}

function proceed()
{
 alert('Data is in');
}

function loadSpecies()
{ 
	if (document.getElementById('species'))
	{ 
		document.getElementById('species').options.length = 1;
		document.getElementById("species").options[0] =new Option ('Please wait...','0'); 
	
		speciesDup = [];
		speciesArray.length = 0;
		
		if(dataXmlDoc.getElementsByTagName("species")[0].childNodes.length > 1)
			speciesNode = 1;
		else 
			speciesNode = 0;
		
		for (i=0;i<dataXmlDoc.getElementsByTagName("species").length;i++) 
		{
			var spec = dataXmlDoc.getElementsByTagName("species")[i].childNodes[speciesNode].nodeValue;
			
			if(!speciesDup[spec]) 
			{
				speciesArray[speciesArray.length] = spec;
				speciesDup[spec] = 1;
			}
		}

		if (document.getElementById('specSortBy').selectedIndex == 1)
		{
			speciesArray = speciesArray.sort(sortBySci);
			for (i=0;i<speciesArray.length;i++)
			{
				//document.getElementById("species").options[i+1] =new Option (SurrogateArray[i].substring(SurrogateArray[i].indexOf('(')+1,SurrogateArray[i].indexOf(')'))+' ('+SurrogateArray[i].substr(0,SurrogateArray[i].indexOf('(')-1)+')',i); 
				document.getElementById("species").options[i+1] =new Option (speciesArray[i].substring(speciesArray[i].indexOf('(')+1,speciesArray[i].indexOf(')'))+' ('+speciesArray[i].substr(0,speciesArray[i].indexOf('(')-1)+')',speciesArray[i]); 
				//if (chosenSpecies == speciesArray[i])
					//document.getElementById("species").selectedIndex = i+1;
			}
		}
		else
		{
			speciesArray = speciesArray.sort();
			for (i=0;i<speciesArray.length;i++)
			{
				//document.getElementById("species").options[i+1] =new Option (SurrogateArray[i],i); 
				document.getElementById("species").options[i+1] =new Option (speciesArray[i],speciesArray[i]); 
				//if (chosenSurrogate == speciesArray[i])
					//document.getElementById("species").selectedIndex = i+1;
			}
		}
		document.getElementById("species").options[0] =new Option ('','All'); 
		document.getElementById("species").selectedIndex = 0; 
	}
	//cleanList();
}

function importSurrogate(surrName) {
	// Changed DIR by J. Flaishans
	file = 'http://s3.amazonaws.com/webice/data/'+fileFamily+surrName+'Surrogates.xml';
	if (document.implementation && document.implementation.createDocument)
	{
		var xmlhttp2 = new window.XMLHttpRequest();
		xmlhttp2.open("GET",file,false);
		xmlhttp2.send(null);
		surrXmlDoc = xmlhttp2.responseXML.documentElement;
		loadSurr(); 
	}
	else if (window.ActiveXObject)
	{
		surrXmlDoc = new ActiveXObject("Microsoft.XMLDOM");
		surrXmlDoc.onreadystatechange = function () {
			if (surrXmlDoc.readyState == 4) loadSurr() };
		surrXmlDoc.load(file); 
 	}
}

function loadSurr()
{
	if (document.getElementById('Surrogate'))
	{
		SurrDup = [];
		SurrogateArray.length = 0;
		
		if(surrXmlDoc.getElementsByTagName("surrogate")[0].childNodes.length > 1)
			surrogateNode = 1;
		else 
			surrogateNode = 0;
		
		for (i=0;i<surrXmlDoc.getElementsByTagName("surrogate").length;i++) 
		{
			var surr = surrXmlDoc.getElementsByTagName("surrogate")[i].childNodes[surrogateNode].nodeValue;
			
			if(!SurrDup[surr]) 
			{
				SurrogateArray[SurrogateArray.length] = surr;
				SurrDup[surr] = 1;
			}
		}
		
		document.getElementById('Surrogate').options.length = 1;
		if (document.getElementById('sortBy').selectedIndex == 1)
		{
			SurrogateArray = SurrogateArray.sort(sortBySci);
			for (i=0;i<SurrogateArray.length;i++)
			{
				//document.getElementById('Surrogate').options[i+1] =new Option (SurrogateArray[i].substring(SurrogateArray[i].indexOf('(')+1,SurrogateArray[i].indexOf(')'))+' ('+SurrogateArray[i].substr(0,SurrogateArray[i].indexOf('(')-1)+')',i); 
				document.getElementById('Surrogate').options[i+1] =new Option (SurrogateArray[i].substring(SurrogateArray[i].indexOf('(')+1,SurrogateArray[i].indexOf(')'))+' ('+SurrogateArray[i].substr(0,SurrogateArray[i].indexOf('(')-1)+')',SurrogateArray[i]); 
				if (chosenSurrogate == SurrogateArray[i])
					document.getElementById('Surrogate').selectedIndex = i+1;
			}
		}
		else
		{
			SurrogateArray = SurrogateArray.sort();
			for (i=0;i<SurrogateArray.length;i++)
			{
				//document.getElementById('Surrogate').options[i+1] =new Option (SurrogateArray[i],i); 
				document.getElementById('Surrogate').options[i+1] =new Option (SurrogateArray[i],SurrogateArray[i]); 
				if (chosenSurrogate == SurrogateArray[i])
					document.getElementById('Surrogate').selectedIndex = i+1;
			}
		}
	}
	cleanList('Surrogate');
}

function popHeader()
{
	var fType;
	if (fileFamily == 'tneAs') fType = 'Aquatic' ;
	if (fileFamily == 'tneWs')
	{
		fType = 'Wildlife';
		document.getElementById('tneUnits').firstChild.nodeValue='mg/kg';
	}
	document.getElementById('PageName').appendChild(document.createTextNode(' - '+fType+' Species'));
	document.getElementById('file1').value = fileFamily;
	// document.title = fType+' Species | '+document.title;
	// newBClink = document.createElement('a');
	// newBClink.setAttribute('href','iceTNE.html');
	// newBClink.appendChild(document.createTextNode('Endangered Species'));
	// oldBC = document.createElement('li');
	// oldBC.appendChild(newBClink);
	// newBC = document.createElement('li');
	// newBC.appendChild(document.createTextNode(fType+' Species'));
	// if(!document.getElementById('breadcrumbs').lastChild.childNodes.length)
	// 	document.getElementById('breadcrumbs').removeChild(document.getElementById('breadcrumbs').lastChild);
	// document.getElementById('breadcrumbs').removeChild(document.getElementById('breadcrumbs').lastChild);
	// document.getElementById('breadcrumbs').appendChild(oldBC);
	// document.getElementById('breadcrumbs').appendChild(newBC);
}

function speciesReload()
{
	for (k=0;k<document.ESTaxaForm.group.length;k++)
		if (document.ESTaxaForm.group[k].checked)
			getGroupOptions(document.ESTaxaForm.group[k].value);
}

function cleanList(fieldName)
{
	var inputs = document.getElementsByTagName('input');
	for (g=0;g<inputs.length;g++)
		if (inputs[g].name=='S')
//		if (inputs[g].name=='ssdSurrogate')
			for (h=0;h<document.getElementById(fieldName).options.length;h++)
				if(document.getElementById(fieldName).options[h].value==inputs[g].value)
						document.getElementById(fieldName).remove(h);
}

function addSpecies(fieldID)
{
	speciesName = document.getElementById(fieldID).options[document.getElementById(fieldID).selectedIndex].value;
	if (speciesName == '') return;
	document.getElementById('DataTable').style.display = 'block';
	document.getElementById('SubmitTable').style.display = 'block';
	newInput = document.createElement('input');
	newInput.setAttribute('name','T');
//		newInput.setAttribute('name','Toxicity');
	nameInput = document.createElement('input');
	nameInput.setAttribute('name','S');
//		nameInput.setAttribute('name','ssdSurrogate');
	nameInput.setAttribute('type','Hidden');
	nameInput.setAttribute('value',speciesName);
	newRow = document.createElement('tr');
	newCell = document.createElement('td');
	newCell.style.paddingRight = '10px';
	newCell.appendChild(nameInput);
	newCell.appendChild(document.createTextNode(speciesName));
	newRow.appendChild(newCell);
	newCell = document.createElement('td');
	newCell.style.paddingRight = '10px';
	newCell.appendChild(newInput);
	newRow.appendChild(newCell);
	newButton = document.createElement('button');
	newButton.setAttribute('type','Button');
	newButton.onclick = removeSpecies(speciesName);
	newButton.appendChild(document.createTextNode('Remove Species'));
	newCell = document.createElement('td');
	newCell.appendChild(newButton);
	newRow.appendChild(newCell);
	document.getElementById('DataRow').parentNode.appendChild(newRow);
	document.getElementById(fieldID).remove(document.getElementById(fieldID).selectedIndex);
	
	var inputs = document.getElementsByTagName('input');
	var speciesCount = 0;
	for (h=0;h<inputs.length;h++)
		if (inputs[h].name=='S') speciesCount++;
	if (speciesCount >= 25)
	{
		document.getElementById('addButton').style.display = 'none';
		document.getElementById('limitText').style.display = 'inline';
	}
}

function insertSpecies(fieldID,speciesName)
{
	//var insSpec = new Option(speciesName,speciesName);
	//document.getElementById(fieldID).options[i+1] = insSpec;
	//nameReload();
	importSurrogate(document.ESTaxaForm.species.options[document.ESTaxaForm.species.selectedIndex].value)
}

function removeSpecies(speciesName)
{
	return function() 
	{
		selectedRow = this.parentNode.parentNode;
		selectedRow.removeChild(selectedRow.firstChild); 
		selectedRow.removeChild(selectedRow.firstChild); 
		insertSpecies('Surrogate',speciesName);
		if (document.getElementById('DataTable').getElementsByTagName('tr').length == 2)
		{
			document.getElementById('DataTable').style.display = 'none';
			document.getElementById('SubmitTable').style.display = 'none';
		}
		selectedRow.parentNode.removeChild(selectedRow); 
		
		document.getElementById('addButton').style.display = 'inline';
		document.getElementById('limitText').style.display = 'none';
	}
}

function checkTox()
{
	var inputs = document.getElementsByTagName('input');
	for (g=0;g<inputs.length;g++)
		if (inputs[g].name=='T' && inputs[g].value=='')
//		if (inputs[g].name=='Toxicity' && inputs[g].value=='')
		{
			alert('You must enter a toxicity value for each species.');
			return false;
		} 
	return true;
}

function getGroupOptions(groupName)
{	
	if (groupName == '')
		groupName = 'All';
	if (groupName != selectedGroup)
	{
		if (clearChosenSurrogates())
		{
			selectedGroup = groupName;
			importSpecies(groupName);
			importSurrogate(groupName);
		}
	}
	else
	{
		importSpecies(groupName);
		importSurrogate(groupName);
	}
}

function addGroup(groupName)
{
	try
	{  
		groupInput = document.createElement('<input type="radio" name="group" />');  
	}
	catch(err)
	{  
		groupInput = document.createElement('input');
		groupInput.setAttribute('name','group');
		groupInput.setAttribute('type','Radio');
	}
	groupInput.setAttribute('id',groupName);
	groupInput.setAttribute('value',groupName);
	if (groupInput.addEventListener)
		groupInput.addEventListener('click',function () { getGroupOptions(groupName); },false);
	else
		groupInput.attachEvent('onclick',function () { getGroupOptions(groupName); });
	groupText = document.createTextNode(' '+groupName+' ');
	document.getElementById("groupCell").appendChild(groupInput);
	document.getElementById("groupCell").appendChild(groupText);
}

function clearChosenSurrogates()
{
	var surrogatesChosen = false;
	var inputs = document.getElementsByTagName('input');
	for (k=0;k<inputs.length;k++)
		if (inputs[k].name=='S')
			surrogatesChosen = true;
	if (surrogatesChosen)
	{
		var ok2remove = confirm('Chosing a new Taxa will remove all chosen surrogates.\n\nClick OK to continue or Cancel to return to the previously chosen Taxa.');
		if (ok2remove)
		{
			for (k=inputs.length-1;k>=0;k--)
				if (inputs[k].name=='S')
				{
					selectedRow = inputs[k].parentNode.parentNode;
					selectedRow.removeChild(selectedRow.firstChild); 
					selectedRow.removeChild(selectedRow.firstChild); 
					selectedRow.parentNode.removeChild(selectedRow); 
				}
			document.getElementById('DataTable').style.display = 'none';
			document.getElementById('SubmitTable').style.display = 'none';	
			document.getElementById('addButton').style.display = 'inline';
			document.getElementById('limitText').style.display = 'none';
			return 1;	
		}
		else
		{
			document.getElementById('species').selectedIndex = selectedSpeciesIndex;
			for (p=0;p<document.ESTaxaForm.group.length;p++)
				if (document.ESTaxaForm.group[p].value == selectedGroup)
					document.ESTaxaForm.group[p].checked = true;
				else
					document.ESTaxaForm.group[p].checked = false;
			return 0;
		}
	}
	else
		return 1;
}

function changeSpecies(speciesName,speciesIndex)
{
	if (speciesIndex != selectedSpeciesIndex)
		if (clearChosenSurrogates())
		{
			selectedSpeciesIndex = speciesIndex;
			importSurrogate(speciesName);
		}
}
