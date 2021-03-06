# Generated by Django 3.0.6 on 2020-06-16 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('gate', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=20)),
                ('mail', models.EmailField(max_length=254, unique=True)),
                ('contact', models.IntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SuperAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='bdate',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mail',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=20),
        ),
    ]
