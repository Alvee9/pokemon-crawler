from django.db import models

# Create your models here.

class Pokemon(models.Model):
    name = models.CharField(max_length=120, unique=True)
    weight = models.IntegerField()
    height = models.IntegerField()

    def __str__(self) -> str:
        return self.name

