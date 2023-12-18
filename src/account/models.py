from django.db import models
from django.conf import settings


class Profile(models.Model):
    GENRE = (
        ('aucun', 'aucun'),
        ('Mme', 'Mme.'),
        ('Mr.', 'Mr.'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    address_primary = models.CharField(max_length=250)
    postal_code_primary = models.CharField(max_length=20)
    city_primary = models.CharField(max_length=100)
    phoneNumber1 = models.CharField(max_length=16, blank=True, null=True)
    phoneNumber2 = models.CharField( max_length=16, blank=True, null=True)
    address_secondery = models.CharField(max_length=250, blank=True, null=True)
    postal_code_secondery = models.CharField(max_length=20, blank=True, null=True)
    city_secondery = models.CharField(max_length=100, blank=True, null=True)
    genre = models.CharField(choices=GENRE, default=1, max_length=20)
	

    def __str__(self):
        return f'{self.user.username}'