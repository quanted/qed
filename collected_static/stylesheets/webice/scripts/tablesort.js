
var HidColumns = [];

function hideCol(obj)
{
obj.className='hidden';
}

function setClicks(tableID)
{
var tbl=document.getElementById(tableID);
var selList = document.getElementById('ColNames');
var str="Show Column: ";
initCol = 0;
if (tableID == 'ssdResults') initCol = 2;
for(var i=initCol;i<tbl.rows[0].cells.length;i++)
{
//tbl.rows[0].cells[i].innerHTML="Col "+(i+1)
//	newOption = new Option (tbl.rows[0].cells[i].innerHTML.replace(/&nbsp;/g, ''),i);
//	selList.options[i+1] = newOption; 
//	var hideDiv = document.createElement('div');
//	hideDiv.className = "Hide";
//	var newLink = document.createElement('a');
//	newLink.setAttribute("href","javascript: void(0);");
//	newLink.onclick = new Function("hideCol("+i+",'none')");
	//newLink.setAttribute("onclick","hideCol("+i+",'none');");
//	newLink.appendChild(document.createTextNode("Hide"));
//	hideDiv.appendChild(newLink);
	var sortDiv = document.createElement('div');
	sortDiv.className = "Sort";
	newLink = document.createElement('a');
	newLink.setAttribute("href","javascript: void(0);");
	newLink.setAttribute("id","sortCol"+i);
	newLink.onclick = new Function("ts_resortTable(this);return false;");
	//newLink.setAttribute("onclick","ts_resortTable(this);return false;");
	newLink.appendChild(document.createTextNode("Sort"));
	var sortSpan = document.createElement('span');
	sortSpan.className = "sortarrow";
	newLink.appendChild(sortSpan);
	sortDiv.appendChild(newLink);
//	tbl.rows[0].cells[i].appendChild(hideDiv);
	tbl.rows[0].cells[i].appendChild(sortDiv);
	//tbl.rows[0].cells[i].innerHTML=tbl.rows[0].cells[i].innerHTML+'<div class="Hide"><a href="javascript: void(0);" onclick="hideCol('+i+',\'none\')">Hide</a></div>'+'<div class="Sort"><a href="javascript: void(0);" onclick="ts_resortTable(this);return false;">Sort<span class="sortarrow"></span></a></div>';
	//if (i>0) str+='<a href="#" onclick="hideCol('+i+',\'\');">'+tbl.rows[0].cells[i].innerHTML+'</a>&nbsp;';
}
//for(var i=0;i<tbl.rows[1].cells.length;i++)
//{
//	if (tbl.rows[1].cells[i].innerHTML=="Hide")
//		tbl.rows[1].cells[i].onclick=new Function("hideCol("+i+",'none')");
//}
//document.getElementById('hidcols').innerHTML=str;
}

function hideCol(num,stat)
{
var tbl=document.getElementById('tbl');
if (stat=="none")
	HidColumns;
for(var i=0;i<tbl.rows.length;i++)
{
tbl.rows[i].cells[num].style.display=stat;
}
}

function hideAll()
{
	var tbl=document.getElementById('tbl');
	for(var i=0;i<tbl.rows[0].cells.length;i++)
		hideCol(i,'none');
}

addEvent(window, "load", sortables_init);

var SORT_COLUMN_INDEX;

function sortables_init() {
    // Find all tables with class sortable and make them sortable
    if (!document.getElementsByTagName) return;
    tbls = document.getElementsByTagName("table");
    for (ti=0;ti<tbls.length;ti++) {
        thisTbl = tbls[ti];
        if (((' '+thisTbl.className+' ').indexOf("sortable") != -1) && (thisTbl.id)) {
            //initTable(thisTbl.id);
            ts_makeSortable(thisTbl);
        }
    }
}

