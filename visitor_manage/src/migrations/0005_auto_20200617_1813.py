# Generated by Django 3.0.6 on 2020-06-17 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0004_auto_20200616_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bdate',
        ),
        migrations.AddField(
            model_name='visitor',
            name='visiting_hour',
            field=models.CharField(default=1, max_length=20),
        ),
    ]