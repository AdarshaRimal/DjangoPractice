from decimal import Decimal
from rest_framework import serializers

from .models import Cart, CartItem, Product,Collection, Review

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

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']   

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,cartitem:CartItem):
        return cartitem.quantity * cartitem.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']


    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True,read_only = True)
    total_price = serializers.SerializerMethodField()
    def get_total_price(self, cart:Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    id = serializers.UUIDField(read_only = True)

    class Meta:
        model = Cart
        fields = ['id','items','total_price']

class AddCartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()

    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product found with this id')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            #item exist upate here
            cart_item = CartItem.objects.get(cart_id = cart_id,product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            #there is no any item so new item
            self.instance = CartItem.objects.create(cart_id = cart_id,**self.validated_data) #from self.validated data product_id,quantity is unpacked for instance of cartitem

        return self.instance
    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']