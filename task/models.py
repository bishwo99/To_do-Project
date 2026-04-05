from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categories(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.title


class Task(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    due_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    is_completed = models.BooleanField(default= False) #Initially Task is pending
    categories = models.ForeignKey(Categories, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)


    def __str__(self):
        return self.title
    




