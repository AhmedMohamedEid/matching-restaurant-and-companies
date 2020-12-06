from django import forms
from django.contrib.auth.models import User

from .models import restaurant, Profile, Category, Product, companies, Order

# class RetaurantForm(forms.ModelForm):
#     class Meta:
#         model = restaurant
#         fields = ['name', 'image']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'job', 'is_rest_staff', 'is_comp_staff','company_id', 'restaurant_id')

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = restaurant
        fields = ('name', 'address', 'phone', 'capacity', 'desc', 'logo')
        widgets = {
            'desc': forms.Textarea(attrs={'cols': 22, 'rows': 5}),
            # 'logo': PictureWidget
        }

class CategForm(forms.Form):
    name = forms.CharField(max_length=30)
    desc = forms.CharField(max_length=200,)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = companies
        fields = ('name', 'address', 'phone', 'desc', 'logo')
        widgets = {
            'desc': forms.Textarea(attrs={'cols': 22, 'rows': 5}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image', 'name', 'category_id','price', 'calories', 'fats','desc')
        widgets = {
            'desc': forms.Textarea(attrs={'cols': 22, 'rows': 5}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ( 'restaurant_id','product_id', 'qty')


    # name = forms.CharField(max_length=30)
    # category_id = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
