from django.db import models
from django.urls import reverse
from Cbonshop.settings import AUTH_USER_MODEL
from django.utils.translation import gettext_lazy

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
        return self.quantity * self.products.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
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
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    def is_empty(self):
        return self.orders.count() == 0
    