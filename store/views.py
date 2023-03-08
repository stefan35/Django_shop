from django.shortcuts import render, redirect
from .models import *
from .utils import cartData, guestOrder, SIZES
from .forms import RegisterForm, ProfileForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import json
import datetime
import random


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    user = data['user']

    products = Product.objects.all()
    products = random.sample(list(set(products)), k=3)

    context = {'products':products, 'cartItems':cartItems, 'user':user}
    
    return render(request, 'store/store.html', context)


def categoryBook(request):
    filters = {}
    picked_products = []
    tmp_products = []
    products = None

    filters["checkbox1"] = request.POST.get('checkbox1')
    filters["checkbox2"] = request.POST.get('checkbox2')
    filters["checkbox3"] = request.POST.get('checkbox3')
    filters["min_price"] = request.POST.get('min_price')
    filters["max_price"] = request.POST.get('max_price')

    if(filters["max_price"] and filters["min_price"]):
        if(int(filters["max_price"]) < int(filters["min_price"])):
            messages.info(request, 'Incorrect values for price interval')
        else:
            tmp_products = Product.objects.filter(category="books")
            for product in tmp_products:
                if(product.price >= int(filters["min_price"]) and product.price <= int(filters["max_price"])):
                    picked_products.append(product)

    tmp_products = []
    if len(picked_products) == 0 and (not filters["max_price"] and not filters["min_price"]):
        picked_products = Product.objects.filter(category="books")
    if request.POST.get('checkbox1') != None:
        tmp_products.append(list(filter(lambda x: x.filters.genre == request.POST.get('checkbox1'), picked_products)))
    if request.POST.get('checkbox2') != None:
        tmp_products.append(list(filter(lambda x: x.filters.genre == request.POST.get('checkbox2'), picked_products)))
    if request.POST.get('checkbox3') != None:
        tmp_products.append(list((filter(lambda x: x.filters.genre == request.POST.get('checkbox3'), picked_products))))

    if len(tmp_products) > 0:
        tmp_products = sum(tmp_products, [])
        products = Product.objects.filter(name__in=tmp_products)
    else:
        products = Product.objects.filter(name__in=list(picked_products))

    data = cartData(request)
    cartItems = data['cartItems']
    user = data['user']

    context = {"products": products, 'cartItems': cartItems, 'user': user, "filters": filters}
    
    return render(request, 'store/category_book.html', context)
    

def categoryShirt(request):
    picked_products = []
    filters = {}

    filters["checkbox1"] = request.POST.get('checkbox1')
    filters["checkbox2"] = request.POST.get('checkbox2')
    filters["checkbox3"] = request.POST.get('checkbox3')
    filters["checkbox4"] = request.POST.get('checkbox4')
    filters["checkbox5"] = request.POST.get('checkbox5')
    filters["checkbox6"] = request.POST.get('checkbox6')
    filters["checkbox7"] = request.POST.get('checkbox7')
    filters["checkbox8"] = request.POST.get('checkbox8')
    filters["min_price"] = request.POST.get('min_price')
    filters["max_price"] = request.POST.get('max_price')

    if(filters["max_price"] and filters["min_price"]):
        if(int(filters["max_price"]) < int(filters["min_price"])):
            messages.info(request, 'Incorrect values for price interval')
        else:
            tmp_products = Product.objects.filter(category="clothes")
            for product in tmp_products:
                if(product.price >= int(filters["min_price"]) and product.price <= int(filters["max_price"])):
                    picked_products.append(product)
    
    tmp_products = []

    if len(picked_products) == 0 and (not filters["max_price"] and not filters["min_price"]):
        picked_products = Product.objects.filter(category="clothes")
    if request.POST.get('checkbox1') != None:
        tmp_products.append(list(filter(lambda x: x.filters.color == request.POST.get('checkbox1'), picked_products)))
    if request.POST.get('checkbox2') != None:
        tmp_products.append(list(filter(lambda x: x.filters.color == request.POST.get('checkbox2'), picked_products)))
    if request.POST.get('checkbox3') != None:
        tmp_products.append(list((filter(lambda x: x.filters.color == request.POST.get('checkbox3'), picked_products))))
    if request.POST.get('checkbox4') != None:
        tmp_products.append(list(filter(lambda x: x.filters.color == request.POST.get('checkbox4'), picked_products)))
    if request.POST.get('checkbox5') != None:
        tmp_products.append(list(filter(lambda x: x.filters.color == request.POST.get('checkbox5'), picked_products)))
    if request.POST.get('checkbox6') != None:
        tmp_products.append(list((filter(lambda x: x.filters.color == request.POST.get('checkbox6'), picked_products))))
    if request.POST.get('checkbox7') != None:
        tmp_products.append(list(filter(lambda x: x.filters.color == request.POST.get('checkbox7'), picked_products)))
    if request.POST.get('checkbox8') != None:
        tmp_products.append(list(filter(lambda x: x.filters.color == request.POST.get('checkbox8'), picked_products)))

    if len(tmp_products) > 0:
        tmp_products = sum(tmp_products, [])
        products = Product.objects.filter(name__in=tmp_products)
    else:
        products = Product.objects.filter(name__in=list(picked_products))

    for i in range(0, len(products)):
        products[i].filters.size = list((products[i].filters.size).split(", "))

    data = cartData(request)
    cartItems = data['cartItems']
    user = data['user']

    context = {"products": products, 'cartItems': cartItems, 'user': user, "filters": filters}
    
    return render(request, 'store/category_shirt.html', context)


