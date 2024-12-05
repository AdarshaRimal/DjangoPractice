from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from tags.models import TaggedItem
from . import models
from django.db.models import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.

class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request,model_admin):
        return [
            ('low','low'),
            ('high','high')
        ]
    
    def queryset(self, request,queryset:QuerySet):
        if self.value() == 'low':
            return queryset.filter(inventory__lt=10)
        if self.value() == 'high':
            return queryset.filter(inventory__gt=50)




@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['title','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection','last_update',InventoryFilter]
    prepopulated_fields = {
        'description':['slug','title']
    }
    autocomplete_fields = ['collection']
    search_fields = ['title']
    inlines = [TagInline]

    def collection_title(self,product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory <10:
            return 'Low'
        return 'OK'
    
    @admin.action(description="clear inventory")
    def clear_inventory(self,request,queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} products are successfully updated'
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    
    list_display = ['first_name','last_name','membership','order_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']

    
    def order_count(self,customer):
        return customer.order_set.count()

    
    
class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','customer_name']
    list_select_related = ['customer']
    inlines = [OrderItemInline]
    
    

    
    def customer_name(self,order):
        return order.customer.first_name
    
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title','product_count']

    @admin.display(ordering='product_count')
    def product_count(self,collection):
        url = (reverse('admin:store_product_changelist')
               +'?'
               +urlencode({
            'collection__id':str(collection.id)
        }))
               
        return format_html('<a href="{}">{}</a>',url,collection.product_count)
         
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count = Count('product'))