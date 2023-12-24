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
        fields = ['first_name', 'last_name', 'email']
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom de famille",
            "email": "Adresse Email",
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
            "genre": "genre",
            "date_of_birth": "Date de naissance",
            "address_primary": "Adresse principale",
            "complement_adress_primary": "Complement d'adresse",
            "postal_code_primary": "Code Postal",
            "city_primary": "Ville",
            "phoneNumber1": "N° Mobile",
            "phoneNumber2": "N° Fixe",
            "address_secondery": "Adresse secondaire",
            "complement_adress_secondary": "Complement d'adresse",
            "postal_code_secondery": "Code Postal",
            "city_secondery": "Ville",
        }
