from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

# Forms

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.translation import gettext as _

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

from django.contrib.auth.models import User
from .forms import UserForm, ProfileForm , RestaurantForm ,CategForm, ProductForm, CompanyForm, OrderForm
from .models import restaurant, companies, Profile, Category, Product, Reviewer ,Order
#
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})
#

def joinas(request, value):
    if request.method == 'POST':
        type = request.POST['type']

        restaurant_id = request.POST['restaurant']
        return render(request, "restaurant/signup.html", {'type': type, 'position_id': restaurant_id})
    else:
        if value == "company":
            res = companies.objects.all()
            return render(request, "restaurant/joinas.html", {'companies': res , 'from' : value})
        elif value == "restaurant":
            res = restaurant.objects.all()
            return render(request, "restaurant/joinas.html", {'restaurant': res, 'from' : value})
        else:
            value = 'restaurant'
            res = restaurant.objects.all()
            return render(request, "restaurant/joinas.html", {'restaurant': res, 'from' : value})

def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.danger(request, 'Email or Password Invalid')
            return render(request, "restaurant/signin.html")
    else:
        return render(request, "restaurant/signin.html")

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        job = request.POST['job']
        type = request.POST['type']
        position_id = request.POST['position_id']

        is_comp_staff = False
        is_rest_staff = False
        company_id = 0
        restaurant_id = 0
        if type == "restaurant":
            is_rest_staff = True
            restaurant_id = position_id
        else:
            is_comp_staff = True
            company_id = position_id
            # is A Company
        user = User.objects.create_user(username=name,email=email, password=password, is_staff=True)
        if user:
            user.save()
            profile = Profile.objects.create(user=user, phone=phone, job=job, is_comp_staff=is_comp_staff,is_rest_staff=is_rest_staff ,company_id =company_id, restaurant_id=restaurant_id)
            profile.save()
            messages.success(request, 'User Successfuly register Done Can Login')
            return render(request, "restaurant/signin.html")
        elif type == 'company':
            company_id = request.POST['company']
        print(3)
    else:
        return HttpResponseRedirect(reverse("joinas"))

def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse("signin"))



def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("signin"))

    return render(request, "restaurant/index.html")

@login_required
def menu(request):
    res = Product.objects.all()
    for r in res:
        print(r.image)
    # print(res)
    return render(request, "restaurant/menu.html", { 'products': res})

def product(request, id):
    if request.method == 'POST':
        res_product = Product.objects.get(pk=id)
        user_id = request.user
        product_id = res_product
        review = request.POST['reviewer']
        review_rate = request.POST['rate']

        model_create = Reviewer.objects.create(user_id=user_id,product_id=product_id, review=review, star_rate=review_rate)
        print(model_create)
        if model_create:
            model_create.save()
            messages.success(request, _('Your profile was successfully updated!'))
            res_review = Reviewer.objects.all().filter(product_id=res_product)
            # return HttpResponseRedirect(reverse("product"))
        return render(request, "restaurant/product.html", { 'product': res_product, 'product_review':res_review})
    else:
        res_product = Product.objects.get(pk=id)
        res_review = Reviewer.objects.all().filter(product_id=res_product)
        print(res_review)
    return render(request, "restaurant/product.html", { 'product': res_product, 'product_review' : res_review})

@login_required
def order(request):

    company_list = companies.objects.all()
    # for order
    # orders = Order.objects.filter()
    # print(type(company_list))
    context = {
        'company_list': company_list,

    }
    return render(request, "restaurant/order.html", context)


@login_required
def order_company(request, company_id):
    company_list = companies.objects.all()
    restaurant_id = request.user.profile.restaurant_id
    orders = Order.objects.filter(company_id=company_id,restaurant_id=restaurant_id)
    # print(type(company_list))
    context = {
        'company_list': company_list,
        'order_list' : orders,

    }
    return render(request, "restaurant/order.html", context)

@login_required
def order_rest(request):
    rest = restaurant.objects.all()
    return render(request, "restaurant/rest_order.html", {'rest' : rest})

@login_required
def order_company_to_rest(request, rest_id):
    rest = restaurant.objects.all()
    company_id = request.user.profile.company_id
    orders = Order.objects.filter(company_id=company_id,restaurant_id=rest_id)
    context = {
        'rest': rest,
        'order_list' : orders,

    }
    return render(request, "restaurant/rest_order.html", context)


@login_required
def add_order(request):
    if request.method == 'POST':
        # rest_edit = restaurant.objects.get(pk=request.user.profile.restaurant_id.id)
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            obj = order_form.save(commit=False)
            obj.user_id = request.user
            obj.company_id = request.user.profile.company_id

            obj.save()

            messages.success(request, _('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse("order_rest"))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        order_form = OrderForm()
    return render(request, "restaurant/insert/add_order.html", {'order_form':order_form})


@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        # product_form.restaurant_id =
        if product_form.is_valid():
            product_form.save()

            messages.success(request, _('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse("menu"))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        product_form = ProductForm()
    return render(request, "restaurant/add_product.html", {'product_form':product_form})
#****************
@login_required
def all_company(request):
    comp_list = companies.objects.all()
    # restaurant_id = request.user.profile.restaurant_id
    # orders = Order.objects.filter(company_id=company_id,restaurant_id=restaurant_id)

    context = {
        'comp_list':comp_list,
        # 'orders':orders,
        }

    return render(request, "restaurant/companies.html",context )
#****************
def users(request):
    return render(request, "restaurant/users.html")

@login_required
@transaction.atomic
def user_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse("user_profile"))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'restaurant/user_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def restaurant_profile(request):
    if request.method == 'POST':
        rest_edit = restaurant.objects.get(pk=request.user.profile.restaurant_id.id)
        rest_form = RestaurantForm(request.POST, request.FILES, instance = rest_edit)
        if rest_form.is_valid():

            name = rest_form.cleaned_data.get("name")
            img = rest_form.cleaned_data.get("logo")
            # obj = restaurant.objects.create(title = name,img = img

            rest_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse("restaurant_profile"))
        else:
            messages.error(request, _('Please correct the error below.'))
        pass
    else:
        current_user = request.user
        print(current_user.profile.restaurant_id.id)
        # user = Profile.objects.get(user=current_user.profile.phone)
        rest_form = RestaurantForm(instance = restaurant.objects.get(pk=current_user.profile.restaurant_id.id))
        # print(rest_form)
    return render(request, 'restaurant/restaurant.html', {
        'rest_form': rest_form
    })

    # return render(request, "restaurant/restaurant.html")

def add_restaurant(request):

    if request.method == 'POST':
        name = request.POST["name"]
        address = request.POST["address"]
        phone = request.POST["phone"]
        capacity = request.POST["capacity"]
        desc = request.POST["description"]

        rest = restaurant.objects.create(name=name,address=address,phone=phone, capacity=capacity, desc=desc)
        if rest:
            rest.save()
            messages.success(request, 'Restaurant Successfuly register Done')
            # msg = "Restaurant Successfuly register Done"

            return render(request, "restaurant/insert/add_restaurant.html")
    return render(request, "restaurant/insert/add_restaurant.html")

def add_company(request):

    if request.method == 'POST':
        name = request.POST["name"]
        address = request.POST["address"]
        phone = request.POST["phone"]
        desc = request.POST["description"]

        company  = companies.objects.create(name=name,address=address,phone=phone, desc=desc)
        if company:
            company.save()
            messages.success(request, 'Restaurant Successfuly register Done')
            # msg = "Restaurant Successfuly register Done"

            return render(request, "restaurant/insert/add_company.html")

    return render(request, "restaurant/insert/add_company.html")
