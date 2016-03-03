function initMap() {
    console.log("initing map");
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 41.854, lng: -87.709},
        zoom: 10
    });
    console.log("map init complete");
    drawMarkers();
}   

function drawMarkers() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/data/markers", true)
    xhttp.send();
    console.log("sent request");
    xhttp.onreadystatechange = function() {
        console.log("readyState change");

        if (xhttp.readyState == 4 && xhttp.status == 200) {
            console.log(xhttp.response)
        }
        else {
            console.error("erorr " + xhttp.status + "occurred at state " + xhttp.readyState);
        }
    }
}