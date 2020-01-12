var DEFAULT_URL = "https://2b9bd382.ngrok.io/smartsoles";

function sendData(fsrData) {
    
    console.log(fsrData);
    var rows = fsrData.split("\n");

    var payload = [];
    for(var i = 0; i < rows.length; i++) {
        if (rows[i].length < 2) {
            continue;
        }

        payload.push(rows[i].split(" "));
    }

    console.log(payload);

    var data = {
        "data": [ payload ]
    };

    function postAjax(url, data) {
    
        var xhr = new XMLHttpRequest();
        xhr.open('post', url);
        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log("Success");
                console.log(xhr.responseText);
            } else {
                console.log("Error");
                console.log(xhr.responseText);
            }
        }

        xhr.send(JSON.stringify(data));

        console.log(data);

        return xhr;
    }

    var url = document.getElementById("url").value;
    if (url == null || url.length < 5) {
        url = DEFAULT_URL;
    }

    postAjax(url, data);
}