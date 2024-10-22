from django.db import models



UNIT_CHOICES = [
    ('Kg', 'Kilograms'),
    ('g', 'Grams'),
    ('l', 'Litres'),
    ('units', 'Units')
]


class InventoryModel(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='units')
    price = models.DecimalField(max_digits=10, decimal_places=2)

