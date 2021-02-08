// pdf report request sent to server


function generateReport(){
    var community_scores = hwbi_disc_data;
    var indicators = hwbi_indicator_data;
    var adjusted_scores = hwbi_indicator_value_adjusted;
    var report_data = JSON.stringify(
        {
            'community_scores': community_scores,
            'indicators': indicators,
            'adjusted_scores': adjusted_scores
        });
    var csrf_token = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url: '/hwbi/disc/rest/report/',
        headers: {
          'X-CSRFToken': csrf_token
        },
        xhrFields: {
            responseType: 'blob'
        },
        data: report_data,
        success: function (data, status, xhr) {
            console.log('DISC Report created successfully');
            var a = document.createElement('a');
            var url = window.URL.createObjectURL(data);
            a.href = url;
            a.download = 'disc-report.pdf';
            a.click();
            window.URL.revokeObjectURL(url);
        },
        error: function (jqXHR, textStatus, errorThrown)
        {
            console.log('DISC Report creation fail. Error: ' + errorThrown);
        },
        complete: function (jqXHR, textStatus) {
            console.log('DISC Report completed: ' + textStatus);
            return false;
        }
        });


}