function ts_makeSortable(table) {
    if (table.rows && table.rows.length > 0) {
        var firstRow = table.rows[0];
    }
    if (!firstRow) return;
    
    // We have a first row: assume it's the header, and make its contents clickable links
    for (var i=0;i<firstRow.cells.length;i++) {
        var cell = firstRow.cells[i];
        //var txt = ts_getInnerText(cell);
        //cell.innerHTML = '<a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">'+txt+'<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a>';
    }
}

function ts_getInnerText(el) {
	if (typeof el == "string") return el;
    if (typeof el == "undefined") {
        return ""
    }
    if (el.innerText) return el.innerText;	//Not needed but it is faster
	var str = "";
	
	var cs = el.childNodes;
	var l = cs.length;
	for (var i = 0; i < l; i++) {
		switch (cs[i].nodeType) {
			case 1: //ELEMENT_NODE
				str += ts_getInnerText(cs[i]);
				break;
			case 3:	//TEXT_NODE
				str += cs[i].nodeValue;
				break;
		}
	}
	return str;
}

function ts_resortTable(lnk) {
    // get the span
    var span;
    for (var ci=0;ci<lnk.childNodes.length;ci++) {
        if (lnk.childNodes[ci].tagName && lnk.childNodes[ci].tagName.toLowerCase() == 'span') span = lnk.childNodes[ci];
    }
    var spantext = ts_getInnerText(span);
    var td = lnk.parentNode.parentNode; 
	if (td.getAttribute("id")=="Col"+td.cellIndex)
    	var column = td.cellIndex;
	else
		var column = td.getAttribute("id").substr(3,2);
    var table = getParent(td,'TABLE');
	//alert(column); 
    
    // Work out a type for the column
    if (table.rows.length <= 1) return;
	var startRow = 1;
	var RegExp = /\s/;
	var itm = ts_getInnerText(table.rows[1].cells[column]);
	while ((itm.replace(RegExp, "") == "") && startRow < table.rows.length) //in case of blank cells, find next cell
	{
		startRow++;
		itm = ts_getInnerText(table.rows[startRow].cells[column]);
	}

	var direction = span.getAttribute("sortdir");
	if(direction==null) direction = 'up';

    sortfn = ts_sort_caseinsensitive;
    if (itm.match(/^\d\d[\/-]\d\d[\/-]\d\d\d\d$/)) sortfn = ts_sort_date;
    if (itm.match(/^\d\d[\/-]\d\d[\/-]\d\d$/)) sortfn = ts_sort_date;
    if (itm.match(/^[�$]/)) sortfn = ts_sort_currency;
    if (itm.match(/^[-+]?[\d\.]+$/)) sortfn = ts_sort_numeric;
    if (itm.match(/^na$/)) sortfn = ts_sort_numeric;

    if (tableID == 'ssdResults') {
	if (direction == 'up') {
	    if (sortfn == ts_sort_caseinsensitive) sortfn = ICESSD_sort_caseinsensitive_up; 
	    if (sortfn == ts_sort_date) sortfn = ICESSD_sort_date_up; 
	    if (sortfn == ts_sort_currency) sortfn = ICESSD_sort_currency_up; 
	    if (sortfn == ts_sort_numeric) sortfn = ICESSD_sort_numeric_up; }
	if (direction == 'down') {
	    if (sortfn == ts_sort_caseinsensitive) sortfn = ICESSD_sort_caseinsensitive_down; 
	    if (sortfn == ts_sort_date) sortfn = ICESSD_sort_date_down; 
	    if (sortfn == ts_sort_currency) sortfn = ICESSD_sort_currency_down; 
	    if (sortfn == ts_sort_numeric) sortfn = ICESSD_sort_numeric_down; }  }

    SORT_COLUMN_INDEX = column;
    var firstRow = [];
    var newRows = [];
    for (i=0;i<table.rows[0].length;i++) { firstRow[i] = table.rows[0][i]; }
    for (j=1;j<table.rows.length;j++) { newRows[j-1] = table.rows[j]; }

    newRows.sort(sortfn);

    if (span.getAttribute("sortdir") == 'down') {
        ARROW = '&nbsp;&uarr;';
	if (tableID != 'ssdResults')
        newRows.reverse();
        span.setAttribute('sortdir','up');
    } else {
        ARROW = '&nbsp;&darr;';
        span.setAttribute('sortdir','down');
    }
    
    // We appendChild rows that already exist to the tbody, so it moves them rather than creating new ones
    // don't do sortbottom rows
    for (i=0;i<newRows.length;i++) { if (!newRows[i].className || (newRows[i].className && (newRows[i].className.indexOf('sortbottom') == -1))) table.tBodies[0].appendChild(newRows[i]);}
    // do sortbottom rows only
    for (i=0;i<newRows.length;i++) { if (newRows[i].className && (newRows[i].className.indexOf('sortbottom') != -1)) table.tBodies[0].appendChild(newRows[i]);}
    
    // Delete any other arrows there may be showing
    var allspans = document.getElementsByTagName("span"); 
    for (var ci=0;ci<allspans.length;ci++) {
        if (allspans[ci].className == 'sortarrow') {
            if (getParent(allspans[ci],"table") == getParent(lnk,"table")) { // in the same table as us?
                allspans[ci].innerHTML = '';
            }
        }
    }
        
    span.innerHTML = ARROW;
}

