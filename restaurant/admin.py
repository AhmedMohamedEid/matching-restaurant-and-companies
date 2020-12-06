from django.contrib import admin

from .models import Profile, restaurant, companies, Category, Product ,Reviewer, Order


admin.site.register(Order)
admin.site.register(Reviewer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(restaurant)
admin.site.register(companies)
