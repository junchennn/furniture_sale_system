from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()

# Create models here

class Profile(models.Model):
    user    = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1087.65)
    
    def __str__(self):
        return self.user.username
        
    def deduct_balance(self, cost, save=True):
        current_balance = self.balance
        current_balance = current_balance - cost
        self.balance = current_balance
        if save == True:
            self.save()
        return self.balance


def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        
post_save.connect(post_save_create_profile, sender=settings.AUTH_USER_MODEL)