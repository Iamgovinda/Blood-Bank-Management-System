# Generated by Django 4.0.4 on 2022-05-25 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blood', '0003_rename_age_bloodrequest_patient_age_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequest',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bloodrequest',
            name='mobile',
            field=models.CharField(default='+9779800000000', max_length=15, null=True),
        ),
    ]
