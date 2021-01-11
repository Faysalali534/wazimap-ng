# Generated by Django 2.2.13 on 2020-11-17 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0037_auto_20200928_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilecategory',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='theme',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name='profilecategory',
            options={'ordering': ['order'], 'verbose_name': 'Profile Collection',
                     'verbose_name_plural': 'Profile Collections'},
        ),
        migrations.AlterModelOptions(
            name='theme',
            options={'ordering': ['order']},
        ),
    ]
