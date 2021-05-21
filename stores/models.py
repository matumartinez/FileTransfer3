from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=120, null=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name