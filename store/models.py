from django.db import models
from django.urls import reverse
from Cbonshop.settings import AUTH_USER_MODEL
from django.utils.translation import gettext_lazy
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
# Create your models here.

#first app product:
      #name'str',price'float',instock,image

class Category(models.Model):
     name=models.CharField(max_length=101)
     parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
     
     def __str__(self) -> str:
         return self.name
     def get_absolute_url(self):
         return reverse("category",kwargs={'slug': self.slug})

class SubCategory(models.Model):
     name = models.CharField(max_length=100)
     category = models.ForeignKey(Category, on_delete=models.CASCADE)


     def __str__(self):
        return self.name 
    
     def get_absolute_url(self):
        return reverse("subcategory", kwargs={'id': self.id}) 

"""

    def __str__(self):
        return self.name


"""   

class product (models.Model):
    name = models.CharField(max_length=128)
    slug= models.SlugField(max_length=228,default='', unique=True)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,default=True,null=False,related_name='products')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=True,null=False,related_name='products')
    prices= models.FloatField(default=0)
    discount_price= models.FloatField(blank=True, null=True)
    instock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to ="product",blank=True ,null=True)
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })
    
class ProductPack (models.Model):
    name= models.CharField(max_length=128)
    prices= models.FloatField(default=0)
    products= models.ManyToManyField(product)
    description = models.TextField(blank=True)
    quantity= models.IntegerField(default=1)
    
    def __str__(self):
        return self.name 
 
''''
-user
-product
-quantiter
-champs de commande
'''
class Order(models.Model):
    user= models.ForeignKey(AUTH_USER_MODEL,on_delete= models.CASCADE,blank=True, null=True)
    ordered= models.BooleanField(default=False)
    products= models.ForeignKey( product ,on_delete=models.CASCADE,blank=True,null=True, related_name="order")
    quantity= models.IntegerField(default=1)
    ordered = models.BooleanField( default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.products.name}"

    def get_total_item_price(self):
        return self.quantity * self.products.prices

    def get_total_discount_item_price(self):
        return self.quantity * self.products.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.products.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
 
    
#pannier(cart)
'''
-user
-articles
-historique de commande
-date de la commande
'''
class Cart (models.Model):
    user = models.OneToOneField( AUTH_USER_MODEL,on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order,related_name='carts' )
    ordered= models.BooleanField(default=False)
    ordered_date = models.DateTimeField( blank=True, null=True)
    products= models.ForeignKey( product ,on_delete=models.CASCADE,blank=True,null=True,related_name="cart")
    #products = models.ForeignKey ( product,on_delete=models.CASCADE )

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.orders.all():
            total += order_item.get_final_price()

        return total
    def product_fetch(self):
        product_list = []
        for order_item in self.orders.all():
            product_list.append(order_item.products.name)  # Ajoutez le nom du produit à la liste
        return ', '.join(product_list) 
    
    def is_empty(self):
        return self.orders.count() == 0
    
    
class CheckoutAddress(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    

class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username