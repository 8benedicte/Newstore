"""
URL configuration for test_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from store.views import index,ProductListView,CategoryListviews,SubCategoryListviews,ProductPackListviews,packproductindex,product_detail, about_us,error_404_view,validate_product_via_whatsapp
from accounts.views import signup,cart,login_user,empty_cart,delete_cart,logout_user,add_to_cart,CheckoutView,validate_cart_via_whatsapp
from Cbonshop import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

handler404 = error_404_view


urlpatterns =[
    path("__debug__/", include("debug_toolbar.urls")),
    path('i18n/', include('django.conf.urls.i18n')),
    path('about/', about_us,name='about'),
    path('',index,name='index'),
    path('product_list/',ProductListView.as_view(),name="product_list"),
    path('product/<slug:slug>/whatsapp/', validate_product_via_whatsapp, name='validate_product_via_whatsapp'),
    path('pack_list_detail/<int:id>/',ProductPackListviews.as_view(), name="pack_list_detail"),
    path('product/<slug:slug>/', product_detail, name='product'),
    path('subcategory/<int:id>/', SubCategoryListviews.as_view(),name='subcategory'),
    path('categories/<int:id>/', CategoryListviews.as_view(), name='category_list'),
    path('product/<int:id>/',product_detail, name="product"),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('product/<int:id>/add_to_cart/',add_to_cart, name="add_to_cart"),
    path('signup/', signup,name='signup'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart ,name='cart'),
    path('via_whatsapp/', validate_cart_via_whatsapp ,name='validate_cart_via_whatsapp'),
    path('cart/empty/', empty_cart,name='empty_cart'),
    path('cart/delete/', delete_cart,name='delete_cart'),
    path('cart/delete/<int:order_id>/', delete_cart, name='delete_cart'),
    path('logout/', logout_user ,name='logout'),
    path('login/', login_user ,name='login'),
    path('pack_list',packproductindex,name='pack_list'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static( settings.STATIC_URL)


urlpatterns += i18n_patterns (
    path('',include('store.urls',namespace='store')),
    path('admin/', admin.site.urls),
    path('about/', about_us,name='about'),
    path('',index,name='index'),
    prefix_default_language=False,

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)











