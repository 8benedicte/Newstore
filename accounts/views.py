from django.shortcuts import render,redirect,get_object_or_404,Http404
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from accounts.models import Shopper
from store.models import product,Cart,Order,CheckoutAddress,Payment
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignUpForm, CheckoutForm
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
    if request.user.is_authenticated:
        if created:  
            cart.orders.add(order_item)
            messages.info(request, "Produit ajouté avec succès")
        elif order_item in cart.orders.all():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Ce produit est rajouté avec succès.")
        else:  
            cart.orders.add(order_item)
            messages.info(request, "Produit ajouté avec succès")
    else:
        messages.info(request, "Vous devez vous connecter pour voir votre panier.")
       
    return redirect(reverse("product_detail", kwargs={"slug": slug}))




#afficher un message pour panier vide
def empty_cart(request):
    return render (_(request, 'store/empty_cart.html'))

#afficher le contenue du panier

def cart(request):
    mycart = Cart.objects.filter(user=request.user)
    order = Order.objects.filter(user=request.user)
    products =  product.objects.all()


    context = {
        "mycart":mycart,
        "order": order,
        "products":products
    }

    return render(request, "store/cart.html", context)

#supprimer l'order du clients

def delete_cart(request, order_id):
    # Récupérer l'objet Order à supprimer
    order = get_object_or_404(Order, id=order_id)

    # Vérifier si l'utilisateur est autorisé à supprimer cet élément du panier
    if request.user.is_authenticated:
        # Supprimer l'objet Order du panier
        order.delete()
        messages.success(request, "Produit supprimé du panier.")
    else :
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cet élément du panier.")
    return redirect('cart')



def validate_cart_via_whatsapp(request):
    # Récupérer les détails du panier (liste des produits et total)
    cartitems = Cart.objects.filter(user=request.user)
    totalprice = sum(cart.get_total() for cart in cartitems)
    products_list = "\n".join([cart.product_fetch() for cart in cartitems ])

    # Générer le message WhatsApp avec les détails du panier
    whatsapp_message = f"Salut j'aimerais valider mon panier contenant :\n{products_list}\nd'un total de {totalprice}"
 
    # Rediriger vers WhatsApp avec le message pré-rempli
    return redirect(f'https://api.whatsapp.com/send/?phone=22893061107&text={whatsapp_message}')

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        cartitems = Cart.objects.filter(user=self.request.user)
        totalprice = sum(cart.get_total() for cart in cartitems)

        products = product.objects.all()

        context = {
            "cartitem": cartitems,
            "totalprice": totalprice,
            "products": products,
            "form": form,  
        }
        return render(self.request, 'store/checkout.html', context)
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.filter(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionaly for these fields
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid Payment option")
                    return redirect('store/checkout.html')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("cart")


"""

def checkout(request):
    print("hey i'm here")
    cartitem= Cart.objects.filter(user=request.user)
    
    products =  product.objects.all()
    
    totalprice=0
    for rawcart in cartitem:
     totalprice += rawcart.get_total()
    context={
        "cartitem":cartitem,
        "totalprice":totalprice,
        "products":products
        
        
    }
    return render(request, "store/checkout.html", context)
class CheckoutView(View):
  def get(self, *args, **kwargs):
        form = CheckoutForm()


        context = {
            'form': form,
        }
        return render(self.request, 'store/checkout.html', context)
 
  
  def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.filter(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionaly for these fields
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()

                if payment_option == 'S':
                    return redirect('store/payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('store/payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid Payment option")
                    return redirect('store/checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("store/cart")
"""