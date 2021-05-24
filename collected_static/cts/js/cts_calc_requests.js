// cts_pchemprop_requests.html javascript widget

var CalcRequestsHandler = {

	// global vars:

	spinner_html = '<img src="/static_qed/cts/images/loader.gif" id="spinner" />',
	calls_tracker = 0,  // calls tracker for data responses
	total_calls = 0,  // total calls expected from backend 
	socket = null,  // websocket var

	// CTS vars rendered from django templates
	template_vars_object = {
		'kowPH': null,
		'smiles': null,
		'name': null,
		'mass': null,
		'formula': null,
		'time': null,
		'checkedCalcsAndProps': null,
		'structure': '',
		'batch_data': [],
		'batch_chems': [],
		'workflow': '',
		'run_type': '',
		'speciation_inputs': null,
		'nodejs_host': null,
		'nodejs_port': null
	},

	// CTS backend calc data request object
	request_object = {
        'chemical': null,
        'ph': null,
        'node': null,
        'pchem_request': null,
        'nodes': null,
        'service': null,
        'calc': null,
        'workflow': null,
        'mass': null,
        'speciation_inputs': null,
        'run_type': null
	},

	init: function (request_json) {

		_request_object = CalcRequestsHandler.request_object

		// fill request object with values from django:
		for (var key in request_object) {
			console.log("index: " + index)
			if (key in request_json) {
				_request_object[key] = request_json[key];
			}
		}

		if (_request_object['batch_chems'] != null) {

			_num_batch_chems = CalcRequestsHandler.template_vars_object['batch_chems'].length;
			_calcs_props_object = CalcRequestsHandler.template_vars_object['checkedCalcsAndProps'];

	        CalcRequestsHandler.calls_tracker = CalcRequestsHandler.calculateTotalCalls([_num_batch_chems], _calcs_props_object);
	        CalcRequestsHandler.total_calls = calls_tracker;

	        // sessionStorage.setItem('calls_tracker', calls_tracker);
	        // sessionStorage.setItem('total_calls', total_calls);

	        CalcRequestsHandler.blockInterface(true);  // block UI with progress bar
	        $('#pdfExport, #htmlExport').hide();

	        CalcRequestsHandler.connectToSocket(structure, checkedCalcsAndProps, kowPH, null, null, batch_chems);

	    }
	    else if (structure === null || structure.length == 0) {
	        return;
	    }
	    else {
	        connectToSocket(structure, checkedCalcsAndProps, kowPH, null, null, null);
	    }

	},

	setup: function () {
		// jquery events, etc.

		// Get Data button (pchem workflow) for gathering pchem props:
	    $('#btn-pchem-data').on('click', function() {
	        //TODO: Change this conditional to something less general
	        if (socket) {
	            socket.close();
	        }
	        checkedCalcsAndProps = buildCheckedCalcsAndProps(); // from scripts_pchemprop.js
	        kowPH = $('#id_kow_ph').val();
	        connectToSocket(structure, checkedCalcsAndProps, kowPH, null, null, null);
	        // startPchemPropDataCollection(structure, checkedCalcsAndProps, kowPH, null, null);
	    });

	    // TODO: Cancel button, which removes pending tasks from celery queues:
	    $('#btn-pchem-cancel').on('click', function () {
	        console.log("pchem cancel button selected");
	        console.log("socket object: " + socket);
	        socket.send(JSON.stringify({'cancel': true, 'pchem_request': checkedCalcsAndProps}));
	        blockInterface(false);
	    });

	},

	buildCheckedCalcsAndProps: function () {
	    // builds object of checked calcs and props from the p-chem table

	    var calc_data_obj = {};

	    $('input.calc_checkbox:checked').each(function () {
	        var calc_name = $(this).attr('name'); 
	        var available_props = $('td.ChemCalcs_available.' + calc_name); // tbl cells of calc's available props..
	        var calc_prop_checkboxes = $(available_props).parent().find('input[type=checkbox]');

	        calc_data_obj[calc_name] = [];

	        $(calc_prop_checkboxes).each(function () {
	            if ($(this).is(':checked')) {
	                var prop_name = this.name;
	                calc_data_obj[calc_name].push(prop_name); 
	            }
	        });
	    });

	    return calc_data_obj;

	},

	startPchemPropDataCollection: function(structure, checkedCalcsAndProps, kowPH, node, currentNode, nodes) {
    
	    if (checkedCalcsAndProps == null) { return; }

	    // var num_pchem = parseFloat($('#gen-select-pchem').val()); // number of props
	    var addDataToTable = false; // whether to plot on visible pchem table or not..

	    // Determine whether data should be inserted into pchem table:
	    if (isPchemWorkflow() && window.location.href.indexOf('batch') < 0) { 
	        addDataToTable = true;
	    }
	    else if (currentNode != null && node.id == currentNode.id) { 
	        addDataToTable = true;
	    }
	    else { 
	        addDataToTable = false;
	    }

	    node_tracker = node;
	    addDataToTable_tracker = addDataToTable;

	    var pchem_data = {};

	    var pchem_data = {
	        'chemical': structure,
	        'ph': kowPH,
	        'node': node,
	        'pchem_request': checkedCalcsAndProps
	    };


	    // adding new nodes stuff:
	    if (nodes != null) {
	        pchem_data['nodes'] = nodes;  // add nodes key (list of nodes)
	    }

	    if (run_type != null) {
	        pchem_data['run_type'] = run_type
	    }

	    if (workflow == 'gentrans' && run_type == 'batch') {
	        
	        calls_tracker = 0;
	        for (node in nodes) {
	            calls_tracker++;
	        }
	        total_calls = calls_tracker;

	        sessionStorage.setItem('calls_tracker', calls_tracker);  //calls for products!
	        sessionStorage.setItem('total_calls', total_calls);

	        pchem_data['service'] = 'getTransProducts';
	        pchem_data['calc'] = 'chemaxon';
	        pchem_data['workflow'] = 'gentrans';
	    }


	    if (workflow == 'chemspec' && run_type == 'batch' ) {

	        for (node in nodes) {
	            calls_tracker++;
	        }
	        total_calls = calls_tracker;

	        sessionStorage.setItem('calls_tracker', calls_tracker);  //calls for products!
	        sessionStorage.setItem('total_calls', total_calls);

	        pchem_data['service'] = 'getSpeciationData';
	        pchem_data['calc'] = 'chemaxon';
	        pchem_data['workflow'] = 'chemspec';
	        pchem_data['speciation_inputs'] = speciation_inputs;

	    }

	    if (workflow == 'pchemprop' && run_type == 'single') {
	        pchem_data['mass'] = mass;
	    }
	    var is_one_chemical = !('nodes' in pchem_data);
	    if (workflow == 'gentrans' && is_one_chemical) {
	        pchem_data['mass'] = pchem_data['node']['data']['mass'];
	    }

	    // var pchem_data_json = stringifyLargeJsonObject(pchem_data);


	    // Send data to cts_nodejs server:
	    // socket.send('get_data', pchem_data_json);
	    socket.send(pchem_data_json);

	    // // testing separate socket.send() per calc to see if calls are parsed onto different workers or performed sequentially on one based on user WS connection...
	    // for (var calc in checkedCalcsAndProps) {
	    //     // var props = checkedCalcsAndProps[calc];
	    //     // pchem_data['props'] = props;
	    //     // var request_json_string = stringifyLargeJsonObject(pchem_data);
	    //     // socket.send(request_json_string);
	    //     for (var i = 0; i < checkedCalcsAndProps[calc].length; i++) {
	    //         var prop = checkedCalcsAndProps[calc][i]; // p-chem property..
	    //         pchem_data['prop'] = prop;
	    //         var request_json_string = stringifyLargeJsonObject(pchem_data);
	    //         socket.send(request_json_string);
	    //     }
	    // }


	    // adds spinners to table cells
	    for (var calc in checkedCalcsAndProps) {
	        for (var i = 0; i < checkedCalcsAndProps[calc].length; i++) {
	            var prop = checkedCalcsAndProps[calc][i]; // p-chem property..
	            var tblCell = $('.' + calc + '.' + prop); // table cell for spinner..
	            if (addDataToTable) { $(tblCell).html(spinner_html); }
	        }
	    }

	}

}




