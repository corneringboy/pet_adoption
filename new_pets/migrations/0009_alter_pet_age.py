# Generated by Django 5.1.6 on 2025-03-11 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_pets', '0008_remove_pet_name_alter_pet_animal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='age',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
    ]
