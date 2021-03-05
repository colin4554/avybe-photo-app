from django.db import models

# photo model
class Photo(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', default='default.jpg')

    # timestamp for when photo is uploaded
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # just returns to home page, direct urls are handled through edit view
    def get_absolute_url(self):
        return '/app'
