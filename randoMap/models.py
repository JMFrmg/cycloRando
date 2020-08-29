from django.db import models
from django.contrib.auth.models import User
from datetime import time


class Place(models.Model):
	place_id = models.SmallIntegerField("Local id", default="", blank=False)
	google_id = models.CharField("Google ID", max_length=200, default="", blank=False)
	lat = models.CharField("Latitude", max_length=50, default="", blank=False)
	lng = models.CharField("Longitude", max_length=50, default="", blank=False)	
	name = models.CharField("Nom de l'emplacement", max_length=200, default="", blank=False, null=False)
	address = models.CharField("Adresse de l'emplacement", max_length=200, default="", blank=False, null=False)
	PLACE_TYPES = [
		("CP", "Camping"),
		("BV", "Bivouac"),
		("PT", "Particulier"),
		("GT", "Gîte"),
		("HT", "Hotel")
	]
	place_type = models.CharField(
		"Type de lieu",
		max_length=2,
		choices=PLACE_TYPES,
		default="CP",
		blank=False
		)
	rating = models.DecimalField("Moyenne des notes", max_digits=2, decimal_places=1, default=0.0)
	user_ratings_total = models.SmallIntegerField("Nombre total de votes", default="0")
	phone_number = models.CharField('Numéro de téléphone', max_length=10, default=0)
	website = models.CharField("Site web", max_length=200, default="", blank=False)
	opening_hour = models.TimeField("Horaires d'ouverture", default=time(0))
	closing_hour = models.TimeField("Horaires de fermeture", default=time(0))

	def __str__(self):
		return self.name

class Openings(models.Model):
	place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)
	monday = models.CharField("Hoaraires du lundi", max_length=30, default="")
	tuesday = models.CharField("Hoaraires du mardi", max_length=30, default="")
	wednesday = models.CharField("Hoaraires du mercredi", max_length=30, default="")
	thursday = models.CharField("Hoaraires du jeudi", max_length=30, default="")
	friday = models.CharField("Hoaraires du vendredi", max_length=30, default="")
	saturday = models.CharField("Hoaraires du samedi", max_length=30, default="")
	sunday = models.CharField("Hoaraires du dimanche", max_length=30, default="")



	def __str__(self):
		return "Les horaires de %s" % self.place.name

class Camping(Place):
	restauration = models.BooleanField(default=False)
	bike_shopping = models.BooleanField(default=False)
	


class Note(models.Model):
	chiffre = models.SmallIntegerField("Note entre 0 et 5")
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="notes",
		default=0
		)
	place = models.ForeignKey(
		Place,
		on_delete=models.CASCADE,
		related_name="notes",
		default =0
		)
