# Generated by Django 2.1 on 2021-05-01 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210418_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='idCategoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.Categoria'),
        ),
    ]
