from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q,Value,F,ExpressionWrapper,DecimalField
from django.db.models.aggregates import Count,Max,Min
from django.db.models.functions import Concat,Lower,Upper
from store.models import Product,OrderItem,Order,Customer
from tags.models import Tag,TaggedItem
from django.contrib.contenttypes.models import ContentType




def say_hello(request):
    # discounted_price = ExpressionWrapper(F('unit_price')*0.9,output_field=DecimalField())
    # queryset = Product.objects.annotate(discounted_price = discounted_price)

    TaggedItem.objects.get_tags_for(Product,1)

    return render(request, 'hello.html', {'name': 'Adarsha',})

 