function getParent(el, pTagName) {
	if (el == null) return null;
	else if (el.nodeType == 1 && el.tagName.toLowerCase() == pTagName.toLowerCase())	// Gecko bug, supposed to be uppercase
		return el;
	else
		return getParent(el.parentNode, pTagName);
}
function ts_sort_date(a,b) {
    // y2k notes: two digit years less than 50 are treated as 20XX, greater than 50 are treated as 19XX
    aa = ts_getInnerText(a.cells[SORT_COLUMN_INDEX]);
    bb = ts_getInnerText(b.cells[SORT_COLUMN_INDEX]);
    if (aa.length == 10) {
        dt1 = aa.substr(6,4)+aa.substr(3,2)+aa.substr(0,2);
    } else {
        yr = aa.substr(6,2);
        if (parseInt(yr) < 50) { yr = '20'+yr; } else { yr = '19'+yr; }
        dt1 = yr+aa.substr(3,2)+aa.substr(0,2);
    }
    if (bb.length == 10) {
        dt2 = bb.substr(6,4)+bb.substr(3,2)+bb.substr(0,2);
    } else {
        yr = bb.substr(6,2);
        if (parseInt(yr) < 50) { yr = '20'+yr; } else { yr = '19'+yr; }
        dt2 = yr+bb.substr(3,2)+bb.substr(0,2);
    }
    if (dt1==dt2) return 0;
    if (dt1<dt2) return -1;
    return 1;
}

function ts_sort_currency(a,b) { 
    aa = ts_getInnerText(a.cells[SORT_COLUMN_INDEX]).replace(/[^0-9.]/g,'');
    bb = ts_getInnerText(b.cells[SORT_COLUMN_INDEX]).replace(/[^0-9.]/g,'');
    return parseFloat(aa) - parseFloat(bb);
}

function ts_sort_numeric(a,b) { 
    aa = parseFloat(ts_getInnerText(a.cells[SORT_COLUMN_INDEX]));
    if (isNaN(aa)) aa = 0;
    bb = parseFloat(ts_getInnerText(b.cells[SORT_COLUMN_INDEX])); 
    if (isNaN(bb)) bb = 0;
    return aa-bb;
}

function ts_sort_caseinsensitive(a,b) {
    aa = ts_getInnerText(a.cells[SORT_COLUMN_INDEX]).toLowerCase();
    bb = ts_getInnerText(b.cells[SORT_COLUMN_INDEX]).toLowerCase();
    if (aa==bb) return 0;
    if (aa<bb) return -1;
    return 1;
}

