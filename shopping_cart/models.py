from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model

from profiles.models import Profile
from products.models import Product

User = get_user_model()

# Create your models here.
class OrderItem(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity        = models.IntegerField(default=1)
    is_ordered      = models.BooleanField(default=False)
    date_added      = models.DateTimeField(auto_now_add=True)
    date_ordered    = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.name
    
    def get_total_item_price(self):
        return self.quantity * self.product.price


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
        return sum([item.get_total_item_price() for item in self.items.all()])
        

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.order_id)
