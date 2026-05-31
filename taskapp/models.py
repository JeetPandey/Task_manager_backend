from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20,unique=True)
    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    description = models.TextField()
    due_date = models.DateField()
    image = models.ImageField(upload_to='task_images/',blank=True,null=True)
    position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.task.name}"
    
    
