# Generated by Django 3.1.7 on 2021-03-27 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('continuum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='image',
            field=models.ImageField(upload_to='uploadedfiles', verbose_name='img'),
        ),
    ]