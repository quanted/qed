/*
Functions for calculating geometric mean for the
p-chem table. Gets called by cts_pchemprop_requests.html.
*/

var geomeanDict;

function handleGeomean(workflow, run_type) {
    /*
    Handles geomean calculation by workflow and
    run type.
    */
    geomeanDict = {};  // initializes global geomean dictionary
    if (run_type == 'single' && workflow == 'pchemprop') {
    	var pchemDict = batch_data;  // gets all pchem values for chemical
    	calculateGeomean(geomeanDict, pchemDict);  // calculates geomean for pchemprop workflow, single mode
    	addGeomeanToTable(geomeanDict);
	}
	else if (run_type == 'single' && workflow == 'gentrans') {
		var pchemDict = buildChemDictFromMetabolites();  // pchem data for each metabolite organized by genKey
		for (genKey in pchemDict) {
			var metaboliteData = pchemDict[genKey];
			var metaboliteGeomean = {};
			geomeanDict[genKey] = calculateGeomean(metaboliteGeomean, metaboliteData);
			addGeomeanDataToNode(metaboliteGeomean, metaboliteData);
		}
	}
	else if (run_type == 'batch' && workflow == 'pchemprop') {
		var pchemDict = batch_data;
		// TODO: Organize batch data like buildChemDictFromMetabolites(), but
		// using SMILES as keys instead of genKey.
		var pchemDict = buildChemDictFromBatchList();
		for (batchChemSmiles in pchemDict) {

			var batchChemData = pchemDict[batchChemSmiles];
			var batchChemGeomean = {};
			geomeanDict[batchChemSmiles] = calculateGeomean(batchChemGeomean, batchChemData);
		}
	}
	else if (run_type == 'batch' && workflow == 'gentrans') {
		return;
	}
}



function calculateGeomean(_geomeanDict, pchemData) {
	/*
	Calculates the logarithmic geomean of CTS
    p-chem data for ChemAxon, EPI, TEST, and SPARC
    calculators. Adds data to pchem table as well.
	*/
	// Props that use the standard mean calculation (already in log, or have negative values):
	var meanProps = ['kow_no_ph', 'koc', 'log_bcf', 'log_baf', 'kow_wph'];
	// Props that use the geometric mean:
    var geomeanProps = ['melting_point', 'boiling_point', 'water_sol', 'vapor_press', 'mol_diss', 'mol_diss_air', 'henrys_law_con', 'water_sol_ph'];
    var props = meanProps.concat(geomeanProps);
    for (var ind in props) {
        var prop = props[ind];
        var geomeanSum = 0.0;
        var isNegative = checkForNegativeValues(prop, pchemData);
        var isMPorBP = prop == 'melting_point' || prop == 'boiling_point';
    	if (meanProps.indexOf(prop) > -1 || (isNegative && !isMPorBP)) {
            // Gets average for props already in log form:
            var geomeanSumVals = sumPropValsForGeomean(prop, true, pchemData);
            geomeanSum = geomeanSumVals.sum;
            _geomeanDict[prop] = geomeanSum / geomeanSumVals.numVals;
            isNegative = false;
        }
        else if (geomeanProps.indexOf(prop) > -1) {
            // Gets geomean for props not yet in log form:
            var geomeanSumVals = sumPropValsForGeomean(prop, false, pchemData);
            geomeanSum = geomeanSumVals.sum;
            var geomeanVal = Math.pow(10, (1.0/geomeanSumVals.numVals)*geomeanSum);
            if (prop == 'melting_point' || prop == 'boiling_point') {
            	geomeanVal = convertKelvinToCelsius(geomeanVal);
            }
            _geomeanDict[prop] = geomeanVal;
        }
    }
    return _geomeanDict
}



function sumPropValsForGeomean(prop, isLog, pchemData) {
    /*
    Loops through calc values by property, summing them up
    by wrapping them in a log() or not depending if the property
    is already in log form.
    */
    var dataSum = 0.0;  // sum of data values for a given prop
    var numVals = 0;  // number of data values that are summed
    // for (var ind in batch_data) {
    for (var ind in pchemData) {
        var dataObj = pchemData[ind];
        var dataVal;
        // Continues looping until data for requested prop is found:
        if (dataObj['prop'] != prop) { continue; }
        // Skips 'measured' data for geomean calculations:
        if (dataObj['calc'] == "measured") { continue; }
        dataVal = parseFloat(dataObj['data']);  // gets pchem data value
        if(dataObj['prop'] == 'melting_point' || dataObj['prop'] == 'boiling_point') {
         	dataVal = convertCelsiusToKelvin(dataVal);
        }
        // Ignore any vals that aren't numbers (e.g., error message):
        if (isNaN(dataVal)) { continue; }
        // Sums data vals by prop, wrapping in log() if prop isn't already in log form:
        if (isLog) {
            dataSum = dataSum + dataVal;
        }
        else {
            dataSum = dataSum + Math.log10(dataVal);
        }
        numVals = numVals + 1;
    }
    return {sum: dataSum, numVals: numVals};
}



