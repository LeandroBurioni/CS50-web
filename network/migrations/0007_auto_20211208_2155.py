# Generated by Django 3.2.5 on 2021-12-08 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_following_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_message',
            field=models.TextField(max_length=150),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('like_user', 'like_post')},
        ),
    ]
