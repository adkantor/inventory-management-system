# Generated by Django 3.2.4 on 2021-09-13 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0006_transaction_goods_dispatch_note'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'permissions': [('can_view_all_transactions', 'Can view all transactions')]},
        ),
    ]
