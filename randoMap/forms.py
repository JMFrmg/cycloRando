from django import forms
from .models import Place

class CreercompteForm(forms.Form):
    user_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Votre pseudo"}), max_length=100)
    user_email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}), max_length=254)
    user_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}), max_length=254)
    confirm_password=forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}), max_length=254)

    def clean(self):
        cleaned_data = super(CreercompteForm, self).clean()
        user_password = cleaned_data.get("user_password")
        confirm_password = cleaned_data.get("confirm_password")

        if user_password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class ConnexionForm(forms.Form):
	user_email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}), max_length=254)
	user_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}), max_length=254)

class EditPlaceForm(forms.Form):
    """
    place_category = forms.ChoiceField(
        choices=(
        ("CP", "Camping"),
        ("BV", "Bivouac"),
        ("PT", "Particulier"),
        ("GT", "Gîte"),
        ("HT", "Hotel"),
    ))
    """
    
    adress = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "adresse"}), max_length=100)
    phone_number = forms.CharField(label ='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Numéro de téléphone'}), max_length=10)
    #opening_hour = forms.TimeField(label = '', required=False, widget=forms.TimeInput(attrs={'placeholder': "Heure d'ouverture ex:8:30"}))
    #closing_hour = forms.TimeField(label = '', required=False, widget=forms.TimeInput(attrs={'placeholder': "Heure de fermeture ex:18:30"}))
    note = forms.IntegerField(label = 'Note /5', required=False, max_value=5, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Note sur 5'}))

class NewPlaceForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Nom"}), max_length=100)
    """
    place_category = forms.ChoiceField(
        choices=(
        ("CP", "Camping"),
        ("BV", "Bivouac"),
        ("PT", "Particulier"),
        ("GT", "Gîte"),
        ("HT", "Hotel"),
    ))
    """
