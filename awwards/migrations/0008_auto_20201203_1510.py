# Generated by Django 3.1.3 on 2020-12-03 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('awwards', '0007_auto_20201203_1451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='user',
        ),
    ]
