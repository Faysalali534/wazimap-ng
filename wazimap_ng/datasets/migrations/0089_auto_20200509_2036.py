# Generated by Django 2.2.10 on 2020-05-09 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0088_auto_20200501_1258'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indicator',
            options={'ordering': ['id'], 'verbose_name': 'Variable'},
        ),
    ]
