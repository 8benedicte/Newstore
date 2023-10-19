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
    instock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to ="products",blank=True ,null=True)
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})
    
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
    user= models.ForeignKey(AUTH_USER_MODEL,on_delete= models.CASCADE)
    products= models.ForeignKey( product ,on_delete=models.CASCADE, related_name="order")
    quantity= models.IntegerField(default=1)
    ordered = models.BooleanField( default=False)
    #cart = models.ForeignKey ( Cart,on_delete= models.CASCADE)
    def __str__(self):
        return f"{self.products} ({self.user.username})"
    
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
    #products = models.ForeignKey ( product,on_delete=models.CASCADE )

    def __str__(self):
        return self.user.username
    def is_empty(self):
        return self.orders.count() == 0
    