# Generated by Django 3.1.3 on 2020-11-30 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awwards', '0004_auto_20201130_0626'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsLetterRecipients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
