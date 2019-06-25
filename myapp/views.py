from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponse
from .models import Category, Product, Client, Order
from .forms import OrderForm,InterestForm
from django.shortcuts import render
from django.utils import timezone
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
def home(request):
  return render (request,'myapp/base.html')


def index0(request):
   cat_list = Category.objects.all().order_by('id')[:10]
   return render(request,'myapp/index0.html',{'cat_list':cat_list})
  # prod_list = Product.objects.all().order_by('-price')[:5]
  # response = HttpResponse()
  # heading1 = '<p>' + 'List of categories: ' + '</p>'
  # response.write(heading1)
  # for category in cat_list:
  #   para = '<p>'+ str(category.id) + ': ' + str(category) + '</p>'
  #   response.write(para)
  # heading2 = '<p>' + 'List of top 5 expensive products: ' + '</p>'
  # response.write(heading2)
  # for product in prod_list:
  #   para = '<p>'+ str(product.id) + ': ' + str(product) + '</p>'
  #   response.write(para)
  # return response

def about(request):
  #return HttpResponse('This is an Online Store APP.')
  return render(request, 'myapp/about0.html')

def detail(request, cat_no):
   products = Product.objects.filter(category_id=cat_no)
   category = get_object_or_404(Category,id=cat_no)
   return render(request,'myapp/detail0.html',{'category':category,'products':products})
  # res = HttpResponse()
  # para3 = '<p>' + 'Warehouse location for the Category (' + str(category_details.name) + ') is: ' + str(category_details.warehouse) + '</p>'
  # res.write(para3)
  # heading3 = '<p>' + 'List of products under this category: ' + '</p>'
  # res.write(heading3)
  # for product in product_details:
  #  para4 = '<p>' + str(product.name) + '</p>'
  #  res.write(para4)
  # return res

def index(request,user_id):

  client=Client.objects.get(id=user_id)
  return render(request,'myapp/index.html', {'client':client})

def products(request):
    products = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'products': products})

#def place_order(request):
   # return HttpResponse('You can place an order here')

# view for part -3
def productdetail(request, prod_id):
    proddetail = Product.objects.get(id=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['interested'] == 1:
                proddetail.interested=proddetail.interested+form.cleaned_data['interested']
                proddetail.save()
        return redirect('/myapp/')
    else:
        form = InterestForm()
        return render(request, 'myapp/productdetail.html', {'form': form, 'proddetail': proddetail})
# view for part 2
def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_unit <= order.product.stock:
                order.save()
                p = Product.objects.get(name=order.product.name)
                p.stock = order.product.stock - order.num_unit
                p.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/orderresponse.html', {'msg': msg})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)
        user = Client.objects.filter(username=username).get(password=password)
        print(user)
        if user:
            if user.is_active:
                login(request, user)
                now = datetime.datetime.now()
                lastlogin = now.strftime("%m/%d/%Y, %H:%M:%S")
                request.session['username'] = username
                if not request.session.has_key('last_login'):
                    lastlogin = 'Your last login was more than one hour ago'
                    request.session['last_login'] = lastlogin
                    print(lastlogin)
                    return redirect('../myapp/'+ str(user.id) +'/')
                else:
                    request.session['last_login'] = lastlogin
                    request.session.set_expiry(3600)
                    print(lastlogin)
                    return redirect('../myapp/'+ str(user.id) +'/')
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

def user_logout(request):
    if request.session.has_key('username'):
        del request.session['username']
        return HttpResponseRedirect('../myapp/login')
    else:
        return HttpResponseRedirect('../myapp/login')

def myorders(request):
    if request.session.has_key('username'):
        username = request.session['username']
        myorderlist = Order.objects.filter(Client__username=username)
        return render(request, 'myapp/myorders.html', {'myorderlist': myorderlist})