# Generated by Django 4.0.6 on 2023-01-04 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session_Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startSession', models.DateField()),
                ('endSession', models.DateField()),
            ],
        ),
    ]