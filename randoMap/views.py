from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from .models import Place
from .forms import CreercompteForm, ConnexionForm, NewPlaceForm, EditPlaceForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import googlemaps
from .myFunctions import generateID
from pprint import pprint

def index(request):
	newPlaceForm = NewPlaceForm()
	editPlaceForm = EditPlaceForm()
	return render(request, 'randoMap/index.html', locals())

def getplaces(request):
	place_type = request.POST.get('place_type')
	#
	#Récupération des lieux avec l'API goole maps
	gmaps = googlemaps.Client(key='') #Création d'un objet googlemaps.Client
	places = gmaps.places_nearby(keyword=place_type,#La recherche places_nearby renvoie l'ensemble des lieux correspondant aux critères dans la zone géographique spécifiée
							location=request.POST.get('coords'),
							radius=20000,
							language='fr',
							type='campground')['results']
	#La recherche places_nearby renvoie un dictionnaire.
	#Les résultats sont stockés dans une liste comprise dans ce dictionnaire sous la clé 'résultats'
	#Création d'un dictionnaire de résultats à renvoyer à l'utilisateur:
	places_dic = {}
	pprint(places)
	#Début du travail sur les données reçues :
	for place in places:
		print('!')
		#Recherche en BDD si le lieu est déjà connu
		#Si ce n'est pas le cas, enregistrement en BDD du nom et de l'id Google du lieu pour faciliter les recherches ultérieures
		if Place.objects.filter(google_id=place['place_id']).exists():
			#Le lieu est connu en BDD
			bdd_place = Place.objects.get(google_id=place['place_id'])
			place = {'geometry':{'location':{'lat':bdd_place.lat, 'lng':bdd_place.lng}},
						}
			places_dic[bdd_place.place_id] = place

		else:
			newSpot = Place(name=place['name'],
								google_id=place['place_id'],
								place_type=place_type,
								lat=place['geometry']['location']['lat'],
								lng=place['geometry']['location']['lng'],
								place_id=int(generateID(13)),)
			newSpot.save()
			print(newSpot.place_id)
			#Ajout du lieux dans le dictionnaires :
			places_dic[newSpot.place_id] = {'geometry':{'location':place['geometry']['location']},
											}
			
	places_response = {'places':places_dic, 'place_type':place_type}
	return JsonResponse(places_response)
	
def getplacedetails(request):
	place_id = request.POST.get('place_id')
	#Création d'un objet googlemaps.Client :
	gmaps = googlemaps.Client(key='')
	"""
	if request.POST.get('local_data') == "true":
		place = Place.objects.get(place_id=place_id)
		details = {'name': place.name,
					'place_type': place.place_type,
					'formatted_address': place.address,
					'formatted_phone_number': place.phone_number,
					'rating': place.rating,
					'user_ratings_total': place.user_ratings_total,
					'website': place.website,
					}
	"""
	#Récupération de l'ID google du lieu dans la BDD :
	google_id = Place.objects.get(place_id=int(place_id)).google_id
	#Demande d'informations détaillée sur le lieu à l'API Place de Google Maps :
	details = gmaps.place(place_id=google_id, language='fr', fields=['name','rating','vicinity','formatted_phone_number','geometry/location/lat','geometry/location/lng','url','opening_hours','user_ratings_total','website'])
	details = details['result']
	#Récupération du type de lieu dans la BDD et insersion dans le dictionnaire details :
	details['place_type'] = Place.objects.get(place_id=int(place_id)).place_type
	"""
	client_address = gmaps.reverse_geocode([request.POST.get('user_lat'), request.POST.get('user_lng')])
	client_address = client_address[0]['formatted_address']
	
	user_coords = request.POST.get('user_lat') + ',' + request.POST.get('user_lng')
	place_coords = str(details['geometry']['location']['lat']) + ',' + str(details['geometry']['location']['lng'])
	#Demande de l'itinéraire à l'API Direction de Google Maps :
	#directions = gmaps.directions(client_address, details['formatted_address'])
	directions = gmaps.directions(user_coords, place_coords, mode='bicycling')
	#distance = directions[0]['legs'][0]['distance']['text']
	details['distance'] = directions[0]['legs'][0]['distance']['text']
	#distance = distance.split(' ')[0]
	#distance = round(float(distance))
	steps = directions[0]['overview_polyline']['points']
	if distance > 1:
		elevation = gmaps.elevation_along_path(steps, distance)
		denivele_positif = 0
		denivele_negatif = 0
		precp = 0
		for p in elevation:
			p = p['elevation']
			if precp != 0:
				dev = p - precp
				if dev > 0:
					denivele_positif += dev
				elif dev < 0:
					denivele_negatif += dev 
			precp = p
	else:
		denivele_positif = 0
		denivele_negatif = 0
	details['devPositif'] = str(round(denivele_positif))
	details['devNegatif'] = str(round(denivele_negatif))
	"""
	return JsonResponse(details)

