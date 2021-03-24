from django.conf import settings
from django.db import models
from django.urls import reverse


User = settings.AUTH_USER_MODEL
# Create models here
class Product(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=220)
    # description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # price of item to be decimal with 2 decimal places
    inventory = models.IntegerField(default=0)
    # featured = models.BooleanField(default=False)

    def has_inventory(self):
        return self.inventory > 0   # this return if the item is in stock (True/False)

    def remove_items_from_inventory(self, count=1, save=True):
        current_inv = self.inventory
        current_inv = current_inv - 1
        self.inventory = current_inv
        if save == True:
            self.save()
        return self.inventory
    
    def get_update_url(self):
        return reverse("update_product", kwargs={
            'pk':self.pk})
