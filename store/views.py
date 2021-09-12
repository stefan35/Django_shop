from django.shortcuts import render, redirect
import json
import datetime
from .models import *
from .utils import cartData, guestOrder
from .forms import RegisterForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    user = data['user']
    products = Product.objects.all()

    context = {'products':products, 'cartItems':cartItems, 'user':user}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = data['user']

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'user':user}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = data['user']

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'user':user}
    return render(request, 'store/checkout.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            customer, created_customer = Customer.objects.get_or_create(username=request.POST.get('username'),
                                                                        name=request.POST.get('name'), email=request.POST.get('email'),
                                                                        password=request.POST.get('password2'), address=request.POST.get('address'),
                                                                        city=request.POST.get('city'), psc=request.POST.get('psc'),
                                                                        country=request.POST.get('country'))
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')
            user_login = authenticate(request, username=username, password=password)
            if user_login is not None:
                login(request, user_login)
                customer = Customer.objects.get(name=form.cleaned_data.get('name'))
                filled_form = {'username':customer.username, 'name': customer.name, 'email': customer.email,
                               'address': customer.address,
                               'city': customer.city, 'psc': customer.psc, 'country': customer.country}
                form = RegisterForm(initial=filled_form)
                customer_orders = Order.objects.filter(customer=customer)
                all_orders = OrderItem.objects.all()
                history_orders = {'customer_orders': customer_orders, 'all_orders': all_orders}
                return redirect('/')
        else:
            messages.error(request, "The password is too common.")
            filled_form = {'username':request.POST.get('username'),
                               'name':request.POST.get('name'),
                               'email':request.POST.get('email'),
                               'address':request.POST.get('address'),
                                'city':request.POST.get('city'),
                               'psc':request.POST.get('psc'),
                                'country':request.POST.get('country')}
            form = RegisterForm(initial=filled_form)
            context = {'form': form}
            return render(request, 'store/register.html', context)
    else:
        form = RegisterForm()
        context = {'form':form}
        return render(request, 'store/register.html', context)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                data = cartData(request)
                customer = Customer.objects.get(username=request.user)
                filled_form = {'name': customer.name, 'email': customer.email, 'address': customer.address,
                               'city': customer.city, 'psc': customer.psc, 'country': customer.country}
                form = RegisterForm(initial=filled_form)
                customer_orders = Order.objects.filter(customer=customer)
                all_orders = OrderItem.objects.all()
                history_orders = {'customer_orders': customer_orders, 'all_orders': all_orders}

                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request=request, template_name="store/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    return redirect('/')


def profile(request):
    if request.method == "POST":
        try:
            obj = Customer.objects.get(username=request.POST.get('username'))
            obj.name = request.POST.get('user_name')
            obj.email = request.POST.get('user_email')
            if request.POST.get('user_password2') != '':
                obj.password = make_password(request.POST.get('user_password2'))
            obj.address = request.POST.get('user_address')
            obj.city = request.POST.get('user_city')
            obj.psc = request.POST.get('user_psc')
            obj.country = request.POST.get('user_country')
            obj.save()

            obj1 = User.objects.get(username=request.POST.get('username'))
            obj1.name = request.POST.get('user_name')
            if request.POST.get('user_password2') != '':
                obj1.password = make_password(request.POST.get('user_password2'))
            obj1.save()
        except Customer.DoesNotExist:
            print("cant match user")

        data = cartData(request)

        customer = Customer.objects.get(username=request.POST.get('username'))
        filled_form = {'name': customer.name, 'email': customer.email, 'address': customer.address,
                       'city': customer.city, 'psc': customer.psc, 'country': customer.country}
        form = RegisterForm(initial=filled_form)
        all_orders = OrderItem.objects.all()
        total_order = Order.objects.filter(customer=customer)

        products = []
        item = []
        date = []
        is_date = False
        for i in total_order:
            item = []
            date = []
            is_date = False
            for j in all_orders:
                if Order(i.id) == j.order:
                    item.append(j.product.name + " " + str(j.quantity))
                    is_date = True
            if is_date:
                date.append(i.date_order)
                date.append(i.total)
                date.append(item)
                products.append(date)
                is_date = False
        history = {'products': products}
        return render(request=request, template_name="store/profile.html",
                      context={"login_form": form, 'data': data, 'user': customer, 'history': history})
    else:
        data = cartData(request)
        customer = Customer.objects.get(username=request.user)
        filled_form = {'name':customer.name, 'email':customer.email, 'address':customer.address, 'city': customer.city, 'psc':customer.psc, 'country':customer.country}
        form = RegisterForm(initial=filled_form)
        all_orders = OrderItem.objects.all()
        total_order = Order.objects.filter(customer=customer)

        products = []
        item = []
        date = []
        is_date = False
        for i in total_order:
            item = []
            date = []
            is_date = False
            for j in all_orders:
                if Order(i.id) == j.order:
                    item.append(j.product.name + " " + str(j.quantity))
                    is_date = True
            if is_date:
                date.append(i.date_order)
                date.append(i.total)
                date.append(item)
                products.append(date)
                is_date = False
        history = {'products':products}
        return render(request=request, template_name="store/profile.html",
                      context={"login_form": form, 'data': data, 'user': customer, 'history': history})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = Customer.objects.get(username=request.user)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, creted = OrderItem.objects.get_or_create(order=order, product=product)

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
