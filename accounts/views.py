from django.shortcuts import render,redirect,get_object_or_404,Http404
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from accounts.models import Shopper
from store.models import product,Cart,Order
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignUpForm
from django.utils.translation import gettext as _



User = get_user_model()

def signup(request):
    form = SignUpForm(request.POST)
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
    # formulaire d'inscription 
            username= form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            #email = form.cleaned_data["email"]
            user = authenticate( username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request,_('Inscriptions réussit'))
            return redirect (_('index'))
    else:
        form= SignUpForm()
        
    return render(request,'account/signup.html',{'form':form})


#reconnexion
def login_user(request):
    if request.method == "POST":
    # formulaire de connexion 
            username= request.POST["username"]
            password = request.POST["password"]

            user= authenticate(username=username, password=password)
            if user:
                login(request, user )
                return redirect(_('index'))

    return render(request, 'account/login.html') 
       
#deconexion
def logout_user(request):
    logout(request)
    return redirect (_('index'))

def add_to_cart(request,slug):
    user= request.user
    products= get_object_or_404(product, slug=slug )
    cart, _ = Cart.objects.get_or_create(user=user)
    order,created =  Order.objects.get_or_create(user=user , products=products)
    product_price = products.price
    
    if created:
        cart.orders.add(order)
        messages.success(request, "Produit ajouter avec succes")
    else:
        cart.total_price += product_price
        order.quantity += 1
        order.save()

    return redirect( _(reverse( "product", kwargs= {"slug": slug} )))
#afficher un message pour panier vide
def empty_cart(request):
    return render (_(request, 'store/empty_cart.html'))

#afficher le contenue du panier
def cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        if cart.orders.exists():
            order_count = Order.objects.filter(user=user).count()
            context = {"order_count": order_count, "cart": cart}
            return render(request, 'store/cart.html', context)
        else:
            raise Http404("Cart is empty")
    except ObjectDoesNotExist:
        return redirect (_('empty_cart') )
    


#supprimer l'order du clients
def delete_cart (request):
  if request.user.is_authenticated :     
    if cart :=request.user.cart:         
        cart.orders.all().delete()
        cart.delete()
        return redirect (_('empty_cart') )
    else :
        return redirect (_('empty_cart') )
        



