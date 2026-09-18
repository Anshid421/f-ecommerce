from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, null=True,blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    def __str__(self):
        return self.name
    
    
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    
# cart cheeyyan 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #foreign key use cheyyum, user um cart um one to many relationship undu. on_delete=models.CASCADE use cheyyum, user delete cheyyumbo cart items um delete cheyyum.
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1) #cart item um quantity um store cheyyan vendi aanu. negative quantity varathirikkan vendi PositiveIntegerField use cheyyum. default 1 aayi set cheyyum, cart item add cheyyumbo quantity 1 aayi start cheyyum.

    #ith get_total method cheyyan vendi aanu. ith product price um quantity um multiply cheyyum total price kittan vendi aanu.
    def get_total(self):
        return self.product.price * self.quantity #cart item um quantity um multiply cheyyum total price kittan vendi aanu.
    
    def __str__(self): 
        return self.user.username 
    
    
# order information store cheyyan vendi aanu. order cheytha user, order items, total price, order date okke store cheyyum.


# ee model cheyyunne order cheytha user total amount, delivery date ellaaaa store cheyyan vendi aanu. order items store cheyyan vendi OrderItem model undu. order items um product um quantity um price um store cheyyum.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #order cheytha user-inde information store cheyyan vendi aanu. on_delete=models.CASCADE use cheyyum, user delete cheyyumbo order items um delete cheyyum.
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField(null=True, blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)#order create cheyyumbo order date automatically store cheyyum. auto_now_add=True use cheyyum, order create cheyyumbo order date automatically store cheyyum.

    def __str__(self):
        return self.user.username


# order items store cheyyan vendi OrderItem model undu. order items um product um quantity um price um store cheyyum.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    # 
    def __str__(self):
        return self.product.name
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    
    
