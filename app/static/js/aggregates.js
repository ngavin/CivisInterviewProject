document.addEventListener('DOMContentLoaded', loadData);

function loadData() {
    var aggregates = document.getElementsByClassName("load");

    for (var i = 0; i < aggregates.length; i++) {
        getAggregate(aggregates[i])
    }
}

function getAggregate(agg) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/data/aggregates/" + agg.getAttribute("id"), true)
    xhttp.send();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            agg.innerHTML = xhttp.responseText;
        }
    }
}
