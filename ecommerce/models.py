from django.db import models
from django.contrib.auth.models import User  , AbstractUser
from django.conf import settings

# Create your models here.


# class Customer(AbstractUser):
#     profile_picture = models.FileField(upload_to='profile/images', blank=True, null=True, default='profile/images/default_profile_picture.png')
    
#     def __str__(self) -> str:
#         return self.username


class Product(models.Model):
    name = models.CharField(max_length=225)
    image = models.FileField(upload_to='product/images', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE )
    product = models.ForeignKey('Product', on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self)-> str:
        return f'Cart for {self.user.username}'
    
    def line_total(self):
        return self.quantity * self.product.price


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending","Pending"),
       ( "Delivered","Delivered"),
        ("Cancelled", "Cancelled" ),


    ]
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=15)
    total_order_price = models.DecimalField(max_digits=12, decimal_places=2, default= 0 )
    status=  models.CharField(choices = STATUS_CHOICES,default= "Pending", max_length=15  )

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
    def update_total_price(self):
        total_price = sum(detail.total_price for detail in self.orderdetail_set.all())
        self.total_order_price = total_price
        self.save()
    

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total_price()


class WishList(models.Model):
    user= models.ForeignKey(User, on_delete = models.CASCADE  )
    product = models.ForeignKey(Product, on_delete = models.CASCADE)


    def __str__(self) :
        return f"{self.user.username} added {self.product.name} to wishlist"
      

