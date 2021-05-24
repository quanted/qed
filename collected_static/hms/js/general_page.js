// General js for hms model/submodel pages //
var taskID;
var counter = 250;
var componentData;
var resultMetaTable;
var resultDataTable;
var dyGraph;

google.charts.load('current', {'packages': ['table', 'corechart']});

$(function () {
    // $("#component_tabs").tabs({
    //     disabled: [2]
    // });

    var datepicker_options = {
        changeMonth: true,
        changeYear: true,
        autosize: true,
        yearRange: '1900:2100'
    };
    // Page load functions
    $("#id_startDate").datepicker(datepicker_options);
    $("#id_endDate").datepicker(datepicker_options);

    $("#id_source").on("change", setSourceConfig);

    // $('.submit_data_request').on('click', getTestData);
    $('.submit_data_request').on('click', getData2);
    setTimeout(pageLoad, 400);
    setTimeout(pageSpecificLoad, 500);
    setTimeout(loadCookies, 400);
    setTimeout(setSourceConfig, 100);
    setTimeout(pageSpecificLoad, 100);
});

function pageLoad() {
    $('#load_page').fadeToggle(600);
    browserCheck();
    return false;
}

function pageSpecificLoad(){
    var current = window.location.href;
    if(current.includes("output_data")){
        taskID = $("#task_id").html();
        if(taskID === "None"){
            toggleLoader(false, "Unable to find your data request task ID. Please select a valid task ID or submit a new request.");
            $("#loader_box").hide();
        }
        else {
            console.log("Data request success. Task ID: " + taskID);
            toggleLoader(false, "Processing data request. Task ID: " + taskID);
            setTimeout(getDataPolling, 500);
        }
    }
}

function setSourceConfig(){
    var src = $('#id_source').val();
    var local = null;
    var resolution = null;
    if (sourceConfigs.hasOwnProperty(src)) {
        local = sourceConfigs[src]['localtime'];
        resolution = sourceConfigs[src]['temporalResolution'];
    }
    if(local){
        $("#id_timelocalized option[value='true']").removeAttr('disabled');
        $("#id_timelocalized option[value='true']").removeAttr('selected');
        $("#id_timelocalized option[value='true']").attr('selected', 'selected');
    }
    else{
        $("#id_timelocalized option[value='true']").removeAttr('selected');
        $("#id_timelocalized option[value='true']").attr('disabled', 'disabled');
        $("#id_timelocalized option[value='false']").attr('selected', 'selected');
    }

    if(resolution) {
        var validRes = false;
        var resolutionOptions = document.getElementById("id_temporalresolution").getElementsByTagName("option");
        for (var i = 0; i < resolutionOptions.length - 1; i++) {
            if (!validRes) {
                if (resolutionOptions[i].value === resolution) {
                    validRes = true;
                    resolutionOptions[i].disabled = false;
                    resolutionOptions[i].selected = true;
                } else {
                    resolutionOptions[i].disabled = true;
                }
            } else {
                resolutionOptions[i].disabled = false;
            }
        }
    }
    if(src === "gldas" || src === "trmm") {
        $("#id_temporalresolution option[value='hourly']").attr('disabled', 'disabled');
        $("#id_temporalresolution option[value='3hourly']").removeAttr('disabled');
    }
    else {
        $("#id_temporalresolution option[value='3hourly']").attr('disabled', 'disabled');
    }
}

function getData() {
    var params = getParameters();
    $.ajax({
        type: "POST",
        url: baseUrl,
        accepts: "application/json",
        data: JSON.stringify(params),
        processData: false,
        timeout: 0,
        contentType: "application/json",
        success: function (data, textStatus, jqXHR) {
            console.log("Data request success");
            componentData = data;
            setOutputUI();
            $('#component_tabs').tabs("enable", 2);
            $('#component_tabs').tabs("option", "active", 2);
            toggleLoader(false,"");
            dyGraph.resize();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Data request error...");
            console.log(errorThrown);
            toggleLoader(false, "");
        },
        complete: function (jqXHR, textStatus) {
            console.log("Data request complete");
        }
    });
    return false;
}

