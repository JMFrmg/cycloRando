from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('getplaces/', views.getplaces, name='getplaces'),
    path('getplacedetails/', views.getplacedetails, name='getplacedetails'),
    path('connexion/', views.connexion, name='connexion'),
	path('deconnexion/', views.deconnexion, name='deconnexion'),
	path('moncompte/', views.moncompte, name='moncompte'),
	path('creercompte/', views.creercompte, name='creercompte'),
	path('participate/', views.moncompte, name='participate'),
	path('new-spot/', views.newSpot, name='newSpot'),
	path('edit-place/', views.editPlace, name='editPlace'),
]
