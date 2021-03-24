from django.shortcuts import render, get_object_or_404
from shopping_cart.models import Order
from .models import Profile

# Create your views here.
def profile_view(request):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders       = Order.objects.filter(user=my_user_profile)
    my_balance      = my_user_profile.balance
    context = {
        'my_orders': my_orders,
        'balance': my_balance,
    }

    return render(request, 'profiles/profile.html', context)