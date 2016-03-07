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
    map.routes = new Map();
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
    var latLng = stop[1].replace(/[()]/g, "").split(",");
    var marker = new google.maps.Marker({
        position: {lat: parseFloat(latLng[0]), lng: parseFloat(latLng[1])},
        title: stop[0].toString(),
        map: map
    });
    marker.addListener("click", displayInfoWindow);
    map.routes.set(stop[0], marker)
    // addToRoutes(stop[2], marker);
}

function addToRoutes(routes, marker) {
    routes.forEach(function(route) {
        if (!map.routes.has(route)) {
            map.routes.set(route, []);
        }
        var stops = map.routes.get(route);
        stops.push(marker);
        map.routes.set(route, stops);
    });
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
            map.infoWindow.setContent(xhttp.responseText);
        }
    }
}
