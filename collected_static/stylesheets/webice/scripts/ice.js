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
		a = a.substr(a.indexOf('('),a.length);
	if (b.indexOf('(') > -1)
		b = b.substr(b.indexOf('('),b.length);
	if (a < b) return -1;
	if (b < a) return 1;
	return 0;
}

function importSurrogate(surrName) {
	// Changed DIR by J. Flaishans
	file = 'http://s3.amazonaws.com/webice/data/'+fileFamily+surrName+'.xml';
	if (document.implementation && document.implementation.createDocument)
	{
		var xmlhttp = new window.XMLHttpRequest();
		xmlhttp.open("GET",file,false);
		xmlhttp.send(null);
		surrXmlDoc = xmlhttp.responseXML.documentElement;
		loadSurr();

//		surrXmlDoc=document.implementation.createDocument("", "doc", null) 
//		surrXmlDoc.load(file); 
//		surrXmlDoc.onload = loadSurr; 
	}
	else if (window.ActiveXObject)
	{
		surrXmlDoc = new ActiveXObject("Microsoft.XMLDOM");
		surrXmlDoc.onreadystatechange = function () {
			if (surrXmlDoc.readyState == 4) loadSurr() };
		surrXmlDoc.load(file); 
 	}



}

function importPredicted(predName) {
	// Changed DIR to webice subdir
	file = 'http://s3.amazonaws.com/webice/data/'+fileFamily+predName+'.xml';
	if (document.implementation && document.implementation.createDocument)
	{
		var xmlhttp = new window.XMLHttpRequest();
		xmlhttp.open("GET",file,false);
		xmlhttp.send(null);
		predXmlDoc = xmlhttp.responseXML.documentElement;
		loadPred();

//		predXmlDoc=document.implementation.createDocument("", "doc", null) 
//		predXmlDoc.load(file); 
//		predXmlDoc.onload = loadPred; 
	}
	else if (window.ActiveXObject)
	{
		predXmlDoc = new ActiveXObject("Microsoft.XMLDOM");
		predXmlDoc.onreadystatechange = function () {
			if (predXmlDoc.readyState == 4) loadPred() };
		predXmlDoc.load(file); 
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
				document.getElementById('Surrogate').options[i+1] =new Option (SurrogateArray[i],SurrogateArray[i]); 
				if (chosenSurrogate == SurrogateArray[i])
					document.getElementById('Surrogate').selectedIndex = i+1;
			}
		}
	}
}

function loadPred()
{
	if (document.getElementById('Predicted'))
	{
		PredDup = [];
		PredictedArray.length = 0;
		
		if(predXmlDoc.getElementsByTagName("predicted")[0].childNodes.length > 1)
			predictedNode = 1;
		else 
			predictedNode = 0;
		
		for (i=0;i<predXmlDoc.getElementsByTagName("predicted").length;i++) 
		{
			var pred = predXmlDoc.getElementsByTagName("predicted")[i].childNodes[predictedNode].nodeValue;
			
			if(!PredDup[pred]) 
			{
				PredictedArray[PredictedArray.length] = pred;
				PredDup[pred] = 1;
			}
		}
		document.getElementById('Predicted').options.length = 1;
		if (document.getElementById('sortBy').selectedIndex == 1)
		{
			PredictedArray = PredictedArray.sort(sortBySci);
			for (i=0;i<PredictedArray.length;i++)
			{
				document.getElementById('Predicted').options[i+1] =new Option (PredictedArray[i].indexOf('(')<0?PredictedArray[i]:PredictedArray[i].substring(PredictedArray[i].indexOf('(')+1,PredictedArray[i].indexOf(')'))+' ('+PredictedArray[i].substr(0,PredictedArray[i].indexOf('(')-1)+')',PredictedArray[i]); 
				if (chosenPredicted == PredictedArray[i])
					document.getElementById('Predicted').selectedIndex = i+1;
			}
		}
		else
		{
			PredictedArray = PredictedArray.sort();
			for (i=0;i<PredictedArray.length;i++)
			{
				document.getElementById('Predicted').options[i+1] =new Option (PredictedArray[i],PredictedArray[i]); 
				if (chosenPredicted == PredictedArray[i])
					document.getElementById('Predicted').selectedIndex = i+1;
			}
		}
	}
}

function loadSurrogate()
{
	if (chosenSurrogate != '' && chosenFirst == 'Surrogate')
		chosenPredicted = '';
	if (chosenFirst == '') chosenFirst = 'Surrogate';
	chosenSurrogate = document.getElementById('Surrogate').options[document.getElementById('Surrogate').selectedIndex].value;
	if (chosenFirst == 'Surrogate')
	{
		if (document.getElementById('Predicted').selectedIndex == 0) document.getElementById('Predicted').options.length=1;
		importPredicted("Surr"+chosenSurrogate);
	} 
}

function loadPredicted()
{
	if (chosenPredicted != '' && chosenFirst == 'Predicted')
		chosenSurrogate = '';
	if (chosenFirst == '') chosenFirst = 'Predicted';
	chosenPredicted = document.getElementById('Predicted').options[document.getElementById('Predicted').selectedIndex].value;
	if (chosenFirst == 'Predicted')
	{
		if (document.getElementById('Surrogate').selectedIndex==0)document.getElementById('Surrogate').options.length=1;
		importSurrogate("Pred"+chosenPredicted);
	} 
}

function popHeader()
{
	var fType;
	pic = document.createElement('img');
	// pic.setAttribute('src','/images/webice/'+ fileFamily +'.jpg');
	pic.setAttribute('src','/static/images/webice/'+ fileFamily +'.jpg');
	if (fileFamily == 'as') { 
		fType = 'Aquatic Species'; 
		pic.setAttribute('alt','Photo of a Blue crab.');}
	if (fileFamily == 'ag') { 
		fType = 'Aquatic Genus'; 
		pic.setAttribute('alt','Photo of a toad.'); }
	if (fileFamily == 'af') { 
		fType = 'Aquatic Family'; 
		pic.setAttribute('alt','Photo of a shrimp.');}//123
	if (fileFamily == 'ws') { 
		fType = 'Wildlife Species'; 
		pic.setAttribute('alt','Photo of a duck.');}
	if (fileFamily == 'wf') { 
		fType = 'Wildlife Family'; 
		pic.setAttribute('alt','Photo of an owl.');}
	if (fileFamily == 'ls') { 
		fType = 'Algae Species'; 
		document.getElementById('sortRow').style.display='none';
		pic.setAttribute('alt','Photo of an alga.');}
	if (fileFamily == 'lg') { 
		fType = 'Algae Genus'; 
		document.getElementById('sortRow').style.display='none';
		pic.setAttribute('alt','Photo of an alga.'); }
	pic.setAttribute('width','350');
	document.getElementById('PageName').appendChild(document.createTextNode(fType+' - Taxa Selection Page'));
	document.getElementById('fileType').appendChild(pic);
	// document.title = fType+' Taxa Selection | '+ document.title;
	// newBC = document.createElement('li');
	// newBC.appendChild(document.createTextNode(fType+' Taxa Selection'));
	// document.getElementById('breadcrumbs').appendChild(newBC);

}

function listReload()
{
	chosenPredicted = '';
	chosenSurrogate = '';
	chosenFirst = '';
	if (document.getElementById('Surrogate'))
	importSurrogate('Surrogate');
	if (document.getElementById('Predicted'))
	importPredicted('Predicted');
}

function nameReload()
{
	if (chosenFirst != '')
	{
		loadPred();loadSurr();
	}
	else
	{
		importSurrogate('Surrogate');
		importPredicted('Predicted');
	}
}