$(document).ready(function() {
    // Some global and local variable delcarations:
    checkedCalcsAndProps = {{checkedCalcsAndProps}};
    speciation_inputs = {{speciation_inputs}};
    structure = "{{structure}}";
    kowPH = "{{kow_ph}}";
    smiles = "{{structure}}";
    name = "{{name}}";
    mass = "{{mass}}";
    formula = "{{formula}}";
    time = "{{time}}";
    workflow = "{{workflow}}";
    // nodes = "{{nodes}}";  // defaults to ""
    batch_chems = {{nodes}};
    run_type = "{{run_type}}";
    nodejs_host = "{{nodejs_host}}";
    nodejs_port = {{nodejs_port}};

    $('#id_kow_ph').val(kowPH);  // set ph on pchem table to user val

    // connectToSocket();

    if (batch_chems != null) {

        // calls_tracker = batch_chems.length;
        calls_tracker = calculateTotalCalls([batch_chems.length], checkedCalcsAndProps);
        total_calls = calls_tracker;
        sessionStorage.setItem('calls_tracker', calls_tracker);
        sessionStorage.setItem('total_calls', total_calls);

        // block UI with progress bar
        blockInterface(true);

        $('#pdfExport, #htmlExport').hide();

        connectToSocket(structure, checkedCalcsAndProps, kowPH, null, null, batch_chems);
        // startPchemPropDataCollection(structure, checkedCalcsAndProps, kowPH, null, null, batch_chems);

    }
    else if (structure === null || structure.length == 0) {
        return;
    }
    else {
        connectToSocket(structure, checkedCalcsAndProps, kowPH, null, null, null);
        // startPchemPropDataCollection(structure, checkedCalcsAndProps, kowPH, null, null);
    }

    // Get Data button (pchem workflow) for gathering pchem props:
    $('#btn-pchem-data').on('click', function() {
        if (socket) {
            // socket.disconnect();
            socket.close();
        }
        checkedCalcsAndProps = buildCheckedCalcsAndProps(); // from scripts_pchemprop.js
        kowPH = $('#id_kow_ph').val();
        connectToSocket(structure, checkedCalcsAndProps, kowPH, null, null, null);
        // startPchemPropDataCollection(structure, checkedCalcsAndProps, kowPH, null, null);
    });

    // TODO: Cancel button, which removes pending tasks from celery queues:
    $('#btn-pchem-cancel').on('click', function () {
        console.log("pchem cancel button selected");
        console.log("socket object: " + socket);
        socket.send(JSON.stringify({'cancel': true, 'pchem_request': checkedCalcsAndProps}));
        blockInterface(false);
    });

});


