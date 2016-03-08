function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 41.854, lng: -87.709},
        zoom: 10
    });
    map.infoWindow = new google.maps.InfoWindow();
    window.addEventListener("mapReady", createMarkers);
    window.dispatchEvent(new CustomEvent("mapReady"));
    initRouteSelector();
}

function initRouteSelector() {
    var routes = document.getElementsByTagName("td");
    for (var i = 0; i < routes.length; i++) {
        routes[i].addEventListener("click", changeRoute);
    } 
}   

function changeRoute() {
    var oldRoute = document.getElementsByClassName("selected")[0];  
    oldRoute.classList.remove("selected");
    this.classList.add("selected");

    var routeName = this.dataset.routeId;
    if (routeName === "all") {
        showAll();
    }
    else {
        showOnly(routeName);
    }
}

function showOnly(routeName) {
    for (var route of map.routes) {
        if (routeName !== route[0]) {
            route[1].forEach( function(markerId) {
                map.markers.get(markerId).setMap(null);
            });
        }
    }

    map.routes.get(routeName).forEach( function(markerId) {
        map.markers.get(markerId).setMap(map);
    });
}

function showAll() {
    for (var marker of map.markers.values()) {
        marker.setMap(map);
    }    
}

function createMarkers() {
    map.markers = new Map();
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
    map.markers.set(stop[0], marker);
    addToRoutes(stop[2], stop[0]);
}

function addToRoutes(routes, markerId) {
    routes.forEach( function(route) {
        route = route.toString();
        if (!map.routes.has(route)) {
            map.routes.set(route, []);
        }
        var stops = map.routes.get(route);
        stops.push(markerId);
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
