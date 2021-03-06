# Generated by Django 3.1 on 2020-09-26 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200914_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='barrio',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='emprendimiento',
            name='cont_insta',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='emprendimiento',
            name='cont_mail',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='emprendimiento',
            name='descripcion',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='emprendimiento',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