function addGeomeanToTable(geomeanDict) {
    /*
    Adds geomean to pchem table if it's a user
    requested property.
    */
    for (propKey in geomeanDict) {
    	var geomean = geomeanDict[propKey];
    	if (validateGeomean(geomean)) {
	        var pchemTableCell = $('.geomean.' + propKey);  // selects table cell for adding geomean to pchem table
	        $(pchemTableCell).html(organizeData('geomean', propKey, geomean));  // adds geomean to table cell
	    }
    }	    
}



function validateGeomean(geomean) {
	/*
	Ensures geomean value is valid (i.e., a number).
	*/
	if (geomean > 0.0 || geomean < 0.0) {
		return true;
    }
    else {
    	return false;
    }
}



function clearGeomeanColumn() {
    /*
    Clears html content from pchem table's geomean column.
    */
    $('.geomean').each(function(i, obj) {
        $(this).html("");
    });
}



function addSpinnersToGeomeanColumn() {
    /*
    Adds spinning wheels to geomean column while p-chem
    data is being retrieved.
    */
    $('.geomean').each(function(i, obj) {
        $(this).html(spinner_html);
    });   
}



function buildChemDictFromMetabolites() {
	/*
	Builds dict ordered by genKey for transformation
	products (single mode). Uses global var batch_data
	from cts_pchemprop_requests.html.
	*/
	var pchemDict = {};  // dict ordered by genKey, with results as list of chem data objects
	for (ind in batch_data) {
		var pchemData = batch_data[ind];
		// Continues to next iteration if not a pchem response for metabolite
		if (!('node' in pchemData['request_post'])) { continue; }
		var chemGenKey = pchemData['request_post']['node']['genKey'];
		// Continues to next iteration if no genKey
		if (!chemGenKey) { continue; }
		if (Object.keys(pchemDict).indexOf(chemGenKey) <= -1) {
			pchemDict[chemGenKey] = [];  // adds array to new key in pchemDict
		}
		pchemDict[chemGenKey].push(pchemData);  // adds pchem data to genKey
	}
	return pchemDict
}



function addGeomeanDataToNode(metaboliteGeomean, metaboliteData) {
	/*
	Adds geomean dict to each metabolite
	nodes' 'data' key on the gentrans single mode
	transformation products tree.
	*/
	for (var ind in metaboliteData) {
		var metabolite = metaboliteData[ind];
		for (node_index in st.graph.nodes) {
	        var matchedNode = st.graph.nodes[node_index];
	    	if (matchedNode.data.genKey != metabolite.node.genKey) {
	    		continue;	
	    	}
	    	if (!('geomeanDict' in matchedNode.data)) {
	            matchedNode.data.geomeanDict = {};
	            // return;
	        }
	        // Adds geomeanDict to node:
	       	// matchedNode.data.geomeanDict[metabolite.node.genKey];
	       	matchedNode.data.geomeanDict = metaboliteGeomean
	    }
	}
}



function buildChemDictFromBatchList() {
	/*
	Loops batch chems and creates a dict organized by
	the chems' smiles as keys.
	*/
    let reg = new RegExp('\r');
	var pchemDict = {};  // dict ordered by batch smiles
	for (var chemInd in batch_chems) {
		var chemObj = batch_chems[chemInd];  // a given batch chem
        chemObj['chemical'] = chemObj['chemical'].replace(reg, '');  // remove any '\r'
		pchemDict[chemObj.chemical] = [];  // creates list for pchem data objects
		for (ind in batch_data) {
			var pchemDataObj = batch_data[ind];
            pchemDataObj['chemical'] = pchemDataObj['chemical'].replace(reg, '');
			if (!('chemical' in pchemDataObj)) { continue; }
			if (pchemDataObj['chemical'] != chemObj.chemical) { continue; }
			pchemDict[chemObj.chemical].push(pchemDataObj);
		}
	}
	return pchemDict;
}



function checkForNegativeValues(prop, pchemData) {
	/*
	Checks data for any negative values before
	computing the geomean.
	*/
	for (var ind in pchemData) {
        var dataObj = pchemData[ind];
        if (dataObj['prop'] != prop) {
        	continue;
        }
        if (dataObj['data'] < 0) {
        	return true;
        }
    }
    return false;
}



function convertCelsiusToKelvin(data) {
	return 273.15 + parseFloat(data);
}



function convertKelvinToCelsius(data) {
	return parseFloat(data) - 273.15;
}