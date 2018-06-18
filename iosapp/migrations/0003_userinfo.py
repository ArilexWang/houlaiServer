# Generated by Django 2.0.6 on 2018-06-18 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iosapp', '0002_auto_20180617_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('openid', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('headimgurl', models.CharField(max_length=512)),
                ('nickname', models.CharField(max_length=255)),
                ('unionid', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
            ],
        ),
    ]