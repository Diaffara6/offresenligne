# Generated by Django 4.2.3 on 2024-05-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0011_rename_offre_marche_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marche_public',
            name='pays',
            field=models.CharField(default='Burkina Faso', max_length=20),
        ),
    ]