function ts_sort_default(a,b) {
    aa = ts_getInnerText(a.cells[SORT_COLUMN_INDEX]);
    bb = ts_getInnerText(b.cells[SORT_COLUMN_INDEX]);
    if (aa==bb) return 0;
    if (aa<bb) return -1;
    return 1;
}


function addEvent(elm, evType, fn, useCapture)
// addEvent and removeEvent
// cross-browser event handling for IE5+,  NS6 and Mozilla
// By Scott Andrew
{
  if (elm.addEventListener){
    elm.addEventListener(evType, fn, useCapture);
    return true;
  } else if (elm.attachEvent){
    var r = elm.attachEvent("on"+evType, fn);
    return r;
  } else {
    alert("Handler could not be removed");
  }
} 

function ICESSD_sort_date_up(a,b) {
    // y2k notes: two digit years less than 50 are treated as 20XX, greater than 50 are treated as 19XX
    aa = ICESSD_getVal(a,[SORT_COLUMN_INDEX]);
    bb = ICESSD_getVal(b,[SORT_COLUMN_INDEX]);
    if (aa.length == 10) {
        dt1 = aa.substr(6,4)+aa.substr(3,2)+aa.substr(0,2);
    } else {
        yr = aa.substr(6,2);
        if (parseInt(yr) < 50) { yr = '20'+yr; } else { yr = '19'+yr; }
        dt1 = yr+aa.substr(3,2)+aa.substr(0,2);
    }
    if (bb.length == 10) {
        dt2 = bb.substr(6,4)+bb.substr(3,2)+bb.substr(0,2);
    } else {
        yr = bb.substr(6,2);
        if (parseInt(yr) < 50) { yr = '20'+yr; } else { yr = '19'+yr; }
        dt2 = yr+bb.substr(3,2)+bb.substr(0,2);
    }
    if (dt1==dt2) return 0;
    if (dt1<dt2) return -1;
    return 1;
}


function ICESSD_sort_currency_up(a,b) { 
    aa = ICESSD_getVal(a,[SORT_COLUMN_INDEX]).replace(/[^0-9.]/g,'');
    bb = ICESSD_getVal(b,[SORT_COLUMN_INDEX]).replace(/[^0-9.]/g,'');
    return parseFloat(aa) - parseFloat(bb);
}

function ICESSD_sort_numeric_up(a,b) { 
    aa = parseFloat(ICESSD_getVal(a,[SORT_COLUMN_INDEX]));
    if (isNaN(aa)) aa = 0;
    bb = parseFloat(ICESSD_getVal(b,[SORT_COLUMN_INDEX])); 
    if (isNaN(bb)) bb = 0;
    if (a.cells[3].childNodes[0].nodeValue == b.cells[3].childNodes[0].nodeValue) return 0;
    return aa-bb;
}

function ICESSD_sort_caseinsensitive_up(a,b) {
    aa = ICESSD_getVal(a,[SORT_COLUMN_INDEX]).toLowerCase();
    bb = ICESSD_getVal(b,[SORT_COLUMN_INDEX]).toLowerCase();
    if (aa==bb) return 0;
    if (aa<bb) return -1;
    return 1;
}

function ICESSD_sort_default_up(a,b) {
    aa = ICESSD_getVal(a,[SORT_COLUMN_INDEX]);
    bb = ICESSD_getVal(b,[SORT_COLUMN_INDEX]);
    if (aa==bb) return 0;
    if (aa<bb) return -1;
    return 1;
}

