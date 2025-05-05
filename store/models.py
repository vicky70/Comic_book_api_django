from django.db import models
from django.contrib.auth.models import User



class CustomerDetail(models.Model):
    STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CT', 'Chhattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TG', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'),
        ('WB', 'West Bengal'),
        ('AN', 'Andaman and Nicobar Islands'),
        ('CH', 'Chandigarh'),
        ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('DL', 'Delhi'),
        ('JK', 'Jammu and Kashmir'),
        ('LA', 'Ladakh'),
        ('LD', 'Lakshadweep'),
        ('PY', 'Puducherry'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # we have created Many-to-one relationship i.e multiple address can be done by one user
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    pincode = models.IntegerField(
        default=0,
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return str(self.id)

class Comic(models.Model):

    CATEGORY_CHOICES = [
        ('DC', 'Dc'),
        ('Marvel', 'Marvel'),
        ('SHUEISHA', 'Shueisha'), 
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description=models.TextField()
    original_price = models.IntegerField()
    discounted_price = models.IntegerField()
    rent_price = models.IntegerField(default=7)
    comic_image =models.ImageField(upload_to='comic_images', null=True)  # As we are using image field we have to intall 'pillow'. And we have to Define MEDIA_URL in settings.py file so that all folder should save in media directory

    def __str__(self):
        return str(self.name)
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Comic, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)       # Quantity cannot be negative so we have used PositiveIntegerField

    def __str__(self):
        return str(self.id)
    
    @property
    def price_and_quantity_total(self):
        return self.product.discounted_price*self.quantity
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return str(self.id)


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviews_on_comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    user_review = models.CharField(max_length=200, null=True, blank=True)
    review_date = models.DateField(auto_now_add=True)
    number_of_stars = models.PositiveIntegerField(default=0)

class Publisher(models.Model):
    comic_status = [
        ('COMPLETED', 'Completed'),
        ('ONGOING', 'Ongoing')
    ]

    PUBLISHER_CHOICES = [
        ('DC', 'Dc'),
        ('MARVEL', 'Marvel'),
        ('SHUEISHA', 'Shueisha'), 
    ]
    comic_publisher = models.CharField(max_length=20, choices=PUBLISHER_CHOICES)
    published_comic = models.ForeignKey(Comic, models.CASCADE, null=True, blank=True)
    published_at = models.DateField()
    number_chapters = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=comic_status, default='ONGOING')
    publisher_brand_logo = models.ImageField(upload_to='brand_images')


class Rental_system(models.Model):
    RENTAL_STATUS = [
        ('ACTIVE', 'active'),
        ('EXPIRED', 'expired'),
        ('NOT ISSUED', 'not issued')
    ]

    RENTAL_PLANS = [
        ('ONE_MONTH', 'one_month'),
        ('THREE_MONTH', 'three_month'),
        ('ONE_MINUTES', 'one minute'),
        ('30_SECONDS', '30_seconds')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    rent_start_date = models.DateTimeField(auto_now_add=True)
    rent_end_date = models.DateTimeField()
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS, default='NOT ISSUED')
    rental_plan = models.CharField(max_length=20, choices=RENTAL_PLANS)


    @property
    def current_time(self):
        return self.rent_start_date.time()


