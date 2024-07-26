from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import ProductForm
from core.models import *

def index(request):
    products = Product.objects.all()
    return render(request, 'core/index.html',{'products': products})

def product_desc(request,pk):
    product= Product.objects.get(pk=pk)
    return render(request,'core/product_desc.html',{'product':product})


def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(product__pk=pk).exists():
            # Increase the quantity if the item is already in the cart
            existing_order_item = order.items.filter(product__pk=pk).first()
            existing_order_item.quantity += 1
            existing_order_item.save()
            messages.info(request, 'Item quantity updated in the cart.')
        else:
            # Add new item to the cart
            order.items.add(order_item)
            messages.info(request, 'Item added to the cart.')

    else:
        # Create a new order if none exists
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'Item added to the cart.')

    return redirect('product_desc', pk=pk)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('add_product')  # Redirect to the same view after successful form submission
        else:
            messages.error(request, 'Error adding product. Please correct the errors below.')
            # Render the form with errors
            return render(request, 'core/add_product.html', {'form': form})

    else:
        form = ProductForm()

    return render(request, 'core/add_product.html', {'form': form})



def order_list(request):
    if Order.objects.filter(user=request.user,ordered=False).exists():
        order = Order.objects.get(user=request.user,ordered=False)
        return render(request,'core/orderlist.html',{'order':order})
    return render(request,'core/orderlist.html',{'message':'Your Cart is Empty'})
