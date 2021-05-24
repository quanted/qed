var jobid = window.location.pathname.split("/").pop();

$(document).ready(function () {
    checkJobExists()
});


function checkJobExists(){
    var statusUrl = "/nta/status/" + jobid;
    //console.log("Process check # :" + attemptCount);
    $.ajax({
        url: statusUrl,
        type: "GET",
        cache: false,
        success: function(data, status, jqXHR) {
            if('status' in data) {
                if (data['status'] === "Not found") {
                    errorDisplay();
                }
                else if(data['status'].startsWith("Failed")){
                    var message = data['status'];
                    var error_info = data['error_info'];
                    $('#download_area').html(message);
                    $('#except_info').html("Error info: "+ error_info);
                }
            }
            else{
                console.log("Error: No status in response!");
                errorDisplay();
            }
        },
        error: function(jqXHR, status){
            console.log("Error contacting status server.");
            errorDisplay();
        },
        complete: function(jqXHR, status) {
            return false;
        }
    })
}


function errorDisplay(){
    $('#download_area').html("<h3> Error: NTA task not found! </h3>");
}