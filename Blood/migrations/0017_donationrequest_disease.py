# Generated by Django 4.0.4 on 2022-06-03 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blood', '0016_donationrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationrequest',
            name='disease',
            field=models.CharField(default='No Diesease', max_length=200),
        ),
    ]
