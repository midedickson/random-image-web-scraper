from django.db import models

# Create your models here.


class Ad(models.Model):
    ad_id = models.TextField()
    ad_info = models.TextField()
    ad_body = models.TextField()
