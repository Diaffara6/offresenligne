# Generated by Django 4.2.3 on 2024-06-05 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_employeur', '0009_remove_employeur_active_offres_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeur',
            name='nom1',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='employeur',
            name='nom2',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]