function getData2() {
    var params = getParameters();
    $.ajax({
        type: "POST",
        url: baseUrl,
        accepts: "application/json",
        data: JSON.stringify(params),
        processData: false,
        timeout: 0,
        contentType: "application/json",
        success: function (data, textStatus, jqXHR) {
            taskID = data.job_id;
            var model = $("#model_name").html();
            var submodule = $("#submodule_name").html();
            window.location.href = "/hms/" + model + "/" + submodule + "/output_data/" + taskID + "/";
            // setDataRequestCookie(taskID);
            // console.log("Data request success. Task ID: " + taskID);
            // toggleLoader(false, "Processing data request. Task ID: " + taskID);
            // setTimeout(getDataPolling, 5000);
            // $('#component_tabs').tabs("enable", 2);
            // $('#component_tabs').tabs("option", "active", 2);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Data request error...");
            console.log(errorThrown);
            // toggleLoader(true, "");
        },
        complete: function (jqXHR, textStatus) {
            console.log("Data request complete");
        }
    });
    return false;
}

function getDataPolling() {
    counter = counter - 1;
    var requestUrl = "hms/rest/api/v2/hms/data";
    if (counter > 0) {
        $.ajax({
            type: "GET",
            url: requestUrl + "?job_id=" + taskID,
            accepts: "application/json",
            timeout: 0,
            contentType: "application/json",
            success: function (data, textStatus, jqXHR) {
                if (data.status === "SUCCESS") {
                    if (typeof data.data === "string") {
                        componentData = JSON.parse(data.data);
                    }else{
                        componentData = data.data;
                    }
                    console.log("Task successfully completed and data was retrieved.");
                    setDataRequestCookie(taskID);
                    setOutputUI();
                    toggleLoader(true, "");
                    setTitle();
                    toggleDownloadButtons(false);
                    dyGraph.resize();
                    counter = 250;
                }
                else if (data.status === "FAILURE") {
                    toggleLoader(false, "Task " + taskID + " encountered an error.");
                    console.log("Task failed to complete.");
                    deleteTaskFromCookie(jobID);
                }
                else {
                    setTimeout(getDataPolling, 5000);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Data request error...");
                console.log(errorThrown);
                toggleLoader(false, "Error retrieving data for task ID: " + taskID);
            },
            complete: function (jqXHR, textStatus) {
                console.log("Data request complete");
            }
        });
    }
    else {
        console.log("Failed to get data, reached polling cap.")
    }
    return false;
}

function getPreviousData() {
    taskID = $('#previous_task_id').val();
    var model = $("#model_name").html();
    var submodule = $("#submodule_name").html();
    window.location.href = "/hms/" + model + "/" + submodule + "/output_data/" + taskID + "/";
    return false;
}

function getPreviousDataFromID(id){
    taskID = id;
    var model = $("#model_name").html();
    var submodule = $("#submodule_name").html();
    window.location.href = "/hms/" + model + "/" + submodule + "/output_data/" + taskID + "/";
    return false;
}

function setMetadata() {
    var metaDataTile = componentData.dataset;
    var sourceTitle = componentData.dataSource.toUpperCase();
    $('#output_metadata_title').html(metaDataTile + ": " + sourceTitle + " Metadata");
    resultMetaTable = new google.visualization.DataTable();
    resultMetaTable.addColumn('string', 'Metadata');
    resultMetaTable.addColumn('string', 'Value');
    $.map(componentData.metadata, function (key, value) {
        resultMetaTable.addRow([value, key]);
    });
    var metaTable = new google.visualization.Table(document.getElementById('output_metadata'));
    var tableOptions = {
        pageSize: 10,
        width: '100%'
    };
    metaTable.draw(resultMetaTable, tableOptions);
    return false;
}

function setTitle() {
    if (taskID === null && testData) {
        taskID = "TESTTASK1234567890";
    }
    var title = "Data for Task: " + taskID.toString();
    var output_title = $("#output_title");
    output_title.html("<h3>" + title + "</h3>");
}

function setDataGraph() {
    var dataTile = componentData.dataset;
    var sourceTitle = componentData.dataSource;
    $('#output_data_title').html(dataTile + ": " + sourceTitle + " Data");
    var chartOption = {
        title: componentData.dataset,
        curveType: 'none',
        legend: {position: 'right'},
        width: 800,
        height: 600
    };

    resultDataTable = new google.visualization.DataTable();
    resultDataTable.addColumn({type: 'datetime', label: 'Date', pattern: 'MM-DD-YYYY HH'});
    var j = 2;
    $.each(componentData.metadata, function (k, v) {
        var testKey = "column_" + j.toString();
        if (k === testKey) {
            resultDataTable.addColumn({type: 'number', label: v});
            j++;
        }
    });
    var colNum = componentData.data[Object.keys(componentData.data)[0]].length;
    if ((j - 1) < colNum) {
        var i;
        for (i = colNum; i < j - 1; i++) {
            resultDataTable.addColumn({type: 'number', label: 'Data Column ' + i.toString()});
        }
    }

    $.each(componentData['data'], function (index, row) {
        var r = [];
        var dt = index.split(' ');
        var d = dt[0].split('-');
        r.push(new Date(d[0], d[1] - 1, d[2], dt[1], 0, 0, 0));

        $.each(row, function (key, value) {
            r.push(parseFloat(value));
        });
        if (r.length < j - 1) {
            var k;
            for (k = r.length; k < j - 1; k++) {
                r.push(0.0);
            }
        }
        console.log(r);
        resultDataTable.addRow(r);
    });
    var chart = new google.visualization.LineChart(document.getElementById("output_data"));
    chart.draw(resultDataTable, chartOption);
    return false;
}

function setDataGraph2() {
    var dataTitle = componentData.dataset;
    var sourceTitle = componentData.dataSource.toUpperCase();

    var labels = [];
    var maxColumns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];
    $.each(maxColumns, function (v) {
        var testKey = "column_" + v.toString();
        if (testKey in componentData.metadata) {
            labels.push(componentData.metadata[testKey]);
        }
    });
    var dataCSV = [];
    var graphOptions = {
        labels: labels,
        title: dataTitle + ": " + sourceTitle + " Data",
        legend: 'always',
        showRangeSelector: true,
        width: 600
    };
    $.each(componentData['data'], function (index, row) {
        if (row.length + 1 === labels.length) {
            var rowD = [];
            var dt = index.split(' ');
            var d = dt[0].split('-');
            var date;
            if (dt.length === 2) {
                var hr = dt[1].split(':');
                if (hr.length === 2) {
                    date = new Date(d[0], d[1] - 1, d[2], hr[0], hr[1], 0, 0);
                }
                else {
                    date = new Date(d[0], d[1] - 1, d[2], dt[1], 0, 0, 0);
                }
            }
            else {
                date = new Date(d[0], d[1] - 1, d[2], 0, 0, 0);
            }
            rowD.push(date);
            $.each(row, function (key, value) {
                var datapoint = parseFloat(value);
                if(datapoint === -9999 || datapoint === -9998){
                    datapoint = -1;
                }
                rowD.push(datapoint);
            });
            dataCSV.push(rowD);
        }
    });
    var graphEle = document.getElementById('output_data');
    dyGraph = new Dygraph(graphEle, dataCSV, graphOptions);
}


