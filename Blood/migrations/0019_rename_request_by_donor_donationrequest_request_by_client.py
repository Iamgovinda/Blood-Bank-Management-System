# Generated by Django 4.0.4 on 2022-06-03 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blood', '0018_donationrequest_response_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donationrequest',
            old_name='request_by_donor',
            new_name='request_by_client',
        ),
    ]
