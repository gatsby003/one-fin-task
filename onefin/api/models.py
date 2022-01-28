import uuid
from django.db import models

# Create your models here.
class AppUser(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Collection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(AppUser, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    movies = models.JSONField()
    

    def __str__(self):
        return self.title

