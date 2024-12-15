from decimal import Decimal
from rest_framework import serializers

from .models import Product,Collection, Review

class CollectionSerializers(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = Collection
        fields = ['id','title','product_count']
        

    


class ProductSerializers(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length= 255)
    # price = serializers.DecimalField(source = 'unit_price', max_digits=6,decimal_places=2)
    #collection = CollectionSerializers()
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    collection = serializers.PrimaryKeyRelatedField(queryset = Collection.objects.all())
     
    class Meta:
        model = Product
        fields = ['id','title','unit_price','price_with_tax','collection','inventory']
        
    
    
    def calculate_tax(self,product:Product):
        return product.unit_price* Decimal(1.1)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['name','description','date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)