from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class Product_Details(models.Model):
    product_name = models.CharField(max_length=50)
    details = models.TextField()
    price = models.FloatField()
    available = models.BooleanField(default=True)
    quantity = models.IntegerField()
    item_type = models.CharField(max_length=50)  
    created_at = models.DateField(default=now)

    def __str__(self):
        return self.product_name

def get_reach_date():
    return now().date() + timedelta(days=7)

class Cart(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)  
    delivery_address = models.JSONField()
    ordered_date = models.DateField(default=now)
    reach_date = models.DateField(default=get_reach_date)
    product = models.ForeignKey(Product_Details, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Cart of {self.username.username} - {self.product.product_name}"

class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product_Details, on_delete=models.CASCADE)  
    message = models.TextField()
    comm_date = models.DateField(default=now)

    def __str__(self):
        return f"{self.username.username} - {self.product.product_name} - {self.message[:30]}..."  

class Message(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    message_date = models.DateField(default=now)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.user_name.username} - {self.email}"

class Favorite_items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product_Details, on_delete=models.CASCADE)  
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_items = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user.username}'s Profile"
