from django.forms import ModelForm
from .models import Photo

# photo form used to update/add photo
class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['name', 'image']
