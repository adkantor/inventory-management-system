# Generated by Django 3.2.4 on 2021-09-10 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('can_view_all_users', 'Can view all users'), ('can_add_user', 'Can add new user'), ('can_update_all_users', 'Can update all users'), ('can_delete_all_users', 'Can delete all users')]},
        ),
    ]
