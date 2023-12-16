from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,get_object_or_404
from store.models import product,Category,SubCategory,ProductPack
from django.views import generic
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language,activate,gettext




def index (request):
     #get 1 product from every category 
    products =  product.objects.all()
    categorys = Category.objects.all()
    
    #get all category_id
    category_all_ID = Category.objects.values_list('id', flat=True)
    #get all category in one set
    category_products = []
    #show one product for each categry on the home page
    for category_all in category_all_ID  :
        products= product.objects.filter(category= category_all)[:1]
        category_products.append({ 'category': category_all, 'products': products })        
    context={ "products": products, 
              "categorys": categorys,
              "category_products" : category_products
            }

    
    return render (request, "docs/index.html",context)

def product_detail(request,slug):
        products = get_object_or_404(product, slug=slug ) 
        context={"product":products}
        return render (request, "docs/detail.html",context ) 

def packproductindex(request):
        product_pack = ProductPack.objects.all() 
        context={"product_pack":product_pack}
        return render (request, "docs/pack_list.html",context ) 

class ProductListView(generic.ListView):
    model = product 
    template_name = 'docs/product_list.html'
    context= {'products':product}
    
    def get_context_data(self, **kwargs):
        context = super(ProductListView,self).get_context_data(**kwargs)
        categories = Category.objects.all()
        category_products = []
        for category in categories:
            products = product.objects.filter(category=category)
            category_products.append({ 'category': category, 'products': products })
        context['category_products'] = category_products

        return context
    
#the aboutus page function 
def about_us(request):

    return render(request,"docs/about.html") 
   
class  CategoryListviews(generic.ListView):
    model=Category
    context_object_name='category'
    template_name='docs/category_list'

    def get_queryset(self):
        return Category.objects.filter(id=self.kwargs['id'])

    def get_context_data(self, **kwargs) :
        #Recupere le context depuis la superclass
        context= super(CategoryListviews,self).get_context_data(**kwargs)
    
       #Rajouter la liste de category
        categories = Category.objects.filter(id=self.kwargs['id'])
        category_id= self.kwargs['id']
        context['categories']= Category.objects.filter(id=self.kwargs['id'])
        context['category_id'] = self.kwargs['id']
        category_on_id = []
 
        for category in categories:
            products = product.objects.filter(category_id=category_id)
            subcategory = SubCategory.objects.filter(category_id=category_id)
            #pour pouvoir acceder directement au noms des subcategory child de a=ma category_id
            category_on_id.append({ 'category': category, 'products': products , "subcategory":subcategory })
        context['category_on_id'] = category_on_id
        return context
    
#creer un template pour les sub category
class  SubCategoryListviews(generic.ListView):
       model= SubCategory
       template_name= "subcategory_list.html"
       context_object_name="subcategory"
        
       def get_context_data(self, **kwargs) :
            context= super(SubCategoryListviews,self).get_context_data(**kwargs)
            sub_id = self.kwargs['id']
            subcategorie = SubCategory.objects.filter(id=sub_id)
            context['sub_id']=self.kwargs['id']
            context['subcategorie']= SubCategory.objects.filter(id=sub_id)
            sub_link=[]

            for sub_ in subcategorie :
                #pour pouvoir le nom de la category id correspondante
                products = product.objects.filter(id=sub_id)
                category_by_sub = Category.objects.filter(id=sub_id)
                subcategory = SubCategory.objects.filter(id=sub_id)
                sub_link.append({'category_by_sub':category_by_sub,'subcategory':subcategory ,'products':products ,'sub_':sub_})
            context['sub_link']= sub_link
            return context
        
        
class  ProductPackListviews(generic.ListView):
        model=ProductPack
        template_name= "docs/pack_list_detail.html"
        context= { 'product_pack':ProductPack }
   
            
        def get_context_data(self, **kwargs) :
           context= super(ProductPackListviews,self).get_context_data(**kwargs)
           pack_id= self.kwargs['id']
           product_packs=ProductPack.objects.filter(id=pack_id)
           context['product_packs']= ProductPack.objects.filter(id=pack_id)
           context['product_id']= self.kwargs['id']

           products_in_pack=[]
           for product_ in product_packs:
               products= product.objects.filter(id=pack_id)
               products_in_pack.append({"products":products, "product_":product_,"product_packs":product_packs})
           context['products_in_pack']=products_in_pack

           return context
    


