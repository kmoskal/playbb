# Generated by Django 3.0.7 on 2020-07-15 03:25

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
                ('symbol', models.CharField(max_length=15)),
                ('nazwa', models.CharField(max_length=150)),
                ('ilosc', models.PositiveSmallIntegerField()),
                ('searchstring', models.CharField(default='Null', max_length=150)),
            ],
        ),
    ]
