from django.db import models

class ImageModel(models.Model):
    image = models.ImageField('img', upload_to = 'uploadedfiles')