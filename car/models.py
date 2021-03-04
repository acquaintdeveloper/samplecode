from django.db import models

class Car(models.Model):
    seller_name = models.CharField(max_length=100)
    seller_mobile = models.CharField(max_length=100)
    make = models.ForeignKey('Make',null=True,blank=True,on_delete=models.CASCADE)
    car_model = models.CharField(max_length=12,blank=True,null=True)
    year = models.ForeignKey('Year',null=True,blank=True,on_delete=models.CASCADE)
    condition = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    is_buy = models.BooleanField(default=False)

class Make(models.Model):
    name = models.CharField(max_length=100)

class Year(models.Model):
    year = models.CharField(max_length=100)