def participate(request):
	return render(request, 'randoMap/index.html')

def newSpot(request):
	#Enregistrement d'un nouveau lieu proposé par un utilisateur
	place_types = ["CP", "BV", "PT", "GT", "HT"]
	if request.method == 'POST':
		form = NewPlaceForm(request.POST)
		#Vérification que les données reçues sont valides et que le type de lieu est connu
		if (form.is_valid()) and (request.POST['place_type'] in place_types):
				#Création d'une nouvelle instance de Place :
				newSpot = Place(name=form.cleaned_data['name'],
								place_type=request.POST['place_type'],
								lat=request.POST['lat'],
								lng=request.POST['lng'],
								place_id=generateID(10))
				#Enregistrement du nouveau lieu :
				newSpot.save()

	return redirect('index')

def editPlace(request):
	redirect('index')

def connexion(request):
	error = False
	logform = ConnexionForm()
	newusrform = CreercompteForm()

	if request.method == "GET":
		#Demande de la page de connexion
		return render(request, 'randoMap/connexion.html', locals())

	if request.method == "POST":
		#Demande de connexion d'un utilisateur
		form = ConnexionForm(request.POST)
		if form.is_valid():
			user_email = form.cleaned_data["user_email"]
			user_password = form.cleaned_data["user_password"]
			try:
				username = User.objects.get(email=user_email)			
				user = authenticate(username=username.username, password=user_password)  # Nous vérifions si les données sont correctes
				if user:  # Si l'objet renvoyé n'est pas None
					login(request, user)  # nous connectons l'utilisateur
					#messages.success(request, 'Vous êtes connecté.')
				else: # sinon une erreur sera affichée
					error = True
					messages.error(request, "Mauvais mot de passe.")
			except:
				error = True
				messages.error(request, "Aucun compte n'est associé à l'adresse email %s." % user_email)		
			
		else:
			error = True
			messages.error(request, "Erreur de connexion")

		if not error:
			return redirect('index')
		if error:
			return render(request, 'randoMap/connexion.html', locals())
	
	else:
		raise Http404("Page non trouvée sorry...")


def deconnexion(request):
	#Déconnexion d'un utilisateur
	logout(request)
	return redirect('index')

def moncompte(request):
	#Gestion d'un utilisateur
	if request.user.is_authenticated:
		if request.method == "POST":
			current_user = request.user
			if request.POST.get('email'):
				new_email = request.POST.get('email')
				current_user.email = new_email
				try:
					current_user.save()
					messages.success(request, "Votre adresse mail a été modifiée.")
				except:
					messages.success(request, "Cette adresse email est déjà utilisée.")
			elif request.POST.get('username'):
				current_user.username = request.POST.get('username')
				try:
					actual_user.save()
					messages.success(request, "Votre nom d'utilisateur a été modifiée.")
				except:
					messages.error(request, "Ce nom d'utilisateur est déjà pris.")
			elif request.POST.get('password') and request.POST.get('password_confirmation'):
				if request.POST.get('password') == request.POST.get('password_confirmation'):
					current_user.set_password(request.POST.get('password'))
					current_user.save()
					messages.success(request, "Votre mot de passe a bien été modifié.")
				else:
					messages.error(request, "Les mots de passes ne sont pas identiques.")
			elif request.FILES.get('nvelavatar'):
				if Avatar.objects.filter(user=current_user):
					old_avatar = Avatar.objects.get(user=current_user)
					old_avatar.delete()
					nvel_avatar = Avatar(user=current_user, photo=request.FILES.get('nvelavatar'))
					nvel_avatar.save()
				else:
					nvel_avatar = Avatar(user=current_user, photo=request.FILES.get('nvelavatar'))
					nvel_avatar.save()
				messages.success(request, "Votre avatar a bien été modifié.")
		else:
			pass
	else:
		messages.error(request, "Vous devez être authentifié pour effectuer cette opération.")		

				
	return render(request, "randoMap/moncompte.html", locals())

def creercompte(request):
	#Création d'un nouveau compte utilisateur
	if request.method=='POST':
		form = CreercompteForm(request.POST)
		if form.is_valid():
			#Les données reçues du client sont valides :
			new_user = User.objects.create_user(
													username=form.cleaned_data['user_name'],
													email=form.cleaned_data['user_email'],
													password=form.cleaned_data['user_password'],
													)
			new_user.save()			
			messages.success(request, 'Votre compte a bien été créé :)')
		else:
			#Les données reçues sont invalides :
			message.error(request, "Nous sommes désolés, il semble qu'il y a eu une erreur dans la création de votre compte...")
			return redirect(creercompte)
	return redirect('connexion')

