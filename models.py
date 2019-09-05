from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Book(models.Model):
    img = models.ImageField(upload_to="gallery")
    title = models.TextField()
    desc = models.TextField()
    price = models.FloatField()
    def __str__(self):
        return self.title  

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')      
    def __str__(self):
        return f'{self.user.username} profile'

class SignUp(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email        

    
              