function toggleLoader(hide, msg) {
    if (hide) {
        $("#output_loading").fadeOut(100);
        $("#loading_msg").html();
    }
    else {
        $("#output_loading").fadeIn(100);
        $("#loading_msg").html("<span>" + msg + "</span>");
    }
    return false;
}

function toggleDownloadButtons(hide){
    if(hide){
        $("#output_data_save_block").hide();
    }
    else{
        $("#output_data_save_block").show();
    }
}

function exportDataToJSON() {
    var fileName = componentData.dataset + "_" + componentData.dataSource + ".json";
    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(componentData)));
    pom.setAttribute('download', fileName);
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

function exportDataToCSV() {
    var fileName = componentData.dataset + "_" + componentData.dataSource;
    var metadata = "";
    $.each(componentData.metadata, function (k, v) {
        metadata += k + "," + v + "\n";
    });
    var columns = "Date";
    var c_index = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];
    $.each(c_index, function (v) {
        if (componentData.metadata["column_" + v] && componentData.metadata["column_" + v].toLowerCase().includes("date")){
            columns = componentData.metadata["column_" + v];
        }
        else if (componentData.metadata["column_" + v] && !componentData.metadata["column_" + v].toLowerCase().includes("date")) {
            if(componentData.metadata["column_" + v + "_units"]){
                columns += "," + componentData.metadata["column_" + v] + "(" + componentData.metadata["column_" + v + "_units"] + ")";
            }
            else {
                columns += "," + componentData.metadata["column_" + v];
            }
        }
    });
    var data = "";
    $.each(componentData.data, function (k, v) {
        data += k;
        $.each(v, function (j, w) {
            data += "," + w;
        });
        data += "\n";
    });

    var metadata_name = fileName + "_metadata.json";
    exportDataAsJSON(metadata_name, componentData.metadata);

    var csvFinal = columns + "\n" + data;
    var dataStr = 'data:data:text/csv;charset=utf-8,' + encodeURIComponent(csvFinal);
    var pom = document.createElement('a');
    pom.setAttribute('href', dataStr);
    pom.setAttribute('download', fileName + '.csv');
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

