from urllib import response
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializers
# Create your views here.

@api_view(['GET','PUT'])
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

       


     
        

def test(request):
    return HttpResponse("testing...")
