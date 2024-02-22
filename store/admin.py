from django.contrib import admin
from store.models import product,Order,Cart,Category,SubCategory,ProductPack

# Register your models here.


admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ProductPack)

@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','prices','discount_price')
    actions = ['discount_30']

    def discount_30(self, request, queryset):
        from math import ceil
        discount = 30  # percentage

        for products in queryset:
            """ Set a discount of 30% to selected products """
            multiplier = discount / 100.  # discount / 100 in python 3
            old_price = products.prices
            new_price = ceil(old_price - (old_price * multiplier))
            products.discount_price = new_price
            products.save(update_fields=['discount_price'])
    discount_30.short_description = 'Set 30%% discount'
