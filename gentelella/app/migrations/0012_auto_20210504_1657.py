# Generated by Django 2.1 on 2021-05-04 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_merge_20210503_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentocompra',
            name='numeroDocumento',
            field=models.CharField(max_length=12),
        ),
    ]
