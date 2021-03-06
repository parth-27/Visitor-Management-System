# Generated by Django 3.0.6 on 2020-06-19 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0009_auto_20200619_0343'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mail', models.EmailField(max_length=254, unique=True)),
                ('contact', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('photo', models.ImageField(upload_to='gallery')),
                ('visitDate', models.DateField()),
                ('checkin', models.DateTimeField(null=True)),
                ('checkout', models.DateTimeField(null=True)),
                ('feedback', models.TextField(null=True)),
                ('visiting_hour', models.CharField(default=1, max_length=20)),
                ('reason', models.TextField(max_length=1000)),
                ('gateId', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='src.Admin')),
            ],
        ),
    ]
