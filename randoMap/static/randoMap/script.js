

function getClientHeight(){
	if (document.body) {
		var cliHeight = (document.body.clientHeight);
	} else {
		var cliHeight = (window.innerHeight);
	};
	cliHeight = cliHeight*70/100;
	return cliHeight.toString() + 'px';
}


function displayCampingName(camping_name){
	$("#campingName").empty().append(camping_name);
}

function displayCampingAddress(camping_address){
	$("#campingAddress").empty().append(camping_address);
}

function displayCampingRating(camping_rating=0, total_rating=0, default_message=""){
	if (camping_rating != 0 && total_rating != 0){
		var phrase = camping_rating+"/5 ("+total_rating+" votes)" 
	} else { var phrase = default_message };
	$("#googleRating").empty().append(phrase);
};

function displayCampingPhone(camping_phone) {
	var HTMLToInsert = '<a href="tel:'+camping_phone+'">'+camping_phone+'</a>';
	$("#campingPhone").empty().append(HTMLToInsert);
}

function displayCampingWebsite(camping_website) {
	$('#campingWebsite').empty().append(camping_website).attr('href', camping_website);
}

function displayGoogleReviews(googleReviews) {
	$('#googleReviews').empty();
	for (var review in googleReviews) {
		if (typeof(googleReviews[review]['text']) == 'string') {
			var texteAInserer = '<p>'+googleReviews[review]['text']+'</p>'
			$('#googleReviews').append(texteAInserer);
		}
	};
}

function displayOpeningHours(openings){
	if (openings['periods']) {
		var date = new Date();
		var day = date.getDay()-1;
		if (day === -1) { day = 6 };
		var today_openings = openings['periods'][day];
		var a_afficher = "<p>Ouverture : " + today_openings['open']['time'][0] + today_openings['open']['time'][1]  + "H      Fermeture : " + today_openings['close']['time'][0] + today_openings['close']['time'][0] + "H</p>";
		return a_afficher
	} else {
		return "<p>Horaires non renseignés</p>"
	};

}

function getPhotos(camp_id){
	$.post(
		'getphotos/',
		{
			csrfmiddlewaretoken: "{{ csrf_token }}",
			camping_id : camp_id

		},
		function(photo, statut){
			$('#ItemPreview').attr('src', `data:image/png;base64,${photo}`);
		}
		)
}

function displayAllCampingDetails(camping_details) {
	var camping = new Map();
	if (camping_details['name']) {
		camping.set('name', camping_details['name'])
	} else { camping.set("name", "Aucun nom disponible") };
	if (camping_details['formatted_address']) {
		camping.set("address", camping_details['formatted_address'])
	} else { camping.set("address", "Aucune adresse disponible") };
	if (camping_details['rating'] && camping_details['user_ratings_total']) {
		camping.set("rating", camping_details['rating'].toString());
		camping.set("total_rating", camping_details['user_ratings_total'].toString())
	} else { camping.set("rating", '0'); camping.set("total_rating", '0') };
	if (camping_details['formatted_phone_number']) {
		camping.set("phone_number", camping_details['formatted_phone_number'])
	} else { camping.set("phone_number", 'Aucun numéro de téléphone renseigné') };
	if (camping_details['website']) {
		camping.set("website", camping_details['website'])
	};
	if (camping_details['opening_hours']) {
		camping.set("openings", camping_details['opening_hours'])
	};
	if (camping_details["distance"]){
		camping.set("distance", camping_details["distance"]);
	};
	if (camping_details["devPositif"]){
		camping.set("devPositif", camping_details["devPositif"])
	};
	if (camping_details["devNegatif"]) {
		camping.set("devNegatif", camping_details["devNegatif"])
	}
	
	if (L.DomUtil.get(id="divCampingInfos") != null) {
		command.remove();	
	};
	
	command = L.control({position: 'topright'});
	command.onAdd = function (macarte) {
    	var div = L.DomUtil.create('div', 'command');
    	div.setAttribute('id', 'divCampingInfos');
    	div.innerHTML += "<p>"+ camping.get('name') + "</p>";
    	div.innerHTML += "<p>"+ camping.get('address') + "</p>";
    	div.innerHTML += "<p>"+ camping.get('rating') + "/" + "5 (" + camping.get('total_rating') + " notes)" + "</p>";
    	if (camping.get("distance")) {
    		div.innerHTML += '<p>Distance : ' + camping.get("distance") + "</p>"
    	};
    	if (camping.get('devPositif')) {
    		div.innerHTML += "<p>  D+ : " + camping.get('devPositif') + "m" + "   D- : " + camping.get('devNegatif') + "m" + "</p>"
    	} 
    	if (camping.get('openings')) {
    		div.innerHTML += displayOpeningHours(camping.get('openings'));
    	} else {
    		div.innerHTML += "<p>Aucun horaire renseigné</p>"
    	};
    	if ( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    		div.innerHTML += '<p><a href="tel:'+ camping.get('phone_number') +'">'+ camping.get('phone_number') +'</a></p>'
    	} else {
    		div.innerHTML += '<p>' + camping.get('phone_number') + '</p>'
    	};
    	if (camping.get("website")) {
    		div.innerHTML += "<p><a href='" + camping.get("website") + "'>" + camping.get('website') + "<a></p>";
    	} else {
    		div.innerHTML += "<p>Aucun site web renseigné</p>"
    	};
    	
    
    return div;
	};
	command.addTo(macarte);
	}


