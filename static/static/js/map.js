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

var iconos = [yellowIcon, greenIcon, redIcon, orangeIcon, purpleIcon];

function MapHandler(categorias, marcadores, latitud, longitud, mapId, map, catastrophe) {
    this.categorias = categorias;
    this.marcadores = marcadores;
    this.latitud = latitud;
    this.longitud = longitud;
    this.mapId = mapId;
    this.map = map
    this.catastrophe = catastrophe
    this.loadMap = function(){

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

        
        /*
        //crear mapa
        var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
                //attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
            }),
            latlng = L.latLng(this.latitud, this.longitud);

        var map = L.map(this.mapId, {
            center: latlng,
            zoom: 15,
            layers: [tiles]
        });
        */
        //marcadores
        var markers = L.markerClusterGroup();


        
        function cargarTodos(marcadores){
            markers.clearLayers();
            console.log(marcadores)
            for (var i = 0; i < marcadores.length; i++) {
                if(catastrophe == i+1) {
                    console.log(marcadores[i].length)
                    for (var j = 0; j < marcadores[i].length; j++) {
                        if (marcadores[i][j].length > 0) {
                            for (var k = 0; k<marcadores[i][j].length; k++) {
                                var markerAux = L.marker([marcadores[i][j][k].fields.latitud, marcadores[i][j][0].fields.longitud], {
                                    icon: iconos[i]
                                });
                                markerAux.bindPopup(marcadores[i][j][k].fields.description);
                                markers.addLayer(markerAux);
                            }
                        }
                    }
                }
            }
        }

        cargarTodos(this.marcadores);

        this.map.addLayer(markers);

        //mostrar dialogo
        var estaPresionado = false;
        var mostrarDialogo = function(e) {
            $("#latitud").val(e.latlng.lat);
            $("#longitud").val(e.latlng.lng);
            $("#id-map").val(mapId);
            jQuery.fn.block();
            $("#dialog").center()
                .fadeIn();
            estaPresionado = false;
        }

        //eventos para crear marcador


        this.map.on('mousedown', function(e) {
            estaPresionado = true;
            clearTimeout(this.downTimer);
            this.downTimer = setTimeout(mostrarDialogo, 1000, e);

        });

        this.map.on('mouseup', function(e) {
            estaPresionado = false;
            clearTimeout(this.downTimer);

        });

        //mousemove event

        $(this.mapId).mousemove(function(event) {
            clearTimeout(this.downTimer);
            this.downTimer = setTimeout(1000);
            if (estaPresionado) {
                this.downTimer = setTimeout(mostrarDialogo, 1000);
            }
        });

    }
}


function init_map(json_str,id,map,catastrophe) {

    var mapHandler = new MapHandler(
            "",
            jQuery.parseJSON(json_str),
            -41.77, 
            -73.134,
            id,
            map,
            catastrophe
        )

    mapHandler.loadMap();

    //filtrar
    $("button.filtro").click(function(){
        var categoria = $(this).attr('categoria') - 1;
        markers.clearLayers();
        for(var j = 0; j < marcadores[categoria].length; j++){
            var markerAux = L.marker([marcadores[categoria][j].fields.latitud, marcadores[categoria][j].fields.longitud], {
                icon: iconos[categoria]
            });
            markerAux.bindPopup(marcadores[categoria][j].fields.description);
            markers.addLayer(markerAux);
        }
    });

    //$("#todos").click(cargarTodos);


}