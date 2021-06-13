const latitude = 50.929896199999995;
const longitude = -1.3922295999999998;

var myLocation = new google.maps.LatLng(latitude, longitude);

function initialize(){
    var mapOptions = {
        center: myLocation,
        zoom: 8,
    };
    var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
    var marker = new google.maps.Marker({
        position: myLocation,
        title: "Address"
    });
    marker.setMap(map);
}
google.maps.event.addDomListener(window, "load", initialize);