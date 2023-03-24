import json
from .models import *

def cookieCart(request):
    try:
        cart= json.loads(request.COOKIES['cart'])
    except:
        cart= {}

    items=[]
    orders= {'get_cart_total': 0, 'get_cart_items':0, 'shipping':False}
    cartItems= orders['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            products = product.objects.get(id= i)
            total= (products.price * cart[i]["quantity"])
            orders['get_cart_total'] += total
            orders['get_cart_items']+= cart[i]['quantity']

            item={
                'product':{
                    'id': products.id,
                    'name': products.name,
                    'price': products.price,
                    'imageURL': products.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
            if products.digital== False:
                orders['shipping']= True
        except:
            pass
    return {'cartItems': cartItems, 'orders':orders, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer= request.user.user_name
        orders, created= order.objects.get_or_create(customer= customer, complete= False)
        items= orders.orderid.all()
        cartItems= orders.get_cart_items
    else:
        cookieData= cookieCart(request)
        cartItems= cookieData['cartItems']
        orders= cookieData['orders']
        items= cookieData['items']
    return {'cartItems': cartItems, 'orders':orders, 'items':items}

def guestOrder(request, data):
    print('User not logged')
    print('cookies:', request.COOKIES)
    name= data['form']['name']
    email= data['form']['email']

    cookieData= cookieCart(request)
    items= cookieData['items']

    Customer, created= customer.objects.get_or_create(
        email= email,
        )
    Customer.name= name
    Customer.save();
    orders= order.objects.create(
        customer= Customer,
        complete= False,
    )
    for item in items:
        products= product.objects.get(id= item['product']['id'])
        orderItem= orderItems.objects.create(
            product= products,
            order= orders,
            quantity= item['quantity']
        )
    return Customer, orders