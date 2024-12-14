from django.db.models.aggregates import Count
from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,mixins
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import OrderItem, Product,Collection
from .serializers import CollectionSerializers, ProductSerializers


#using viewset
class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'product can not be deleted , it was associated with order'})
        return super().destroy(request, *args, **kwargs)
    

    


class CollectionViewset(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializers

    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.products.count()>0:
            return Response('cannot delete , one or more products are associated with this collection')

        return super().destroy(request, *args, **kwargs)
    
    # def delete(self,request,pk):
    #     collection = get_object_or_404(Collection,pk=pk)
    #     if collection.products.count()>0:
    #         return Response('cannot delete , one or more products are associated with this collection')
    #     collection.delete()
    #     return Response('collection deleted ')




#using genreicviews with mixins
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers
    
#     def get_serializer_context(self):
#         return {'request':self.request}
    
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers


#     def delete(self,request,pk):    
#         product = get_object_or_404(Product,pk=pk)
#         if product.orderitem_set.count()>0:
#             return Response({'error':'product can not be deleted , it was associated with order'})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(product_count=Count('products')).all()
#     serializer_class = CollectionSerializers

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(product_count=Count('products')).all()
#     serializer_class = CollectionSerializers

#     def delete(self,request,pk):
#         collection = get_object_or_404(Collection,pk=pk)
#         if collection.products.count()>0:
#             return Response('cannot delete , one or more products are associated with this collection')
#         collection.delete()
#         return Response('collection deleted ')



#class based views
# class ProductList(APIView):
#     def get(self,request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializers(queryset,many = True)
#         return Response(serializer.data)

#     def post(self,request):
#         serializer = ProductSerializers(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
    

# class ProductDetail(APIView):
#     def get(self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         serializer = ProductSerializers(product)
#         return Response(serializer.data)
    
#     def put(self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         serializer = ProductSerializers(product,data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         if product.orderitem_set.count()>0:
#             return Response({'error':'product can not be deleted , it was associated with order'})
#         self.product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

        
# class CollectionList(APIView):
#     def get(self,request):
#         queryset = Collection.objects.annotate(product_count=Count('products')).all()
#         serializer = CollectionSerializers(queryset,many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = CollectionSerializers(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response("saved successfully")

# class CollectionDetail(APIView):
#     def get(self,request,id):
#         collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')),pk=id)
#         serializer = CollectionSerializers(collection)
#         return Response(serializer.data)
    

#     def put(self,request,id):
#         collection = get_object_or_404(Collection,pk=id)
#         serializer = CollectionSerializers(collection,data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('Sucessfully updated')
    
#     def delete(self,request,id):
#         collection = get_object_or_404(Collection,pk=id)
#         if collection.products.count()>0:
#             return Response('cannot delete , one or more products are associated with this collection')
#         collection.delete()
#         return Response('collection deleted ')


# @api_view(['GET','PUT','DELETE'])
# def product_detail(request,id):
    
#     product = get_object_or_404(Product,pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializers(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializers(product,data = request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitem_set.count()>0:
#             return Response({'error':'product can not be deleted , it was associated with order'})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializers(queryset,many = True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = ProductSerializers(data = request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.validated_data
#             return Response(serializer.data,status=status.HTTP_201_CREATED)


# @api_view(['GET','POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(product_count=Count('products')).all()
#         serializer = CollectionSerializers(queryset,many=True)
#         return Response(serializer.data)
    
#     elif  request.method == 'POST':
#         serializer = CollectionSerializers(data = request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response("saved successfully")



# @api_view(['GET','PUT','DELETE'])
# def collection_detail(request,id):
#     if request.method == 'GET':
#         collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')),pk=id)
#         serializer = CollectionSerializers(collection)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         collection = get_object_or_404(Collection,pk=id)
#         serializer = CollectionSerializers(collection,data = request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response('Sucessfully updated')
        
#     elif request.method == 'DELETE':
#         collection = get_object_or_404(Collection,pk=id)
#         if collection.products.count()>0:
#             return Response('cannot delete , one or more products are associated with this collection')
#         collection.delete()
#         return Response('collection deleted ')
        


     
    