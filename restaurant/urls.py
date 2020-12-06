from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('joinas/<value>', views.joinas, name='joinas'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('logout_page', views.logout_page, name='logout_page'),
    path('menu', views.menu, name='menu'),
    path('product/<int:id>', views.product, name='product'),
    path('order', views.order, name='order'),
    path('new/order', views.add_order, name='add_order'),
    path('order/company/<company_id>', views.order_company, name='order_company'),
    path('newproduct', views.add_product, name='add_product'),
    path('company', views.all_company, name='companies'),
    path('users', views.users, name='users'),
    path('profile', views.user_profile, name='user_profile'),
    path('info', views.restaurant_profile, name='restaurant_profile'),
    path('add', views.add_restaurant, name='add_restaurant'),
    path('add/company', views.add_company, name='add_company'),
    path('company/restaurant', views.order_rest, name='order_rest'),
    path('company/restaurant/<int:rest_id>', views.order_company_to_rest, name='order_company_to_rest'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
