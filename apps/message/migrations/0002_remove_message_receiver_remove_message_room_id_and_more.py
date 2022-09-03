# Generated by Django 4.1 on 2022-09-03 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='message',
            name='room_id',
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
        ),
        migrations.CreateModel(
            name='MessageMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first', to='user.profile')),
                ('second_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='meta',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='message.messagemeta'),
            preserve_default=False,
        ),
    ]