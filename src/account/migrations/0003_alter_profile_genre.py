# Generated by Django 5.0 on 2023-12-29 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_complement_adress_primary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='genre',
            field=models.CharField(choices=[('aucun', 'aucun'), ('Mme.', 'Mme.'), ('Mr.', 'Mr.')], default=1, max_length=20),
        ),
    ]