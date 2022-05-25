# Generated by Django 4.0.4 on 2022-05-25 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blood', '0002_bloodrequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloodrequest',
            old_name='age',
            new_name='patient_age',
        ),
        migrations.RenameField(
            model_name='bloodrequest',
            old_name='bloodgroup',
            new_name='patient_bloodgroup',
        ),
        migrations.RenameField(
            model_name='bloodrequest',
            old_name='gender',
            new_name='patient_gender',
        ),
        migrations.RenameField(
            model_name='bloodrequest',
            old_name='Name',
            new_name='patient_name',
        ),
        migrations.RenameField(
            model_name='bloodrequest',
            old_name='date',
            new_name='request_date',
        ),
    ]
