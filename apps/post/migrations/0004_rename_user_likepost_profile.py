# Generated by Django 4.1 on 2022-08-27 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_post_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likepost',
            old_name='user',
            new_name='profile',
        ),
    ]
