import json
from .models import *

SIZES = ["XS", "S", "M", "L", "XL"]


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        size = ""
        cartItems += cart[i]['quantity']

        if("size" in cart[i].keys()):
            size = cart[i]['size']

        if(any(filter(lambda x: x in i, SIZES))):
            idOnly = ''.join(c for c in i if c.isdigit())
            product = Product.objects.get(id=idOnly)
        else:
            product = Product.objects.get(id=i)

        total = (product.price * cart[i]['quantity'])
        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']

        item = {
            'product': {
                'id': i,
                'name': product.name,
                'price': product.price,
                'imageURL': product.imageURL
            },
            'size': size,
            'quantity': cart[i]['quantity'],
            'get_total': total,
        }
        items.append(item)

    return {'cartItems':cartItems, 'order':order, 'items':items}


def cartData(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(username = request.user)
        user = customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        user = ''

    return {'cartItems':cartItems, 'order':order, 'items':items, 'user':user}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']
    address = data['shipping']['address']
    city = data['shipping']['city']
    psc = data['shipping']['psc']
    country = data['shipping']['country']

    customer, created = Customer.objects.get_or_create(name=name, email=email)
    customer.name = name
    customer.address = address
    customer.city = city
    customer.psc = psc
    customer.country = country
    customer.save()
    
    order = Order.objects.create(customer=customer, complete=False)

    cookieData = cookieCart(request)
    items = cookieData['items']
    
    for item in items:
        itemSize = ""
        
        if(any(filter(lambda x: x in item['product']['id'], SIZES))):
            itemSize = ''.join(c for c in item['product']['id'] if not c.isdigit())
            item['product']['id'] = ''.join(c for c in item['product']['id'] if c.isdigit())
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(product=product, order=order, size=itemSize, quantity=item['quantity'])
        else:
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])   

    return customer, order