function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 41.854, lng: -87.709},
        zoom: 10
    });
    console.log("map init complete");
    var mapReady = new CustomEvent("mapReady");
    window.dispatchEvent(mapReady);
}   

function drawMarkers() {
    console.log("drawing markers");
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/data/markers", true)
    xhttp.send();
    console.log("sent request");
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4) {
            if (xhttp.status == 200) {
                console.log("recieved data");
            }
            else {
                console.error("erorr " + xhttp.status);
            }
        }
    }
}