$(function () {
    var map = L.map('map').setView([47.82289, 35.19031], 12);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6IjZjN' +
        'mRjNzk3ZmE2MTcwOTEwMGY0MzU3YjUzOWFmNWZhIn0.Y8bhBaUMqFiPrDRW9hieoQ', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'mapbox.streets'
    }).addTo(map);

    //==========================
    function getVehiclesLocations(){
        $.getJSON(
            $SCRIPT_ROOT + '/get_user_veh_locations',
            function (data) {
                var allVehPoints=[], i=0, j=0;
                var points = [];
                var dotLayer = new L.multiPolyline([]);
                for ( i=0; i<data.vehicles.length; i++){
                    //console.log(data.vehicles[i].locations);
                    points = [];
                    for (j=0; j<data.vehicles[i].locations.length; j++){
                        //tmp = [data.vehicles[i].locations[j].latitude, data.vehicles[i].locations[j].longitude];
                        tmp = L.latLng(data.vehicles[i].locations[j].longitude, data.vehicles[i].locations[j].latitude);

                        // добавим точку на карту
                        L.circle(tmp, 10).addTo(dotLayer).bindPopup('Vehicle: <strong>' + data.vehicles[i]['name'] +
                            //'</strong><p> ts: ' + data.vehicles[i].locations[j].ts + '</p>'+
                            //'<p> longitude: ' + data.vehicles[i].locations[j].longitude + '</p>'+
                            //'<p> latitude: ' + data.vehicles[i].locations[j].latitude + '</p>'+
                            //'<p> other: ' + data.vehicles[i].locations[j].other + '</p>');

                            '</strong> <br /> ts: ' + data.vehicles[i].locations[j].ts +
                            '<br /> longitude: ' + data.vehicles[i].locations[j].longitude +
                            '<br /> latitude: ' + data.vehicles[i].locations[j].latitude +
                            '<br /> other: ' + data.vehicles[i].locations[j].other);
                        points.push(tmp);
                    }
                    allVehPoints.push(points);
                }
                //console.log(allVehPoints);
                var polyline = new L.multiPolyline(allVehPoints);
                map.addLayer(polyline);
                map.addLayer(dotLayer);
                map.fitBounds(polyline.getBounds());
            }
        );
    }

    // выводим координаты всех маршрутов конкретного пользователя
    getVehiclesLocations();
    //==========================

});