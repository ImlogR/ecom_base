from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import datetime
from .utils import cartData, guestOrder

# Create your views here.
def store(request):
    data= cartData(request)
    cartItems= data['cartItems']
    products= product.objects.all()
    context= {
        'products': products,
        'cart_items':  cartItems,
    }
    return render(request, 'store/index.html', context)

def cart(request):
    data= cartData(request)
    items= data['items']
    orders= data['orders']
    cartItems= data['cartItems']
        
    context= {
        'items': items,
        'orders': orders,
        'cart_items':  cartItems,
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    data= cartData(request)
    items= data['items']
    orders= data['orders']
    cartItems= data['cartItems']
    context= {
        'items': items,
        'orders': orders,
        'cart_items':  cartItems,
    }
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data= json.loads(request.body)
    productId= data['productId']
    action= data['action']

    customer_ins = customer.objects.get(name= request.user)
    products= product.objects.get(id= productId)

    orders, created= order.objects.get_or_create(customer= customer_ins, complete= False)
    orderItem, created= orderItems.objects.get_or_create(order= orders, product= products)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action== 'remove':
        orderItem.quantity = (orderItem.quantity-1)
    orderItem.save();
    if orderItem.quantity <= 0:
        orderItem.delete();
    
    return JsonResponse("Item was added To cart!!", safe= False)

@login_required(login_url='/')
def add_product(request):
    if request.method == 'POST':
        product_image= request.FILES.get('product_image')
        product_name= request.POST['product_name']
        product_price= request.POST['product_price']
        product_state= request.POST['state']
        product_owner= User.objects.get(username= request.user.username)

        new_product= product.objects.create(
            name= product_name,
            price= product_price,
            digital= product_state,
            image= product_image,
            owner= product_owner
        )
        new_product.save();
    
    data= cartData(request)
    cartItems= data['cartItems']
    context= {
        'cart_items':  cartItems,
    }
    return render(request, 'store/add_product.html', context)

def processOrder(request):
    transaction_id= datetime.datetime.now().timestamp()
    data= json.loads(request.body)

    if request.user.is_authenticated:
        Customer= request.user
        Customer= customer.objects.get(name= Customer)
        orders, created= order.objects.get_or_create(customer= Customer, complete= False)


    else:
        Customer, orders= guestOrder(request, data)


    if (orders.shipping== True):
        shippingAddress.objects.create(
            customer= Customer,
            order= orders,
            address= data['shipping']['address'],
            city= data['shipping']['city'],
            state= data['shipping']['state'],
            zipcode= data['shipping']['zipcode'],
        )
        
    total= float(data['form']['total'])
    orders.transaction_id= transaction_id
    if total== orders.get_cart_total:
        orders.complete= True
    orders.save();

    return JsonResponse('Payment submitted', safe=False)

@login_required(login_url='/')
def shop(request):
    data= cartData(request)
    cartItems= data['cartItems']
    owner= User.objects.get(username= request.user.username)
    products= product.objects.filter(owner= owner)
    context= {
        'products': products,
        'cart_items':  cartItems,
    }
    return render(request, 'store/shop.html', context)

def view_product(request, id):
    data= cartData(request)
    cartItems= data['cartItems']
    products= product.objects.get(id= id)
    context= {
        'cart_items':  cartItems,
        'product': products,
    }
    return render(request, 'store/view_product.html', context)
    
def update_product(request, id):
    products= product.objects.get(id= id)
    data= cartData(request)
    cartItems= data['cartItems']

    if request.method== 'POST':
        updated_picture= request.FILES.get('product_image')
        if updated_picture == None:
            updated_picture= products.image

        updated_name= request.POST['updated-name']
        updated_price= request.POST['updated-price']
        updated_state= request.POST['digital']

        products.image= updated_picture
        products.name= updated_name
        products.price= updated_price
        products.digital= updated_state
        products.save();
    

    context= {
        'cart_items':  cartItems,
        'product': products,
    }
    return render(request, 'store/update_product.html', context)

@login_required(login_url='/')
def delete_product(request, id):
        delete_item= product.objects.get(id= id)
        delete_item.delete();
        return redirect('/shop')
