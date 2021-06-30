# Generated by Django 3.2.4 on 2021-06-30 09:55

from django.db import migrations, models
import inventories.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='material_group',
            field=models.ForeignKey(default=inventories.models.get_undefined_material_group, on_delete=models.SET(inventories.models.get_deleted_material_group), related_name='materials', to='inventories.materialgroup'),
        ),
    ]