function buildCheckedCalcsAndProps () {
    // front end way to get checkedCalcsAndProps without
    // calling cts-jchem rest
    var calc_data_obj = {};

    $('input.calc_checkbox:checked').each(function () {
        var calc_name = $(this).attr('name'); 
        var available_props = $('td.ChemCalcs_available.' + calc_name); // tbl cells of calc's available props..
        var calc_prop_checkboxes = $(available_props).parent().find('input[type=checkbox]');

        calc_data_obj[calc_name] = [];

        $(calc_prop_checkboxes).each(function () {
            if ($(this).is(':checked')) {
                var prop_name = this.name;
                calc_data_obj[calc_name].push(prop_name); 
            }
        });
    });
    return calc_data_obj;
}


function connectToSocket(structure, checkedCalcsAndProps, kowPH, node, currentNode, nodes) {

    // if (typeof io !== 'undefined') {
        
    //     // connect to socket.io!
    //     if (nodejs_host == 'nginx') {
    //         socket = io.connect();  // docker way
    //     }
    //     else {
    //         if (nodejs_port && nodejs_port != 80) {
    //             socket = io.connect('http://' + nodejs_host + ':' + nodejs_port, {'force new connection': true});
    //         }
    //         else {
    //             socket = io.connect(nodejs_host, {'force new connection': true});
    //         }
    //     }

    // }
    // else {
    //     socket = null;
    //     return;
    // }

    socket = new WebSocket("ws://" + window.location.host + "/channels/");

    // Call onopen directly if socket is already open
    if (socket.readyState == WebSocket.OPEN) socket.onopen();

    socket.onopen = function() {
        console.log("new socket opened..");
        startPchemPropDataCollection(structure, checkedCalcsAndProps, kowPH, node, currentNode, nodes);
    }

    socket.onclose = function() {
        console.log("socket closed..");
    }

    // incoming data pushed to client from redis:
    // socket.on('message', function(data) {
    socket.onmessage = function(message_event) {
        
        data = JSON.parse(message_event.data);

        // expecting node object for gentrans workflow:
        // this conditional may ALWAYS be true! should be !=
        if (data['node'] != null) {

            calls_tracker--;
            sessionStorage.setItem('calls_tracker', calls_tracker);
            console.log("calls tracker: " + calls_tracker);

            if (window.location.href.indexOf('batch') > -1) {

                calls_tracker = parseInt(sessionStorage.getItem('calls_tracker'));
                total_calls = parseInt(sessionStorage.getItem('total_calls'));

                // if (workflow == 'gentrans') {
                if (data['workflow'] == 'gentrans') {
                    // workflow global var was getting set to false during
                    // gentrans batch, oddly enough...

                    if (data.prop == "products") {

                        // Metabolites results from gentrans batch:

                        // creating st instance for use of functions,
                        // like getting single list of n-nested nodes (st.graph.nodes)
                        init(data.data);
                        st_array.push(st);  // add spacetree instance to array

                        var products = st.graph.nodes;
                        var product_data = [];
                        for (product in products) {
                            var product_gen = parseFloat(products[product]['data']['generation']);
                            if (product_gen <= genMax) {
                                product_data.push(products[product]['data']);
                            }
                        }

                        batch_data.push(product_data);

                        // TODO: Refactor this section
                        // If p-chem data requested, make requests for products
                        if (Object.keys(checkedCalcsAndProps).length > 0) {

                            // getting pchem data for a batch chem's trans products..
                            // calls_tracker needs to be increased to account for
                            // batch chem products.

                            // need to increase total_calls with batch chem's
                            // products and p-chem requests:
                            // total_calls += calculateTotalCalls([product_data.length], checkedCalcsAndProps);
                            // total_calls += calculateTotalCalls([product_data.length], checkedCalcsAndProps);
                            total_calls = calls_tracker + calculateTotalCalls([product_data.length], checkedCalcsAndProps);
                            // calls_tracker = total_calls - 1;
                            calls_tracker = total_calls
                            sessionStorage.setItem('calls_tracker', calls_tracker);
                            sessionStorage.setItem('total_calls', total_calls);

                            var pchem_data = {
                                'chemical': structure,
                                'ph': kowPH,
                                'nodes': product_data,
                                'pchem_request': checkedCalcsAndProps,
                                'run_type': run_type,
                                'workflow': 'gentrans'
                            };

                            var cache = [];
                            var pchem_data_json = JSON.stringify(pchem_data, function(key, value) {
                                if (typeof value === 'object' && value !== null) {
                                    if (cache.indexOf(value) !== -1) {
                                        // Circular reference found, discard key
                                        return;
                                    }
                                    // Store value in our collection
                                    cache.push(value);
                                }
                                return value;
                            });
                            cache = null; // Enable garbage collection

                            // socket.send('get_data', pchem_data_json);
                            socket.send(pchem_data_json);

                        }

                    }
                    else {

                        // 'prop' key not 'products', assuming p-chem prop
                        // todo: prop keys for checking, refactor to js obj

                        // get genKey of incoming data object:
                        var data_obj_genkey = data['node']['genKey'];
                        var data_obj_smiles = data['node']['smiles'];  // this or data['chemical']?

                        // add p-chem data to the right metabolite in batch_data array
                        for (var index in batch_data) {

                            var batch_chem = batch_data[index];

                            if (batch_chem.length > 0) {
                                // batch chem has metabolites..
                                for (prod_index in batch_chem) {

                                    var prod_obj = batch_chem[prod_index];

                                    if (prod_obj['genKey'] == data_obj_genkey && prod_obj['smiles'] == data_obj_smiles) {

                                        var data_obj = {
                                            'data': data['data'],
                                            'prop': data['prop'],
                                            'calc': data['calc']
                                        }
                                        if ('method' in data) { data_obj['method'] = data['method']; }

                                        if (!('pchemprops' in prod_obj)) {
                                            batch_data[index][prod_index]['pchemprops'] = [];
                                        }
                                        batch_data[index][prod_index]['pchemprops'].push(data_obj);

                                    }

                                }
                            }
                            
                        }

                    }

                }
                else {
                    batch_data.push(data);
                }

            }
            else {
                batch_data.push(data);
            }


            if (calls_tracker <= 0) {
                console.log("All data retrieved!");
                blockInterface(false);

                var pchemprop_option = $('#gen-select-pchem').val();

                if (workflow == 'gentrans' && pchemprop_option != "0" && pchemprop_option != undefined) {
                    displayProductData();  // cts_gentrans_tree function
                }

                // if batch, display link for CSV:
                if (window.location.href.indexOf('batch') > -1) {
                    $('#export_menu').css('position', 'relative');
                    $('#export_menu').prepend('<h3>Batch results ready for download</h3>');
                }


            }
            else {
                updateProgressBar(calls_tracker, total_calls);
            }

            var data_node;
            if ('data' in data['node']) {
                data_node = data['node']['data'];
            }
            else {
                data_node = data['node'];
            }

        }

        parseResponseToPchemTable(data, data_node, false, addDataToTable_tracker);

    }
}


