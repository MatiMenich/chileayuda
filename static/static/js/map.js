//iconos para marcadores
var yellowIcon = L.icon({
    iconUrl: 'static/js/images/Icon_y.png',
    shadowUrl: 'static/js/images/marker-shadow.png',

    iconSize: [25, 41], // size of the icon
    shadowSize: [41, 41], // size of the shadow
    iconAnchor: [12.5, 41], // point of the icon which will correspond to marker's location
    shadowAnchor: [13, 41], // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});

var redIcon = L.icon({
    iconUrl: 'static/js/images/Icon_r.png',
    shadowUrl: 'static/js/images/marker-shadow.png',

    iconSize: [25, 41], // size of the icon
    shadowSize: [41, 41], // size of the shadow
    iconAnchor: [12.5, 41], // point of the icon which will correspond to marker's location
    shadowAnchor: [13, 41], // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});

var orangeIcon = L.icon({
    iconUrl: 'static/js/images/Icon_o.png',
    shadowUrl: 'static/js/images/marker-shadow.png',

    iconSize: [25, 41], // size of the icon
    shadowSize: [41, 41], // size of the shadow
    iconAnchor: [12.5, 41], // point of the icon which will correspond to marker's location
    shadowAnchor: [13, 41], // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});

var purpleIcon = L.icon({
    iconUrl: 'static/js/images/Icon_p.png',
    shadowUrl: 'static/js/images/marker-shadow.png',

    iconSize: [25, 41], // size of the icon
    shadowSize: [41, 41], // size of the shadow
    iconAnchor: [12.5, 41], // point of the icon which will correspond to marker's location
    shadowAnchor: [13, 41], // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});

var greenIcon = L.icon({
    iconUrl: 'static/js/images/Icon_g.png',
    shadowUrl: 'static/js/images/marker-shadow.png',

    iconSize: [25, 41], // size of the icon
    shadowSize: [41, 41], // size of the shadow
    iconAnchor: [12.5, 41], // point of the icon which will correspond to marker's location
    shadowAnchor: [13, 41], // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});


function init_map(json_str) {

    var iconos = [yellowIcon, greenIcon, redIcon, orangeIcon, purpleIcon];

	//centrar
    jQuery.fn.center = function() {
        this.css("position", "absolute");
        this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 3) +
            $(window).scrollTop()) + "px");
        this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) +
            $(window).scrollLeft()) + "px");
        return this;
    }


    //block screen
    jQuery.fn.block = function(){
        $("#screen").css({
            "display": 'block',
            opacity: 0.7,
            'width': $(document).width(),
            'height': $(document).height()
        });
        $('body').css({
            'overflow': 'hidden'
        });
    }

    //form
    $("#dialog").css('box-shadow', '0px 0px 2px 3px #000')
        .css('height', $(".content-dialog").height())
        .css('z-index', 1001)
        .hide();

    $("#cerrar").click(
        function() {

            $("#dialog").fadeOut(400, function() {
                $(window).css('display', 'none');
                $('#screen').css('display', 'none');
            });

        }
    );

    //crear mapa
    var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            //attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
        }),
        latlng = L.latLng(-41.77, -73.134);

    var map = L.map('map', {
        center: latlng,
        zoom: 15,
        layers: [tiles]
    });

    //marcadores
    var markers = L.markerClusterGroup();


    var marcadores = jQuery.parseJSON(json_str);

    for (var i = 0; i < marcadores.length; i++) {
        for(var j = 0; j < marcadores[i].length; j++){
            var markerAux = L.marker([marcadores[i][j].fields.longitud, marcadores[i][j].fields.latitud], {
                icon: iconos[i]
            });
            markerAux.bindPopup(marcadores[i][j].fields.description);
            markers.addLayer(markerAux);
        }
    }

    map.addLayer(markers);

    //mostrar dialogo
    var estaPresionado = false;
    var mostrarDialogo = function(e) {
        $("#latitud").value = e.latlng.lat;
        $("#longitud").value = e.latlng.lat;
        jQuery.fn.block();
        $("#dialog").center()
            .fadeIn();
        estaPresionado = false;
    }

    //eventos para crear marcador


    map.on('mousedown', function(e) {
        estaPresionado = true;
        clearTimeout(this.downTimer);
        this.downTimer = setTimeout(mostrarDialogo, 1000, e);

    });

    map.on('mouseup', function(e) {
        estaPresionado = false;
        clearTimeout(this.downTimer);

    });

    //mousemove event

    $(map).mousemove(function(event) {
        clearTimeout(this.downTimer);
        this.downTimer = setTimeout(1000);
        if (estaPresionado) {
            this.downTimer = setTimeout(mostrarDialogo, 1000);
        }
    });
}