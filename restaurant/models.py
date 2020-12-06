
from django import forms

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime

# class User(AbstractUser):
#    phone = models.CharField(verbose_name="phone number", max_length=11)
#    job = models.CharField(max_length=30, blank=True)

class restaurant(models.Model):
    """docstring for restaurants."""

    name = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    capacity = models.IntegerField(blank=True)
    desc = models.CharField(max_length=200, blank=True)

    logo = models.ImageField(upload_to="images/", blank=False, null=True)

    def __str__(self):
        return self.name

class companies(models.Model):
    """docstring for Company."""

    name = models.CharField(max_length=30, blank=False, null=True )
    address = models.CharField(max_length=100,blank=False, null=True)
    phone = models.CharField(max_length=15, blank=False, null=True)
    desc = models.CharField(max_length=200, blank=True)

    logo = models.ImageField(upload_to="images/", blank=False, null=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    """docstring for User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(verbose_name="phone number", max_length=11)
    job = models.CharField(max_length=30, blank=True)
    is_rest_staff = models.BooleanField(default=False)
    is_comp_staff = models.BooleanField(default=False)
    company_id = models.ForeignKey(companies, blank=True, null=True, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(restaurant, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Category(models.Model):
    """docstring for Category of Product."""

    name = models.CharField(max_length=30, blank=False, null=True )
    desc = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """docstring for Product."""

    name = models.CharField(max_length=30, blank=False, null=True )
    category_id = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(restaurant, blank=True, null=True, on_delete=models.CASCADE)
    desc = models.TextField(max_length=200, blank=True)
    calories = models.DecimalField(max_digits=19, decimal_places=2)
    fats = models.DecimalField( max_digits=19, decimal_places=2)
    price = models.DecimalField( max_digits=19, blank=True, null=True, decimal_places=2)
    image = models.ImageField(upload_to="images/product", blank=True, null=True)

    def __str__(self):
        return self.name
    # logo = models.ImageField()
class Reviewer(models.Model):
    """ Docstring for Reviewer """

    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    review = models.TextField(max_length=200, blank=True)
    star_rate = models.DecimalField( max_digits=19, decimal_places=2)

    review_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return ('{}- Product: {} is rate {}'.format(self.user_id.username,self.product_id, self.star_rate))
ORDER_STATE = [
    ('IN_REQUEST', 'Request' ),
    ('IN_PREPARING', 'Preparing'),
    ('RECIVED', 'Received'),
    ('CANCELED', 'Cancel'),
]

class Order(models.Model):
    """ Docstring for Order """
    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    company_id = models.ForeignKey(companies, blank=True, null=True, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(restaurant, blank=True, null=True, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    order_date = models.DateField(default=datetime.now, blank=True)
    qty = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=30, default='Request' ,choices=ORDER_STATE )
    is_send = models.BooleanField(default=False)

    def __str__(self):
        return ("{} request Product {} From {} Restaurant has {}".format(self.user_id,self.product_id,self.restaurant_id,self.state))
