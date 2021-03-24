from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from profiles.models import Profile
from .forms import ProductModelForm, ProductUpdateForm
from shopping_cart.models import Order, OrderItem
from django.urls import reverse
from django.db.models import Q 


# These views are for interactions with Products

def search_view(request, *args, **kwargs): # search product to update
    queryset = Product.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(id__icontains=query)
        ).distinct()

    context = {
        "queryset": queryset,
    }
    
    return render(request, 'search_results.html', context)


@staff_member_required
def product_create_view(request, *agrs, **kwargs):
    title = 'Create a product'
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = ProductModelForm()
    context = {
        "form":form,
    }
    return render(request, 'forms.html', context)

def product_detail_view(request, pk):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404

    return render(request, "products/detail.html", {"object":obj} )

@staff_member_required
def product_update_view(request, pk):
    title = 'Update a product'
    product = get_object_or_404(Product, pk=pk)
    form = ProductUpdateForm(request.POST or None, instance=product,)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(reverse('product_list'))
        
    context = {
        "form":form,
    }
    return render(request, 'forms.html', context)


def product_api_detail_view(request, pk, *args, **kwargs):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Not found'}) # return JSON with HTTP status code of 404

    return JsonResponse({"id": obj.pk})

@login_required
def product_list_view(request, *args, **kwargs):
    object_list     = Product.objects.all() # return all objects
    incompleted_orders = Order.objects.filter(user=request.user.profile, is_ordered=False) # filter orders of a user that was not completed
    current_order_products = [] # create an empty list to add products that are in incompleted orders
    if incompleted_orders.exists():
        user_order_items        = incompleted_orders[0].items.all()
        current_order_products  = [item.product for item in user_order_items]

    balance = Profile.objects.filter(user=request.user).first().balance
    
    context = {
        "object_list": object_list,
        "current_order_products": current_order_products,
        "balance": balance,
        }
    return render(request, 'products/list.html', context)