function startPchemPropDataCollection(structure, checkedCalcsAndProps, kowPH, node, currentNode, nodes) {
    
    if (checkedCalcsAndProps == null) { return; }

    // var num_pchem = parseFloat($('#gen-select-pchem').val()); // number of props
    var addDataToTable = false; // whether to plot on visible pchem table or not..

    // Determine whether data should be inserted into pchem table:
    if (isPchemWorkflow() && window.location.href.indexOf('batch') < 0) { 
        addDataToTable = true;
    }
    else if (currentNode != null && node.id == currentNode.id) { 
        addDataToTable = true;
    }
    else { 
        addDataToTable = false;
    }

    node_tracker = node;
    addDataToTable_tracker = d;

    var pchem_data = {};

    var pchem_data = {
        'chemical': structure,
        'ph': kowPH,
        'node': node,
        'pchem_request': checkedCalcsAndProps
    };


    // adding new nodes stuff:
    if (nodes != null) {
        pchem_data['nodes'] = nodes;  // add nodes key (list of nodes)
    }

    if (run_type != null) {
        pchem_data['run_type'] = run_type
    }

    if (workflow == 'gentrans' && run_type == 'batch') {
        
        calls_tracker = 0;
        for (node in nodes) {
            calls_tracker++;
        }
        total_calls = calls_tracker;

        sessionStorage.setItem('calls_tracker', calls_tracker);  //calls for products!
        sessionStorage.setItem('total_calls', total_calls);

        pchem_data['service'] = 'getTransProducts';
        pchem_data['calc'] = 'chemaxon';
        pchem_data['workflow'] = 'gentrans';
    }


    if (workflow == 'chemspec' && run_type == 'batch' ) {

        for (node in nodes) {
            calls_tracker++;
        }
        total_calls = calls_tracker;

        sessionStorage.setItem('calls_tracker', calls_tracker);  //calls for products!
        sessionStorage.setItem('total_calls', total_calls);

        pchem_data['service'] = 'getSpeciationData';
        pchem_data['calc'] = 'chemaxon';
        pchem_data['workflow'] = 'chemspec';
        pchem_data['speciation_inputs'] = speciation_inputs;

    }

    if (workflow == 'pchemprop' && run_type == 'single') {
        pchem_data['mass'] = mass;
    }
    var is_one_chemical = !('nodes' in pchem_data);
    if (workflow == 'gentrans' && is_one_chemical) {
        pchem_data['mass'] = pchem_data['node']['data']['mass'];
    }

    // var pchem_data_json = stringifyLargeJsonObject(pchem_data);


    // Send data to cts_nodejs server:
    // socket.send('get_data', pchem_data_json);
    // socket.send(pchem_data_json);

    // testing separate socket.send() per calc to see if calls are parsed onto different workers or performed sequentially on one based on user WS connection...
    for (var calc in checkedCalcsAndProps) {
        // var props = checkedCalcsAndProps[calc];
        // pchem_data['props'] = props;
        // var request_json_string = stringifyLargeJsonObject(pchem_data);
        // socket.send(request_json_string);
        for (var i = 0; i < checkedCalcsAndProps[calc].length; i++) {
            var prop = checkedCalcsAndProps[calc][i]; // p-chem property..
            pchem_data['prop'] = prop;
            var request_json_string = stringifyLargeJsonObject(pchem_data);
            socket.send(request_json_string);
        }
    }


    // adds spinners to table cells
    for (var calc in checkedCalcsAndProps) {
        for (var i = 0; i < checkedCalcsAndProps[calc].length; i++) {
            var prop = checkedCalcsAndProps[calc][i]; // p-chem property..
            var tblCell = $('.' + calc + '.' + prop); // table cell for spinner..
            if (d) { $(tblCell).html(spinner_html); }
        }
    }

}


