# Generated by Django 4.1 on 2022-08-30 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follows', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='user.profile')),
            ],
        ),
    ]