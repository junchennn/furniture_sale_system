import datetime
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .extras import generate_order_id
from .models import OrderItem, Order
from profiles.models import Profile
from products.models import Product


def get_user_pending_order(request): # grab order for the current user     
    user_profile    = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(user=user_profile, is_ordered=False)
    if order.exists():
        return order[0] # ensure the only order in the filtered list is grabbed
    return 0

@login_required()
def add_to_cart(request, *args, **kwargs):
    user_profile    = get_object_or_404(Profile, user=request.user)
    # filter rpoducts by id
    product         = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # if product in request.user.Profile.eBooks.all():
    #     messages.info(request, 'You already own this book')
    #     return redirect(reverse('products:product-list'))
    
    # create OrderItem of the chosen product
    order_item, status = OrderItem.objects.get_or_create(product=product)

    # create an order associated with the user
    user_order, status = Order.objects.get_or_create(user=user_profile, is_ordered=False)

    user_order.items.add(order_item)

    if status:
        # use extra mode to generate order id
        user_order.order_id = generate_order_id()
        user_order.save()
    messages.info(request, 'Item added to cart successfully.')
    return redirect(reverse('product_list'))

@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted.")
    return redirect(reverse('order_summary'))

@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    balance = Profile.objects.filter(user=request.user).first().balance
    context = {
        'order': existing_order,
        'balance': balance
    }
    return render(request, 'shopping_cart/order_summary.html', context)

@login_required()
def checkout(request, **kwargs):
    existing_order = get_user_pending_order(request)
    balance = Profile.objects.filter(user=request.user).first().balance
    context = {
        'order': existing_order,
        'balance': balance,
    }
    return render(request, 'shopping_cart/checkout.html', context)

@login_required()
def process_payment(request, order_id):
    # process_payment (check if user has enough balance to purchase the order)
    user_profile = get_object_or_404(Profile, user=request.user)
    order_total = Order.objects.filter(pk=order_id).first().get_cart_total()
    if user_profile.balance > order_total:
        return redirect(reverse('update_records', 
                        kwargs={
                            'order_id': order_id,
                        })
                    )   
    else:
        messages.info(request, 'There is not enough credit in your account.')
        return redirect(reverse('product_list'))

@login_required()
def update_transaction_records(request, order_id):
    # grab the order which is to be processed
    order_to_complete   = Order.objects.filter(pk=order_id).first()

    # update the order information
    order_to_complete.is_ordered    = True
    order_to_complete.date_ordered  = datetime.datetime.now()
    order_to_complete.save() # save changes to database

    # get all the OrderItem from the order and update their info
    order_items = order_to_complete.items.all()
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # get user's profile to update remaining credit
    user_profile = get_object_or_404(Profile, user=request.user)

    # get the total cost from the order and deduct it from user's balance
    order_total = order_to_complete.get_cart_total()
    user_profile.deduct_balance(cost=order_total, save=True)

    # update products inventory
    for item in order_items:
        product = item.product
        product.remove_items_from_inventory(count=1, save=True)

    messages.info(request, "Thank you! Your order have been added to your profile.")
    return redirect(reverse('profile'))

def success(request, **kwargs):
    return render(request, 'shopping_cart/purchase_success.html', {})