function stringifyLargeJsonObject(json_obj) {
    var cache = [];
    var json_string = JSON.stringify(json_obj, function(key, value) {
        if (typeof value === 'object' && value !== null) {
            if (cache.indexOf(value) !== -1) {
                // Circular reference found, discard key
                return;
            }
            // Store value in our collection
            cache.push(value);
        }
        return value;
    });
    cache = null; // Enable garbage collection
    return json_string;
}


function parseListDataFromResults(data, node, d) {
    var calc = data['calc']; // sparc
    var props = data['props']; // get sparc props list
    var data_key = "";
    if ('error' in data) {
        for (prop in props) {
            var prop_obj = {'calc': data['calc'], 'prop': prop, 'data': data['error']};
            parseResponseToPchemTable(prop_obj, node, false, d);  // note: hasData hardcoded to false!!
        }
    }
    else { 
        for (prop_data in data['data']) {
            var prop_obj;
            if ('error' in data) { 
                prop_data = {'calc': data['calc'], 'prop': data['prop'], 'data': data['error']};
            }
            else { 
                prop_obj = data['data'][prop_data];
            }
            parseResponseToPchemTable(prop_obj, node, false, d);  // note: hasData hardcoded to false!!
        }   
    }
}


function isPchemWorkflow() {
    var workflow_url = window.location.href;
    if (workflow_url.indexOf("pchem") > -1) { return true; }
    else { return false; }
}


