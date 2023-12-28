from django import forms
from django.contrib.auth.models import User
from .models import Profile




# Class pour la création d'un nouveau user
class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={"class": 'form-control', 'placeholder': "Votre mot de passe"}))
    password2 = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={"class": 'form-control', 'placeholder': "Confirmation de votre mot de passe"}))


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

        labels = {'username': "", 'first_name': "", 'email': "", 'last_name': ""}

        widgets = {
            'username': forms.EmailInput(attrs={"class": 'form-control', 'placeholder': 'Votre adresse Email'}),
            'email': forms.EmailInput(attrs={"class": 'form-control', 'placeholder': "Confirmation de votre adresse Email"}),
            'first_name': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Votre Prénom"}),            
            'last_name': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Votre Nom de famille"}),
        }   

    def clean_password2(self):
        # Vérification que les mots de passes sont identique
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Les mots de passe ne sont pas identique')
            
        return cd['password2']
    
    def clean_email(self):
        # Vérifie que l'adresse mail n'est pas déja utilisé
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
 
        return data
    

# class pour modifié un utilisateur
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        labels = {
            "first_name": "",
            "last_name": "",

        }
        widgets = {
            'first_name': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Votre Prénom"}),            
            'last_name': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Votre Nom de famille"}),
        }


# class pour modifié le profil d'un utilisateur
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "genre",
            "date_of_birth",
            "address_primary",
            "complement_adress_primary",
            "postal_code_primary",
            "city_primary",
            "phoneNumber1",
            "phoneNumber2",
            "address_secondery",
            "complement_adress_secondary",
            "postal_code_secondery",
            "city_secondery",            
        ]
        labels = {
            "genre": "",
            "date_of_birth": "",
            "address_primary": "",
            "complement_adress_primary": "",
            "postal_code_primary": "",
            "city_primary": "",
            "phoneNumber1": "",
            "phoneNumber2": "",
            "address_secondery": "",
            "complement_adress_secondary": "",
            "postal_code_secondery": "",
            "city_secondery": "",
        }
        widgets = {
             'date_of_birth': forms.DateInput(attrs={"class": 'form-control', 'placeholder': "Date de naissance"}),
             'address_primary': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Adresse principale"}),
             'complement_adress_primary': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Complement d'adresse"}),
             'postal_code_primary': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Code Postal", "id": "codePostal_primary"}),
             'city_primary': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Ville", "name": "city_primary", "id": "city_primary", "hidden": "true"}),
             'phoneNumber1': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "N° Mobile"}),
             'phoneNumber2': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "N° Fixe"}),
             'address_secondery': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Adresse secondaire"}),
             'complement_adress_secondary': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Complement d'adresse"}),
             'postal_code_secondery': forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Code Postal", "id": "codePostal_secondery"}),
             'city_secondery': forms.TextInput(attrs={"class": 'form-control', "name": "city_secondery", "id": "city_secondery", "hidden": "true"}),
        }

