# Generated by Django 4.2.3 on 2023-08-15 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_blog', '0003_alter_offre_doc1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidature',
            name='date_limite',
        ),
        migrations.RemoveField(
            model_name='candidature',
            name='employe',
        ),
        migrations.AddField(
            model_name='offre',
            name='delai',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offre',
            name='employe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
