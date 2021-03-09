# Generated by Django 3.1 on 2020-08-18 09:34

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Akcesoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(auto_now_add=True)),
                ('co', models.CharField(choices=[('plecki', 'Plecki'), ('book', 'Książka'), ('szklo', 'Szkło'), ('folia', 'Folia'), ('inne', 'Inne')], default='plecki', max_length=15)),
                ('kwota', models.DecimalField(decimal_places=2, max_digits=5)),
                ('model', models.CharField(blank=True, max_length=128, null=True)),
                ('kto', models.ForeignKey(default=django.contrib.auth.models.User, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