function exportDataAsJSON(name, output){
    var pom = document.createElement('a');
    var data = encodeURIComponent(JSON.stringify(output));
    pom.setAttribute('href', 'data:data:text/plain;charset=utf-8,' + data);
    pom.setAttribute('download', name);
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

function loadCookies(){
    var url = window.location.href.split('/');
    var model = $("#model_name").html();
    var submodule = $("#submodule_name").html();
    url = url[2] + "/hms/" + model + "/" + submodule;
    var cookie = getCookie(url);
    cookie = pruneCookieTasks(cookie);
    var ids = cookie.split(",");
    if( ids.length > 1){
        $("#previous_tasks").show();
        var list = $('#previous_tasks_list')[0];
        ids.forEach(function(id){
            if(id !== "") {
                var id_time = id.split(':');

                var eleID = document.createElement("span");
                eleID.innerText = id_time[0];
                eleID.className = "previous_task_id";
                eleID.setAttribute("title", "Task ID");
                eleID.onclick = function () {
                    getPreviousDataFromID(id_time[0]);
                };

                var eleT = document.createElement("span");
                var d = new Date(parseInt(id_time[1]));
                eleT.innerText = d.toLocaleString();
                eleT.className = "previous_task_time";
                eleT.setAttribute("title", "Task Timestamp");

                var ele = document.createElement("li");
                ele.className = "previous_task";
                ele.appendChild(eleID);
                ele.appendChild(eleT);
                list.appendChild(ele);
            }
        });
    }
}

function setDataRequestCookie(taskID){
    var daysToExpire = 1;
    var date = new Date();
    date.setTime(date.getTime() + daysToExpire * 24*60*60*1000);
    var expires = "expires=" + date.toUTCString();
    var timestamp = new Date();
    var taskIDs = taskID + ":" + timestamp.getTime();
    var url = window.location.href.split('/');
    var model = $("#model_name").html();
    var submodule = $("#submodule_name").html();
    url = url[2] + "/hms/" + model + "/" + submodule;
    var current = getCookie(url);
    current = pruneCookieTasks(current);
    var ids = "";
    $.each(current.split(','), function(index, value){
        var id = value.split(':')[0];
        if(id !== taskID && id !== ""){
            ids += "," + value;
        }
        else if(id === taskID){
            taskIDs = value;
        }
    });

    taskIDs = taskIDs + ids;
    document.cookie = url+  "=" + taskIDs + ";" + expires + ";path=" + "/hms/" + model + "/" + submodule + "/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function pruneCookieTasks(currentTasks){
    var IDs = currentTasks.split(',');
    var taskIDs = "";
    var now = new Date();
    now.setDate(now.getDate() - 1);
    now = now.getTime();
    $.each(IDs, function(k, v){
        if(v !== "") {
            var timestamp = new Date();
            if (v.includes(":")) {
                var id_t = v.split(':');
                timestamp.setTime(parseInt(id_t[1]));
                if (timestamp.getTime() > now) {
                    taskIDs = taskIDs + "," + v;
                }
            } else {
                taskIDs = taskIDs + "," + v + ":" + timestamp.getTime();
            }
        }
    });
    return taskIDs;
}

function deleteTaskFromCookie(id){
    var url = window.location.href.split('/');
    var model = $("#model_name").html();
    var submodule = $("#submodule_name").html();
    url = url[2] + "/hms/" + model + "/" + submodule;
    var current = getCookie(url);
    current = pruneCookieTasks(current);
    var IDs = current.split(',');
    var validIDs = [];
    $.each(IDs, function(k, v){
        if(v.includes(":")){
            var i = v.split(':');
            if(i[0] !== id){
                validIDs.push(v);
            }
        }
    });
    var daysToExpire = 1;
    var date = new Date();
    date.setTime(date.getTime() + daysToExpire * 24*60*60*1000);
    var expires = "expires=" + date.toUTCString();
    var taskIDs = validIDs.join();
    document.cookie = url+  "=" + taskIDs + ";" + expires + ";path=" + "/hms/" + model + "/" + submodule + "/";
}