function parseResponseToPchemTable(response, node, hasData, d) {
    // Map response to pchemprop output table.
    // Every calc-prop data value comes here.

    var calc = response['calc'];
    var prop = response['prop'];
    var table_cell = $('.' + calc + '.' + prop); // table cell for calc's prop..
    var data;

    // TODO: improve error handling to mitigate error checking like below..
    if (response.hasOwnProperty('error')) { 
        // $(table_cell).html("");
        $(table_cell).html(response['error']);
        return;
    }

    else if (!('data' in response)) {
        $(table_cell.html("error processing data"));
        return;
    }
    else if (calc == "epi") {
        if (response.data.propertyvalue) {
            data = response.data.propertyvalue;
        }
        else {
            data = response['data'];
        }
    }
    else { data = response['data']; }

    // Add pchemprop data to node if gentrans workflow:
    // if (!isPchemWorkflow()) {
    if (workflow == 'gentrans' && run_type != 'batch') {

        // get node object from spacetree:
        for (node_index in st.graph.nodes) {
            var some_node = st.graph.nodes[node_index];
            if (some_node.data.genKey == node.genKey) {
                node = some_node;
            }
        }

        if (!node.data.hasOwnProperty('pchemprops')) {
            node.data.pchemprops = []; // keys: calc, prop, data (single-level)..
        }
        var post_data = {"calc": calc, "prop": prop, "data": data};
        if (response.hasOwnProperty('method')) { 
            post_data['method'] = response['method'];
        }
        if (hasData == false) {
            node.data.pchemprops.push(post_data);
            // $('')
            addPchemDataToNode(node, post_data);
        }
    }

    if (response.hasOwnProperty('method') && response['method'] !== null) {
        var method = response['method'];
        var has_spinner = $(table_cell).children('img#spinner').length;
        if (has_spinner > 0) { $(table_cell).html(""); }
        if (d) {

            // make sure data isn't already there..

            var node_data = organizeData(calc, prop, data) + " " + method;
            var cell_data = $(table_cell).html().split('<br>');  // (remove trailing blank array item)
            cell_data.pop();

            var new_cell_data = "";
            var unique_data;

            if (cell_data.length <= 0) {
                new_cell_data = node_data + '<br>';
            }
            else {
                unique_data = $.unique(cell_data);

                for (item in cell_data) {
                    new_cell_data += cell_data[item] + '<br>';
                }

                new_cell_data += node_data + '<br>';

                var unique_array = new_cell_data.split('<br>');
                unique_array.pop();

                unique_array = $.unique(unique_array);

                new_cell_data = "";
                for (item in unique_array) {
                    new_cell_data += unique_array[item] + '<br>';
                }

            }

            $(table_cell).html(new_cell_data);


        }
    }
    else { 
        if (addDataToTable) { 
            $(table_cell).html(organizeData(calc, prop, data));
        }
    }

}


