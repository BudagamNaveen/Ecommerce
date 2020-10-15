"""ecomsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
from users import views as UserViews
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),

    #Shop App Url's
    path('', views.HomePage,name='index'),
    path('DetailView/<id>', 
        views.DetailView,
        name='DetailView'),
    path('Addtocart/<id>', 
        views.Addtocart,
        name='Addtocart'),
    path('searchfunction/<title>', 
        views.searchfunction,
        name='searchfunction'),
    path('Pagination/<objectset>', 
        views.Pagination,
        name='Pagination'),
    path('cartcount', 
        views.cartcount,
        name='cartcount'),
    path('SubCatergory_View/<id>', 
        views.SubCatergory_View,
        name='SubCatergory_View'),
    path('Products_View/<id>', 
        views.Products_View,
        name='Products_View'),
    path('Sortingfunc/<id>', 
        views.Sortingfunc,
        name='Sortingfunc'),
    path('Increment_cart_quantity/<id>', 
        views.Increment_cart_quantity,
        name='Increment_cart_quantity'),
    path('Ordersummary', 
        views.Ordersummary,
        name='Ordersummary'),
    path('remove_single_item_from_cart/<id>', 
        views.remove_single_item_from_cart,
        name='remove_single_item_from_cart'
        ),
    path('RemoveFromcart/<id>', 
        views.RemoveFromcart,
        name='RemoveFromcart'
        ),
    path('checkout', 
        views.checkout,
        name='checkout'),


    #Users App Url's
    path('Registration/', 
        UserViews.Registration,
        name='Registration'),
    path('Profile/', 
        UserViews.Profile,
        name='Profile'),
    path('Login/', 
        auth_views.LoginView.as_view(template_name='users/Login.html'),
        name='Login'),
    path('Logout/', 
        auth_views.LogoutView.as_view(template_name='users/Logout.html'),
        name='Logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)