def categoryWatch(request):
    picked_products = []
    filters = {}

    filters["min_price"] = request.POST.get('min_price')
    filters["max_price"] = request.POST.get('max_price')

    if(filters["max_price"] and filters["min_price"]):
        if(int(filters["max_price"]) < int(filters["min_price"])):
            messages.info(request, 'Incorrect values for price interval')
        else:
            tmp_products = Product.objects.filter(category="watches")
            for product in tmp_products:
                if(product.price >= int(filters["min_price"]) and product.price <= int(filters["max_price"])):
                    picked_products.append(product.name)
    
    if len(picked_products) == 0: 
        products = Product.objects.filter(category="watches")  
    else:
        products = Product.objects.filter(name__in=picked_products)

    data = cartData(request)
    cartItems = data['cartItems']
    user = data['user']

    context = {"products": products, 'cartItems': cartItems, 'user': user, "filters": filters}
    
    return render(request, 'store/category_watch.html', context)


def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    user = data['user']

    context = {'cartItems': cartItems, 'user': user}

    return render(request, 'store/contact.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = data['user']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'user': user}

    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = data['user']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'user': user}

    return render(request, 'store/checkout.html', context)


def register(request):
    data = cartData(request)
    user = data['user']
    cartItems = data['cartItems']

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            customer, created = Customer.objects.get_or_create(username=request.POST.get('username'),
                                                      name=request.POST.get('name'), email=request.POST.get('email'),
                                                      password=request.POST.get('password2'), address=request.POST.get('address'),
                                                      city=request.POST.get('city'), psc=request.POST.get('psc'),
                                                      country=request.POST.get('country'))
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')
            user_login = authenticate(request, username=username, password=password)

            if user_login is not None:
                login(request, user_login)
                customer = Customer.objects.get(username=username)
                filled_form = {'username':customer.username, 'name': customer.name, 'email': customer.email,
                               'address': customer.address,
                               'city': customer.city, 'psc': customer.psc, 'country': customer.country}
                form = RegisterForm(initial=filled_form)

                return redirect('/')
        else:
            if("password is too common" in str(form.errors)):
                messages.error(request, "Password is too common.")
            elif("password fields didn’t match" in str(form.errors)):
                messages.error(request, "Password fields didn't match.")
            elif("username already exists" in str(form.errors)):
                messages.error(request, "Username already exists.")
            filled_form = {'username':request.POST.get('username'),
                           'name':request.POST.get('name'),
                           'email':request.POST.get('email'),
                           'address':request.POST.get('address'),
                           'city':request.POST.get('city'),
                           'psc':request.POST.get('psc'),
                           'country':request.POST.get('country')}
            form = RegisterForm(initial=filled_form)
            context = {'form': form, 'cartItems': cartItems, 'user': user}

            return render(request, 'store/register.html', context)
    else:
        form = RegisterForm()
        context = {'form': form, 'cartItems': cartItems, 'user': user}

        return render(request, 'store/register.html', context)


