from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = [
		'user',
		'date_of_birth',
		'address_primary',
		'postal_code_primary',
		'city_primary',
		'phoneNumber1',
		'phoneNumber2',
		'address_secondery',
		'postal_code_secondery',
		'city_secondery',
		]

	raw_id_fields = ['user']