function ICESSD_sort_date_down(a,b) {
    // y2k notes: two digit years less than 50 are treated as 20XX, greater than 50 are treated as 19XX
    aa = ICESSD_getVal(a,[SORT_COLUMN_INDEX]);
    bb = ICESSD_getVal(b,[SORT_COLUMN_INDEX]);
    if (aa.length == 10) {
        dt1 = aa.substr(6,4)+aa.substr(3,2)+aa.substr(0,2);
    } else {
        yr = aa.substr(6,2);
        if (parseInt(yr) < 50) { yr = '20'+yr; } else { yr = '19'+yr; }
        dt1 = yr+aa.substr(3,2)+aa.substr(0,2);
    }
    if (bb.length == 10) {
        dt2 = bb.substr(6,4)+bb.substr(3,2)+bb.substr(0,2);
    } else {
        yr = bb.substr(6,2);
        if (parseInt(yr) < 50) { yr = '20'+yr; } else { yr = '19'+yr; }
        dt2 = yr+bb.substr(3,2)+bb.substr(0,2);
    }
    if (dt1==dt2) return 0;
    if (dt1<dt2) return 1;
    return -1;
}


function ICESSD_sort_currency_down(a,b) { 
    aa = ICESSD_getVal(a,[SORT_COLUMN_INDEX]).replace(/[^0-9.]/g,'');
    bb = ICESSD_getVal(b,[SORT_COLUMN_INDEX]).replace(/[^0-9.]/g,'');
    return parseFloat(bb) - parseFloat(aa);
}

function ICESSD_sort_numeric_down(a,b) { 
    aa = parseFloat(ICESSD_getVal(a,[SORT_COLUMN_INDEX]));
    if (isNaN(aa)) aa = 0;
    bb = parseFloat(ICESSD_getVal(b,[SORT_COLUMN_INDEX])); 
    if (isNaN(bb)) bb = 0;
    if (a.cells[3].childNodes[0].nodeValue == b.cells[3].childNodes[0].nodeValue) return 0;
    return bb-aa;
}

function ICESSD_sort_caseinsensitive_down(a,b) {
    aa = ICESSD_getVal(a,[SORT_COLUMN_INDEX]).toLowerCase();
    bb = ICESSD_getVal(b,[SORT_COLUMN_INDEX]).toLowerCase();
    if (aa==bb) return 0;
    if (aa<bb) return 1;
    return -1;
}

function ICESSD_sort_default_down(a,b) {
    aa = ICESSD_getVal(a,[SORT_COLUMN_INDEX]);
    bb = ICESSD_getVal(b,[SORT_COLUMN_INDEX]);
    if (aa==bb) return 0;
    if (aa<bb) return 1;
    return -1;
}

function ICESSD_getVal(row,col)
{
	if(!row.cells) return -10000000;	
	
	if(row.cells[1].childNodes.length) 
		row = document.getElementById(row.cells[1].childNodes[0].id.substring(0,row.cells[1].childNodes[0].id.indexOf('!')+1)).parentNode.parentNode;
	switch (parseInt(col)) {
		case 2: //common name
			return ts_getInnerText(row.cells[col]);
			break;
		case 3: //scientific name
			return ts_getInnerText(row.cells[col]);
			break;
		case 4: //toxicity
			return row.cells[0].childNodes[0].value.split(",")[3];
			break;
		case 5: //conf int.
			return row.cells[0].childNodes[0].value.split(",")[4];
			break;
		case 6: //surrogate
			return row.cells[0].childNodes[0].value.split(",")[8];
			break;
		case 7: //df
			return row.cells[0].childNodes[0].value.split(",")[9];
			break;
		case 8: //r2
			return row.cells[0].childNodes[0].value.split(",")[10];
			break;
		case 9: //pval
			return row.cells[0].childNodes[0].value.split(",")[11];
			break;
		case 10: //MSE
			return row.cells[0].childNodes[0].value.split(",")[12];
			break;
		case 11: //cross val.
			return row.cells[0].childNodes[0].value.split(",")[13];
			break;
		case 12: //tax. dist.
			return row.cells[0].childNodes[0].value.split(",")[14];
			break;
		case 13: //slope
			return row.cells[0].childNodes[0].value.split(",")[15];
			break;
		case 14: //intercept
			return row.cells[0].childNodes[0].value.split(",")[16];
			break;
//		default:
//			alert('aieeeeee!');
	}
}