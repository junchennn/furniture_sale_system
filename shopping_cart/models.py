from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model

from profiles.models import Profile
from products.models import Product

User = get_user_model()

# Create your models here.
class OrderItem(models.Model):
    product         = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    is_ordered      = models.BooleanField(default=False)
    date_added      = models.DateTimeField(auto_now_add=True)
    date_ordered    = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    order_id        = models.CharField(max_length=15)
    user            = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    is_ordered      = models.BooleanField(default=False)
    items           = models.ManyToManyField(OrderItem)
    # payment_details = models.ForeignKey(Payment, null=True)
    date_ordered    = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.order_id)