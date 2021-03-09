# Generated by Django 3.1 on 2020-08-18 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StanAkcesoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=50)),
                ('nazwa', models.CharField(max_length=250)),
                ('ilosc', models.PositiveSmallIntegerField()),
                ('searchstring', models.CharField(default='Null', max_length=250)),
            ],
        ),
    ]
