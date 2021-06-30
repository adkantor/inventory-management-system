# Generated by Django 3.2.4 on 2021-06-29 15:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('tax_number', models.CharField(blank=True, default='NA', max_length=32, null=True)),
                ('is_private_person', models.BooleanField(verbose_name='Private person')),
                ('contact_name', models.CharField(max_length=100)),
                ('contact_phone', models.CharField(max_length=20)),
                ('contact_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('partner_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='partners.partner')),
            ],
            bases=('partners.partner',),
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('partner_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='partners.partner')),
            ],
            bases=('partners.partner',),
        ),
    ]