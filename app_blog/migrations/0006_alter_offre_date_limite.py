# Generated by Django 4.2.3 on 2023-08-19 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0005_alter_offre_date_limite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offre',
            name='date_limite',
            field=models.DateField(),
        ),
    ]