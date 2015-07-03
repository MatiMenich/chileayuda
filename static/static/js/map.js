// centrar
jQuery.fn.center = function() {
	this.css("position", "absolute");
	this.css("top", Math.max(0,
			(($(window).height() - $(this).outerHeight()) / 3)
					+ $(window).scrollTop())
			+ "px");
	this.css("left", Math.max(0,
			(($(window).width() - $(this).outerWidth()) / 2)
					+ $(window).scrollLeft())
			+ "px");
	return this;
}

// block screen
jQuery.fn.block = function() {
	$("#screen").css({
		"display" : 'block',
		opacity : 0.7,
		'width' : $(document).width(),
		'height' : $(document).height()
	});
	$('body').css({
		'overflow' : 'hidden'
	});
}

// iconos para marcadores
var yellowIcon = L.icon({
	iconUrl : 'static/js/images/Icon_y.png',
	shadowUrl : 'static/js/images/marker-shadow.png',

	iconSize : [ 25, 41 ], // size of the icon
	shadowSize : [ 41, 41 ], // size of the shadow
	iconAnchor : [ 12.5, 41 ], // point of the icon which will correspond to
	// marker's location
	shadowAnchor : [ 13, 41 ], // the same for the shadow
	popupAnchor : [ -3, -76 ]
// point from which the popup should open relative to the iconAnchor
});

var redIcon = L.icon({
	iconUrl : 'static/js/images/Icon_r.png',
	shadowUrl : 'static/js/images/marker-shadow.png',

	iconSize : [ 25, 41 ], // size of the icon
	shadowSize : [ 41, 41 ], // size of the shadow
	iconAnchor : [ 12.5, 41 ], // point of the icon which will correspond to
	// marker's location
	shadowAnchor : [ 13, 41 ], // the same for the shadow
	popupAnchor : [ -3, -76 ]
// point from which the popup should open relative to the iconAnchor
});

var orangeIcon = L.icon({
	iconUrl : 'static/js/images/Icon_o.png',
	shadowUrl : 'static/js/images/marker-shadow.png',

	iconSize : [ 25, 41 ], // size of the icon
	shadowSize : [ 41, 41 ], // size of the shadow
	iconAnchor : [ 12.5, 41 ], // point of the icon which will correspond to
	// marker's location
	shadowAnchor : [ 13, 41 ], // the same for the shadow
	popupAnchor : [ -3, -76 ]
// point from which the popup should open relative to the iconAnchor
});

var purpleIcon = L.icon({
	iconUrl : 'static/js/images/Icon_p.png',
	shadowUrl : 'static/js/images/marker-shadow.png',

	iconSize : [ 25, 41 ], // size of the icon
	shadowSize : [ 41, 41 ], // size of the shadow
	iconAnchor : [ 12.5, 41 ], // point of the icon which will correspond to
	// marker's location
	shadowAnchor : [ 13, 41 ], // the same for the shadow
	popupAnchor : [ -3, -76 ]
// point from which the popup should open relative to the iconAnchor
});

var greenIcon = L.icon({
	iconUrl : 'static/js/images/Icon_g.png',
	shadowUrl : 'static/js/images/marker-shadow.png',

	iconSize : [ 25, 41 ], // size of the icon
	shadowSize : [ 41, 41 ], // size of the shadow
	iconAnchor : [ 12.5, 41 ], // point of the icon which will correspond to
	// marker's location
	shadowAnchor : [ 13, 41 ], // the same for the shadow
	popupAnchor : [ -3, -76 ]
// point from which the popup should open relative to the iconAnchor
});

var iconos = [ yellowIcon, greenIcon, redIcon, orangeIcon, purpleIcon ];

