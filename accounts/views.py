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
from django.contrib.auth.decorators import login_required


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

def add_to_cart(request, slug):
    user = request.user
    products = get_object_or_404(product, slug=slug)
    cart, created = Cart.objects.get_or_create(user=user, ordered=False)
    order_item, created = Order.objects.get_or_create(user=user, products=products, ordered=False)  # Utilisez product_id au lieu de products
    if created:  
        cart.orders.add(order_item)
        messages.info(request, "Produit ajouté avec succès")
    elif order_item in cart.orders.all():  
        messages.info(request, "Ce produit est déjà dans votre panier.")
    else:  
        cart.orders.add(order_item)
        messages.info(request, "Produit ajouté avec succès")
    return redirect(reverse("product_detail", kwargs={"slug": slug}))




#afficher un message pour panier vide
def empty_cart(request):
    return render (_(request, 'store/empty_cart.html'))

#afficher le contenue du panier
def cart(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
            if cart.orders.exists():
                context = {"cart": cart}
                return render(request, 'store/cart.html', context)
            else:
                messages.info(request, "Le panier est vide.")
                return render(request, 'store/empty_cart.html')
        except Cart.DoesNotExist:
            messages.info(request, "Le panier est vide.")
            return render(request, 'store/empty_cart.html')
    else:
        messages.info(request, "Vous devez vous connecter pour voir votre panier.")
        return redirect('login')  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté

    return render(request, 'base.html', context)

#supprimer l'order du clients
def delete_cart(request, slug):
    products = get_object_or_404(product, slug=slug)
    order_qs = Cart.objects.filter(user=request.user, ordered=False)
    orders = Order.objects.filter(products=product, user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if orders.exists():
            order_item = Order.objects.get(products=product, user=request.user, ordered=False)
            order_item.delete()
            messages.info(request, "Produit supprimé du panier.")
        else:
            messages.info(request, "Le produit n'est pas dans votre panier.")
    else:
        messages.info(request, "Le panier est vide.")
    return redirect('cart')  # Rediriger vers la page du panier après suppression du produit



