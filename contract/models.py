from django.db import models

from user.models import UserModel

from datetime import datetime


class ContractModel(models.Model):
    CONTRACT_TYPE = [
        ('borrowed', 'US borrowed'),
        ('lent', 'lent'),
    ]
    
    CONTRACT_STATUS = [
        ('active', 'Active'),
        ('deleted', 'deleted'),
        ('waiting', 'waiting'),
        ('done', 'done'),
    ]
    
    CURRENCY = [
        ('usd', 'usd'),
        ('uzs', 'uzs'),
        ('rub', 'rub'),
    ]
    
    type = models.CharField(choices=CONTRACT_TYPE, max_length=20)
    status = models.CharField(choices=CONTRACT_STATUS, max_length=20)
    currency = models.CharField(choices=CURRENCY, max_length=20)

    who = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name="contracts")
    whom = models.CharField(max_length=13)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(null=True, blank=True)
    date = models.DateField(default=datetime.now)
    deadline = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.amount)
    

    class Meta:
        ordering = ['-id']
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'