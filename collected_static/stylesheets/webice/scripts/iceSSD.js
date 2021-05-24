// if (!document.URL.split("?")[1])
// 	location.href="index.html";
var fileFamily = '';
fileFamily = document.URL.split("?")[1];
if (fileFamily)
fileFamily = fileFamily.split("=")[1];
var chosenSurrogate = '';
var chosenPredicted = '';
var chosenFirst = '';
//var fileName = file.split("=")[1]+".xml";
var SurrogateArray = [];
var PredictedArray = [];
var surrXmlDoc; 
var predXmlDoc; 
var time1;
var time2;

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

function importSurrogate(prefix) {
	// Changed DIR by J. Flaishans
	file = 'http://s3.amazonaws.com/webice/data/'+prefix+'Surrogate.xml';
	if (document.implementation && document.implementation.createDocument)
	{
		var xmlhttp = new window.XMLHttpRequest();
		xmlhttp.open("GET",file,false);
		xmlhttp.send(null);
		surrXmlDoc = xmlhttp.responseXML.documentElement;
		loadSurr(prefix); 
	}
	else if (window.ActiveXObject)
	{
		surrXmlDoc = new ActiveXObject("Microsoft.XMLDOM");
		surrXmlDoc.onreadystatechange = function () {
			if (surrXmlDoc.readyState == 4) loadSurr(prefix) };
		surrXmlDoc.load(file); 
 	}
}

function loadSurr(prefix)
{
	if (prefix == 'as') fieldName = 'Surrogate';
	if (prefix == 'ws') fieldName = 'Surrogate';
	if (prefix == 'ls') fieldName = 'Algae';
	if (document.getElementById(fieldName))
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
		
		document.getElementById(fieldName).options.length = 1;

		if (prefix == 'as') {
			if (document.getElementById('sortBy').selectedIndex == 1)
			{
				SurrogateArray = SurrogateArray.sort(sortBySci);
				for (i=0;i<SurrogateArray.length;i++)
				{
					//document.getElementById('Surrogate').options[i+1] =new Option (SurrogateArray[i].substring(SurrogateArray[i].indexOf('(')+1,SurrogateArray[i].indexOf(')'))+' ('+SurrogateArray[i].substr(0,SurrogateArray[i].indexOf('(')-1)+')',i); 
					document.getElementById(fieldName).options[i+1] =new Option (SurrogateArray[i].substring(SurrogateArray[i].indexOf('(')+1,SurrogateArray[i].indexOf(')'))+' ('+SurrogateArray[i].substr(0,SurrogateArray[i].indexOf('(')-1)+')',SurrogateArray[i]); 
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
					document.getElementById(fieldName).options[i+1] =new Option (SurrogateArray[i],SurrogateArray[i]); 
					if (chosenSurrogate == SurrogateArray[i])
						document.getElementById('Surrogate').selectedIndex = i+1;
				}
			}
		}
		else {
			SurrogateArray = SurrogateArray.sort();
			for (j=0;j<SurrogateArray.length;j++)
			{
				//document.getElementById('Surrogate').options[j+1] =new Option (SurrogateArray[j],j); 
				document.getElementById(fieldName).options[j+1] =new Option (SurrogateArray[j],SurrogateArray[j]); 
				if (chosenSurrogate == SurrogateArray[j])
					document.getElementById('Surrogate').selectedIndex = j+1;
			}
		}
	}
	cleanList();
}

function popHeader()
{
	var fType;
	if (fileFamily == 'as') 
	{
		fType = 'Aquatic';
		document.getElementById('primaryType').appendChild(document.createTextNode('Vertebrates & Invertebrates:'));
	}
	if (fileFamily == 'ws')
	{
		fType = 'Wildlife';
		document.getElementById('tneUnits').firstChild.nodeValue='mg/kg';
		document.getElementById('AlgaeHeaderRow').style.display='none';
		document.getElementById('AlgaeFormRow').style.display='none';
		document.getElementById('primaryType').appendChild(document.createTextNode('Vertebrates:'));
	}
	document.getElementById('PageName').appendChild(document.createTextNode(' - '+fType+' Species'));
	document.getElementById('file1').value = fileFamily;
	// document.title = fType+' Species | '+document.title;
	// newBClink = document.createElement('a');
	// newBClink.setAttribute('href','iceSSD.html');
	// newBClink.appendChild(document.createTextNode('Species Sensistivity Distributions'));
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

function nameReload()
{
	importSurrogate(fileFamily);
	if (fileFamily == 'as') setTimeout("importSurrogate('ls')",300);
}

function cleanList()
{
	var inputs = document.getElementsByTagName('input');
	for (g=0;g<inputs.length;g++)
		if (inputs[g].name=='S')
		{
			for (h=0;h<document.getElementById('Surrogate').options.length;h++)
				if(document.getElementById('Surrogate').options[h].value==inputs[g].value)
					document.getElementById('Surrogate').remove(h);
			if (document.getElementById('Algae'))
				for (k=0;k<document.getElementById('Algae').options.length;k++)
					if(document.getElementById('Algae').options[k].value==inputs[g].value)
						document.getElementById('Algae').remove(k);
		}
}

	function addSpecies(fieldID)
	{
		speciesName = document.getElementById(fieldID).options[document.getElementById(fieldID).selectedIndex].value;
		if (speciesName == '') return;
		document.getElementById('DataTable').style.display = 'block';
		document.getElementById('SubmitTable').style.display = 'block';
		newInput = document.createElement('input');
		newInput.setAttribute('name','T'); //Toxicity
		nameInput = document.createElement('input');
		nameInput.setAttribute('name','S'); //Surrogate
		nameInput.setAttribute('type','Hidden');
		nameInput.setAttribute('value',speciesName);
		familyInput = document.createElement('input');
		familyInput.setAttribute('name','F'); //Family
		familyInput.setAttribute('type','Hidden');
		if (fieldID == 'Surrogate')
			familyInput.setAttribute('value',fileFamily);
		if (fieldID == 'Algae')
			familyInput.setAttribute('value','ls');
		newRow = document.createElement('tr');
		newCell = document.createElement('td');
		newCell.appendChild(nameInput);
		newCell.appendChild(familyInput);
		newCell.appendChild(document.createTextNode(speciesName));
		newRow.appendChild(newCell);
		newCell = document.createElement('td');
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
		nameReload();
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

function initPage()
{
	// openContent();
	importSurrogate(fileFamily);
	if (fileFamily == 'as') setTimeout("importSurrogate('ls')",300);
	popHeader();
}