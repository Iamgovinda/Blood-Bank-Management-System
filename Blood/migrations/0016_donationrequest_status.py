# Generated by Django 4.0.4 on 2022-06-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blood', '0015_donationrequest_request_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationrequest',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
