from django.contrib import admin
from .models import CustomerDetail, Comic, Publisher, Reviews, Cart, Order, Rental_system

# Register your models here.

@admin.register(CustomerDetail)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','address','city','state','pincode']

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ['id','name','category','description','original_price','discounted_price','rent_price','comic_image']

@admin.register(Cart)
class ComicAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']


@admin.register(Order)
class ComicAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','comic','quantity','order_at','status']


@admin.register(Reviews)
class ComicAdmin(admin.ModelAdmin):
    list_display = ['id','user','reviews_on_comic','user_review','review_date','number_of_stars']


@admin.register(Publisher)
class ComicAdmin(admin.ModelAdmin):
    list_display = ['id','comic_publisher','published_comic','published_at','number_chapters','status','publisher_brand_logo']

@admin.register(Rental_system)
class RentalSystemAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'comic', 'rent_start_date', 'rent_end_date', 'rental_status', 'rental_plan']