function displayAllPlaceDetails(place_details) {
	var place = new Map();
	if (place_details['name']) {
		place.set('name', place_details['name'])
	} else { place.set("name", "Aucun nom disponible") };
	if (place_details['formatted_address']) {
		place.set("address", place_details['formatted_address'])
	} else { place.set("address", "Aucune adresse disponible") };
	if (place_details['rating'] && place_details['user_ratings_total']) {
		place.set("rating", place_details['rating'].toString());
		place.set("total_rating", place_details['user_ratings_total'].toString())
	} else { place.set("rating", '0'); place.set("total_rating", '0') };
	if (place_details['formatted_phone_number']) {
		place.set("phone_number", place_details['formatted_phone_number'])
	} else { place.set("phone_number", 'Aucun numéro de téléphone renseigné') };
	if (place_details['website']) {
		place.set("website", place_details['website'])
	};
	if (place_details['opening_hours']) {
		place.set("openings", place_details['opening_hours'])
	};
	if (place_details["distance"]){
		place.set("distance", place_details["distance"]);
	};
	if (place_details["devPositif"]){
		place.set("devPositif", place_details["devPositif"])
	};
	if (place_details["devNegatif"]) {
		place.set("devNegatif", place_details["devNegatif"])
	}
	
	if (L.DomUtil.get(id="divCampingInfos") != null) {
		command.remove();	
	};
	
	command = L.control({position: 'topright'});
	command.onAdd = function (macarte) {
    	var div = L.DomUtil.create('div', 'command');
    	div.setAttribute('id', 'divCampingInfos');
    	div.innerHTML += "<p>"+ place.get('name') + "</p>";
    	div.innerHTML += "<p>"+ place.get('address') + "</p>";
    	div.innerHTML += "<p>"+ place.get('rating') + "/" + "5 (" + place.get('total_rating') + " notes)" + "</p>";
    	if (place.get("distance")) {
    		div.innerHTML += '<p>Distance : ' + place.get("distance") + "</p>"
    	};
    	if (place.get('devPositif')) {
    		div.innerHTML += "<p>  D+ : " + place.get('devPositif') + "m" + "   D- : " + place.get('devNegatif') + "m" + "</p>"
    	} 
    	if (place.get('openings')) {
    		div.innerHTML += displayOpeningHours(place.get('openings'));
    	} else {
    		div.innerHTML += "<p>Aucun horaire renseigné</p>"
    	};
    	if ( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    		div.innerHTML += '<p><a href="tel:'+ place.get('phone_number') +'">'+ place.get('phone_number') +'</a></p>'
    	} else {
    		div.innerHTML += '<p>' + place.get('phone_number') + '</p>'
    	};
    	if (place.get("website")) {
    		div.innerHTML += "<p><a href='" + place.get("website") + "'>" + place.get('website') + "<a></p>";
    	} else {
    		div.innerHTML += "<p>Aucun site web renseigné</p>"
    	};
    	
    
    return div;
	};
	command.addTo(macarte);
};

//Création du panneau de contrôle
panneau = L.control({position: 'topleft'});
panneau.onAdd = function (macarte) {
	var div = L.DomUtil.create('div', 'command');
	all_places_types.forEach(function(place_type){
		div.innerHTML += '<p><form><input id="' + place_type + '" type="checkbox" />' + place_type.capitalize() + '</form></p>';
	});
	return div
	};


function onMapClick(e) {
	if (L.DomUtil.get(id="divPlaceInfos") != null) {
		command.remove();	
	};
};

function onMapMove(e) {
	if (L.DomUtil.get(id="divPlaceInfos") != null) {
		command.remove();	
	};
	all_places_types.forEach(function(place_type){
		if ($('#'+place_type).is(':checked')){ getPlaces(place_type) };
	});
};

function displayOrNotDisplay(){
	if (this.checked) {
		getPlaces(this.id);
	} else {
		macarte.removeLayer(all_markers[this.id]);
	}
}



function initMap(userLoc) {
	// Création une variable avec les coordonnées de l'utilisateur
	// Créer l'objet "macarte" et l'insèrer dans l'élément HTML qui a l'ID "map"
    macarte = L.map('map').setView(userLoc, 12);
    // Leaflet ne récupère pas les cartes (tiles) sur un serveur par défaut. Nous devons lui préciser où nous souhaitons les récupérer. Ici, openstreetmap.fr
   	L.tileLayer('https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=3bbb3f952f5e433b8eedf4cec24fbb18', {
        // Il est toujours bien de laisser le lien vers la source des données
        attribution: 'données © <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
        minZoom: 1,
        maxZoom: 20
    }).addTo(macarte);
	panneau.addTo(macarte)
   	L.marker(userLoc, {icon: veloIcon}).addTo(macarte);
   	//getcampings();
   	macarte.on('moveend', onMapMove);
   	macarte.on('click', onMapClick);
   	document.getElementById('camping').addEventListener("click", displayOrNotDisplay, false);
   	document.getElementById('grocery').addEventListener("click", displayOrNotDisplay, false);	
}