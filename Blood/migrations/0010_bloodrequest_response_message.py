# Generated by Django 4.0.4 on 2022-06-02 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blood', '0009_alter_bloodrequest_request_by_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequest',
            name='response_message',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
