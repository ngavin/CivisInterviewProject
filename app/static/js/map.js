function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 41.854, lng: -87.709},
        zoom: 10
    });
    map.infoWindow = new google.maps.InfoWindow();
    window.addEventListener("mapReady", createMarkers);
    window.dispatchEvent(new CustomEvent("mapReady"));
}   

function createMarkers() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/data/markers", true)
    xhttp.send();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var stops = JSON.parse(xhttp.responseText);
            stops.forEach(createMarker);
        }
    }
}

function createMarker(stop) {
    var marker = new google.maps.Marker({
        position: {lat: parseFloat(stop[1]), lng: parseFloat(stop[2])},
        title: stop[0],
        map: map
    });
    marker.addListener("click", displayInfoWindow);
}

function displayInfoWindow(e) {
    map.infoWindow.close();
    map.infoWindow.open(map, this);
    getInfoWindowContent(this.title);
}

function getInfoWindowContent(markerID) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/data/markers/infoWindow/" + markerID, true);
    xhttp.send();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            console.log(xhttp.responseText);
            map.infoWindow.setContent(xhttp.responseText);
        }
    }
}
