# Generated by Django 2.2.8 on 2020-01-10 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0002_auto_20200110_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='points.Theme'),
        ),
    ]