function MapHandler(marcadores, latitud, longitud, map, mapId, catastrophe) {
	this.marcadores = marcadores;
	this.latitud = latitud;
	this.longitud = longitud;
	this.map = map;
	this.mapId = mapId;
	this.catastrophe = catastrophe;
	this.markers = L.markerClusterGroup();
	this.loadAll = function(placeHolder, marcadores) {
		placeHolder.markers.clearLayers();
		for (var i = 0; i < placeHolder.marcadores.length; i++) {
			for (var j = 0; j < placeHolder.marcadores[i].length; j++) {
				var markerAux = L.marker([
						placeHolder.marcadores[i][j].fields.latitud,
						placeHolder.marcadores[i][j].fields.longitud ], {
					icon : iconos[i]
				});
				markerAux
						.bindPopup(placeHolder.marcadores[i][j].fields.description);
				this.markers.addLayer(markerAux);
			}
		}
	}
	this.loadByCategory = function(placeHolder, category) {
		placeHolder.markers.clearLayers();
		for (var j = 0; j < placeHolder.marcadores[category].length; j++) {
			var markerAux = L.marker([
					placeHolder.marcadores[category][j].fields.latitud,
					placeHolder.marcadores[category][j].fields.longitud ], {
				icon : iconos[category]
			});
			markerAux.bindPopup(marcadores[category][j].fields.description);
			placeHolder.markers.addLayer(markerAux);
		}
	}
	this.loadMap = function() {

		var placeHolder = this;

		// form
		$("#dialog").css('box-shadow', '0px 0px 2px 3px #000').css('height',
				$(".content-dialog").height()).css('z-index', 1001).hide();

		$("#cerrar").click(function() {

			$("#dialog").fadeOut(400, function() {
				$(window).css('display', 'none');
				$('#screen').css('display', 'none');
			});

		});

		this.loadAll(placeHolder, this.marcadores);
		this.map.addLayer(this.markers);

		// mostrar dialogo
		var estaPresionado = false;
		var eventoMostrarDialogo;
		var mostrarDialogo = function(e) {

			$("#latitud").val(eventoMostrarDialogo.latlng.lat);
			$("#longitud").val(eventoMostrarDialogo.latlng.lng);
			$("#id-map").val(mapId);
			jQuery.fn.block();
			$("#dialog").center().fadeIn();
			estaPresionado = false;
		}

		// eventos para crear marcador
		this.map.on('mousedown', function(e) {
			estaPresionado = true;
			eventoMostrarDialogo = e;
			if ($("#actual-catastrophe")[0].value != mapId.substring(3)) {
				$("#actual-catastrophe").val(mapId.substring(3));
				delete_select_form();
				update_select_form();
			}
			clearTimeout(this.downTimer);
			this.downTimer = setTimeout(mostrarDialogo, 1000, e);

		});

		this.map.on('mouseup', function(e) {
			estaPresionado = false;
			clearTimeout(this.downTimer);

		});

		// mousemove event
		$(this.map).mousemove(function(event) {
			clearTimeout(this.downTimer);
			this.downTimer = setTimeout(1000);
			if (estaPresionado) {
				this.downTimer = setTimeout(mostrarDialogo, 1000, null);
			}
		});

		$("button.all." + catastrophe).click(function() {
			placeHolder.loadAll(placeHolder, $(this).attr('categoria'));
		});

		$("button.filtro." + catastrophe).click(function() {
			placeHolder.loadByCategory(placeHolder, $(this).attr('categoria'));
		});
	}
}

function init_map(json_str, cat_str) {

	var allData = jQuery.parseJSON(json_str);
	var catData = jQuery.parseJSON(cat_str);

	for (var i = 0; i < allData.length; i++) {
		var mapId = "map" + (i + 1);
		var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
			maxZoom : 18,
		}), latlng = L.latLng(catData[i][0].fields.latitud, catData[i][0].fields.longitud);
		var map = L.map(mapId, {
			center : latlng,
			zoom : 15,
			layers : [ tiles ]
		});
		var mapHandler = new MapHandler(allData[i], catData[i][0].fields.latitud, catData[i][0].fields.longitud, map,
				mapId, i)
		mapHandler.loadMap();
	}
}