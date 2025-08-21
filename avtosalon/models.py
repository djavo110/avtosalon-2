from django.db import models
from django.urls import reverse

# Create your models here.

class Avtosalon(models.Model):
    title = models.CharField(max_length=100)
    context = models.TextField(blank=True)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photo/%Y/%m/%d/')

    def __str__(self):
        return self.title
    
class Brend(models.Model):
    title = models.CharField(max_length=100)
    context = models.TextField(blank=True)
    created_ed = models.DateTimeField(auto_now_add=True)
    updated_ed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Car(models.Model):
    salon = models.ForeignKey(Avtosalon, on_delete=models.CASCADE)
    brend = models.ForeignKey(Brend, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField()
    color = models.CharField(max_length=30)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    context = models.TextField(blank=True)


    def __str__(self):
        return f"{self.brend} {self.model} {self.year} - {self.color} - {self.price} $"
    
    def get_absolute_url(self):
        return reverse("detail_car", args=[str(self.id)])