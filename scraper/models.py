from django.db import models

# Create your models here.


class AdPhoto(models.Model):
    photo = models.TextField()
    keywords = models.TextField()
