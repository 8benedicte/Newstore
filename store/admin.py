from django.contrib import admin
from store.models import product,Order,Cart,Category,SubCategory,ProductPack

# Register your models here.

admin.site.register(product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ProductPack)

