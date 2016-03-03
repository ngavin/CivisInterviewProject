function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 41.854, lng: -87.709},
        zoom: 10
    });
    // map.infoWindow = new google.maps.InfoWindow();
    window.addEventListener("mapReady", createMarkers);
    window.dispatchEvent(new CustomEvent("mapReady"));
}   

function createMarkers() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/data/markers", true)
    xhttp.send();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4) {
            if (xhttp.status == 200) {
                var stops = JSON.parse(xhttp.responseText);
                stops.forEach(createMarker);
            }
            else {
                console.error("erorr " + xhttp.status);
            }
        }
    }
}

function createMarker(stop) {
    var marker = new google.maps.Marker({
        position: {lat: parseFloat(stop[1]), lng: parseFloat(stop[2])},
        title: stop[0],
        map: map
    });
    marker.addListener("click", displayInfoWindow, marker);
}

// Need to find a way to access the Marjer object
function displayInfoWindow(e, marker) {
    console.log(marker);
    // console.log(marker.getPosition());
}