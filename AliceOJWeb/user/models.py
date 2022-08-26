from django.db import models

# Create your models here.


class User(models.Model):
    
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    accepted_count = models.PositiveIntegerField(default=0)
    
    def __str__(self) -> str:
        return self.user.username
