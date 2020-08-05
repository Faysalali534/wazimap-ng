# Generated by Django 2.2.10 on 2020-08-05 05:30

from django.db import migrations


def create_choropleth_method(apps, schema_editor):

    ChoroplethMethod = apps.get_model("profile", "ChoroplethMethod")
    ChoroplethMethod.objects.create(
        name="absolute_value",
        description="This method displays the exact value as provided in the data."
    )

class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0043_profile_configuration'),
    ]

    operations = [
        migrations.RunPython(create_choropleth_method),
    ]
