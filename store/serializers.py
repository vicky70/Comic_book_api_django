from rest_framework import serializers
from .models import Comic, CustomerDetail, Cart, Order,Reviews, Publisher, Rental_system
from django.contrib.auth.models import User

# @     ()

class CustomerDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetail
        fields = ['user','name','address','city','state','pincode']

class ComicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']

        def create(self, validate_data):
            user = User.objects.create_user(
                username=validate_data['username'],
                email=validate_data['email'],
                password=validate_data['password']
            )
            return user

class ComicSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ['id','name','category', 'description', 'original_price', 'discounted_price','rent_price','comic_image']
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user','product','quantity']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user','customer','comic','quantity','order_at','status']

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['user','reviews_on_comic','user_review','review_date','number_of_stars']
        extra_kwargs = {
            'user': {'read_only':True},
            'reviews_on_comic': {'read_only': True}
        }

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['comic_publisher','published_comic','published_at','number_chapters','status','publisher_brand_logo']

class Rental_systemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental_system
        fields = ['user','comic','rent_start_date', 'rent_end_date','rental_status','rental_plan']
