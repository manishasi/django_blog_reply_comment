# Generated by Django 4.1.6 on 2023-03-17 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_reply_options_post_viewers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='viewers',
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reply',
            name='replay',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replays', to='myapp.reply'),
        ),
    ]
