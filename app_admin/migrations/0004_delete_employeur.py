# Generated by Django 4.2.3 on 2023-08-19 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0003_employeur_fonction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employeur',
        ),
    ]