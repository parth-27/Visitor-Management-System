# Generated by Django 3.0.6 on 2020-06-18 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0007_auto_20200618_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='gender',
            field=models.CharField(max_length=10),
        ),
    ]