function organizeData(calc, prop, data) {
    // formats data for pchem table

    if (typeof data === "number") {
        if (prop == "water_sol" || prop == "vapor_press" || prop == "mol_diss" || prop == "henrys_law_con" || prop == "water_sol_ph") {
            if (calc == "test" && prop == "vapor_press") { 
                data = Math.pow(10, data);
            }
            return data.toExponential(2);
        }
        else {
            return data.toFixed(2);
        }
    }

    if (typeof data === "string" || data == null) {
        return data;
    }

    // For multiple pKa values in a cell..
    var parsedData = "";
    for (item in data) {
        if (data.hasOwnProperty(item) && data[item] != null) {
            var itemVals = data[item];
            if (itemVals.length == 0) {
                parsedData += '<div class="pka-wrapper">' + item + ': none</div>';
            }
            else {
                for (var i = 0; i < itemVals.length; i++) {
                    var label = item + String(i + 1).sub() +  ': ';
                    try {
                        parsedData += '<div class="pka-wrapper">' + label + itemVals[i].toFixed(2) + '</div>';    
                    }
                    catch (e) {
                        if (e instanceof TypeError) {
                            parsedData += '<div class="pka-wrapper">' + label + itemVals[i] + '</div>';  // probably a message instead of Number   
                        } 
                    }
                    
                }
            }
        }
    }
    return parsedData;
}


function calculateTotalCalls(nodes_list, checkedCalcsAndProps) {
    // get max calls for progress bar (max metabolites + calcs + props + any methods):
    var num_nodes = 0;
    for (var i = 0; i < nodes_list.length; i++) {
        num_nodes += nodes_list[i];
    }

    // if (workflow == 'chemspec') { return num_nodes; }  // 1req/chem in chemspec workflow

    var num_props = 0;
    for (calc in checkedCalcsAndProps) {
        if (checkedCalcsAndProps.hasOwnProperty(calc)) {
            var props = checkedCalcsAndProps[calc];
            for (var i = 0; i < props.length; i ++) {
                var prop = props[i];
                if (calc == "chemaxon") { 
                    if (prop == 'kow_no_ph' || prop == 'kow_wph') { 
                        num_props += 3;  // these chemaxon props have 3 methods
                    }
                    else { num_props += 1; }
                }
                else { num_props += 1; }
            }
        }
    }
    var total_calls = num_nodes * num_props;
    return total_calls;
}


function jsonRepack(jsonobj) {
  return JSON.parse(JSON.stringify(jsonobj));
}

</script>