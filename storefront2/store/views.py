from django.db.models.aggregates import Count
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import CollectionSerializers, ProductSerializers
# Create your views here.

@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
    
    product = get_object_or_404(Product,pk=id)
    if request.method == 'GET':
        serializer = ProductSerializers(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializers(product,data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitem_set.count()>0:
            return Response({'error':'product can not be deleted , it was associated with order'})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializers(queryset,many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializers(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data
            return Response(serializer.data,status=status.HTTP_201_CREATED)
@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(product_count=Count('products')).all()
        serializer = CollectionSerializers(queryset,many=True)
        return Response(serializer.data)
    
    elif  request.method == 'POST':
        serializer = CollectionSerializers(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("saved successfully")



@api_view(['GET','PUT','DELETE'])
def collection_detail(request,id):
    if request.method == 'GET':
        collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')),pk=id)
        serializer = CollectionSerializers(collection)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        collection = get_object_or_404(Collection,pk=id)
        serializer = CollectionSerializers(collection,data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Sucessfully updated')
        
    elif request.method == 'DELETE':
        collection = get_object_or_404(Collection,pk=id)
        if collection.products.count()>0:
            return Response('cannot delete , one or more products are associated with this collection')
        collection.delete()
        return Response('collection deleted ')
        


     
        

def test(request):
    return HttpResponse("testing...")
