# Generated by Django 2.0.6 on 2018-06-18 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iosapp', '0006_delete_commentinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentInfo',
            fields=[
                ('dayid', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('openid', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=255)),
                ('created', models.CharField(max_length=255)),
            ],
        ),
    ]