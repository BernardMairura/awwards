# Generated by Django 3.1.3 on 2020-12-01 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awwards', '0002_auto_20201201_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.TextField(blank=True),
        ),
    ]
