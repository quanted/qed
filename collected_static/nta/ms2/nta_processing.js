

/*
$(document).ready(function(){
    jobid = window.location.pathname.split("/").pop()
    window.location.href = 'nta/output/'+jobid
});*/


var jobid = window.location.pathname.split("/").pop();
var timeout = 5000; // Timeout length in milliseconds (1000 = 1 second)
var attemptCount = 0;
var maxAttempts = 45;

$(document).ready(function () {
    setTimeout(checkJobStatus, 5000);
});


function checkJobStatus(){
    var statusUrl = "/nta/ms2/status/" + jobid;
    attemptCount += 1;
    //console.log("Process check # :" + attemptCount);
    $.ajax({
        url: statusUrl,
        type: "GET",
        cache: false,
        success: function(data, status, jqXHR) {
            if('status' in data) {
                if (data['status'] === "Completed") {
                    console.log("Task was completed! Redirecting...");
                    var outputUrl = "/nta/ms2/output/" + jobid;
                    //window.location.href = outputUrl;
                    $(location).attr('href', outputUrl);
                }
                else if(data['status'] === "Not found"){
                    $('#status').html("Error: NTA task failed to start!");
                    $('#wait_gif').html("");

                }
                else if(data['status'].startsWith("Failed")){
                    var message = data['status'];
                    var error_info = data['error_info'];
                    $('#status').html(message);
                    $('#wait_gif').html("");
                    $('#except_info').html("Error info: "+ error_info);
                }
                else {
                    console.log("Status: " + data['status']);
                    var progress = parseInt(data['progress']);
                    var max_progress = parseInt(data['n_masses']);
                    console.log(progress);
                    console.log('out of'+ max_progress);
                    var percent_done = Math.round((progress/max_progress)*100);
                    if(percent_done > 99){
                        percent_done = 99
                    }
                    $('#status').html('Processing... '+ percent_done+'% completed');
                    if(attemptCount<maxAttempts){
                        setTimeout(checkJobStatus, timeout);
                    }
                    else{
                       $('#status').html("Error: NTA task timed out!");
                       $('#wait_gif').html("");
                    }

                }
            }
            else{
                console.log("Error: No status in response!");
            }
        },
        error: function(jqXHR, status){
            console.log("Error contacting status server");
        },
        complete: function(jqXHR, status) {
            return false;
        }
    })
}