def login_request(request):
    data = cartData(request)
    user = data['user']
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                customer = Customer.objects.get(username=request.user)
                filled_form = {'name': customer.name, 
                               'email': customer.email, 
                               'address': customer.address,
                               'city': customer.city, 
                               'psc': customer.psc, 
                               'country': customer.country}
                form = RegisterForm(initial=filled_form)

                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    cartItems = data['cartItems']
    context = {"login_form": form, "user": user, "cartItems": cartItems}

    return render(request, "store/login_page.html", context)


def logout_request(request):
    logout(request)
    return redirect('/')


def profile(request):
    products = []
    item =  []
    history_products = []
    
    if request.method == "POST":
        form = ProfileForm(request.POST)
        
        if form.is_valid():
            obj = Customer.objects.get(username=request.POST.get('username'))
            obj.name = request.POST.get('name')
            obj.email = request.POST.get('email')
            obj.address = request.POST.get('address')
            obj.city = request.POST.get('city')
            obj.psc = request.POST.get('psc')
            obj.country = request.POST.get('country')
            obj.save()
        else:
            messages.error(request, "Password is too common")
        
        customer = Customer.objects.get(username=request.POST.get('username'))
        filled_form = {'name': customer.name, 
                       'email': customer.email, 
                       'address': customer.address,
                       'city': customer.city, 
                       'psc': customer.psc, 
                       'country': customer.country}
        form = ProfileForm(initial=filled_form)
        all_orders = OrderItem.objects.all()
        total_order = Order.objects.filter(customer=customer)

        for i in total_order:
            item =  []
            history_products = []

            for j in all_orders:
                if Order(i.id) == j.order:
                    if(j.size):
                        item.append(j.product.name + " " + j.size +" " + str(j.quantity))
                    else:
                        item.append(j.product.name + " " + str(j.quantity))

            if i.complete:
                history_products.append(i.date_order)
                history_products.append(i.total)
                history_products.append(item)
                products.append(history_products)

        history = {'products': products}
        data = cartData(request)
        cartItems = data['cartItems']
        context={"form": form, 'data': data, 'user': customer, 'history': history, "cartItems": cartItems}

        return render(request, "store/profile.html", context)
    else:
        data = cartData(request)
        customer = Customer.objects.get(username=request.user)
        filled_form = {'name':customer.name, 
                       'email':customer.email, 
                       'address':customer.address, 
                       'city': customer.city, 
                       'psc':customer.psc, 
                       'country':customer.country}
        form = ProfileForm(initial=filled_form)
        all_orders = OrderItem.objects.all()
        total_order = Order.objects.filter(customer=customer)
        
        for i in total_order:
            item =  []
            history_products = []

            for j in all_orders:
                if Order(i.id) == j.order:
                    if(j.size):
                        item.append(j.product.name + " Size:" +j.size +" " + str(j.quantity))
                    else:
                        item.append(j.product.name + " " + str(j.quantity))

            if i.complete:
                history_products.append(i.date_order)
                history_products.append(i.total)
                history_products.append(item)
                products.append(history_products)

        history = {'products': products}
        cartItems = data['cartItems']
        context={"form": form, 'data': data, 'user': customer, 'history': history, "cartItems": cartItems}

        return render(request, "store/profile.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = Customer.objects.get(username=request.user)
    
    if(any(filter(lambda x: x in productId, SIZES))):
        idOnly = ''.join(c for c in productId if c.isdigit())
        idSize = ''.join(c for c in productId if not c.isdigit())
        product = Product.objects.get(id=idOnly)
    else:
        product = Product.objects.get(id=productId)
        idSize = ""
    
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, size=idSize)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = Customer.objects.get(username = request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    order.total = total

    if float(total) == float(order.get_cart_total):
        order.complete = True
    order.save()

    return JsonResponse('Payment complete', safe=False)
