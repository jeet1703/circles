# Generated by Django 4.2.4 on 2023-09-19 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_current_conversation_alter_user_location_circle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='current_conversation_type',
            field=models.CharField(default='normal', max_length=16),
        ),
    ]
