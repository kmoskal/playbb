# Generated by Django 3.0.7 on 2020-06-26 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inwentaryzacja', '0002_auto_20200317_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raport',
            name='data_elza',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='raport',
            name='doladowania_elza',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='raport',
            name='kasa_elza',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='raport',
            name='telefony_elza',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='raport',
            name='voice_elza',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='raport',
            name='zdrapki_elza',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
