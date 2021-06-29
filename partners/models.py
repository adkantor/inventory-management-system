import uuid
from django.db import models
from django.urls import reverse


class Partner(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    tax_number = models.CharField(max_length=32, blank=True)
    is_private_person = models.BooleanField(verbose_name='Private person', default=False)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)

    def __str__(self):
        return f'{self.name} ({self.tax_number})'

    def get_absolute_url(self):
        raise NotImplementedError


class Vendor(Partner):
    def get_absolute_url(self):
        return reverse('vendor_detail', args=[str(self.id)])


class Customer(Partner):
    def get_absolute_url(self):
        return reverse('customer_detail', args=[str(self.id)])
