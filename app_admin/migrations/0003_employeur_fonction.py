# Generated by Django 4.2.3 on 2023-08-19 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0002_rename_utilsateur_employeur_utilisateur'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeur',
            name='fonction',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
