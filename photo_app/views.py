from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, View
from django.contrib import messages

from .models import Photo
from.forms import PhotoForm

# home view displays photos
class Home(ListView):
    model = Photo
    template_name = 'photo_app/index.html'
    # only display up to 9 most recent uploads
    queryset = Photo.objects.order_by('-date_added')[:9]

# allows use to submit a form and add a photo
class Add(CreateView):
    model = Photo
    template_name = 'photo_app/add.html'
    fields = '__all__'


# search page to find an elment to edit, also returns errors if element does not exit
class Search(View):
    model = Photo
    template_name = 'photo_app/search.html'

    def get(self, request):
        name = request.GET.get('name')
        id = request.GET.get('id')

        # if get isn't from a submitted form, show blank form
        if name is None or id is None:
            return render(request, self.template_name)
        else:

            if len(name) > 0 and len(id) > 0:
                try:
                    photo = Photo.objects.filter(name=name, id=id)[0]
                except:
                    messages.error(request, 'No item exists with name {:s} and id {:s}'.format(name, id))
                    return render(request, self.template_name)
            elif len(name) > 0:
                try:
                    # if multiple photos have the same name, we just use the first one
                    photo = Photo.objects.filter(name=name)[0]
                except:
                    messages.error(request, 'No item exists with name {:s}'.format(name))
                    return render(request, self.template_name)
            elif len(id) > 0:
                try:
                    photo = Photo.objects.get(pk=id)
                except:
                    messages.error(request, 'No item exists with id {:s}'.format(id))
                    return render(request, self.template_name)
            else:
                messages.error(request, 'Enter a name and/or id to search for an item')
                return render(request, self.template_name)

            # redirect to edit page if photo exists
            return HttpResponseRedirect('/app/edit/%s' % photo.pk)


# displays one photo at a time so the user can edit
class Edit(View):
    model = Photo
    template_name = 'photo_app/edit.html'
    form_class = PhotoForm

    def get(self, request, pk):
        photo = Photo.objects.get(pk=pk)

        # pre-populates form with stored data
        form = self.form_class(instance=photo)

        return render(request, self.template_name, {'form': form, 'photo' : photo})

    def post(self, request, pk):
        photo = Photo.objects.get(pk=pk)

        form = self.form_class(request.POST, request.FILES, instance=photo)

        if form.is_valid():
            # updates and saves correct data
            image = form.cleaned_data['image']
            photo.image = image
            photo.save()

            name = form.cleaned_data['name']
            photo.name = name
            photo.save()

            # returns home after editing
            return HttpResponseRedirect("/app")
        return HttpResponse('failed')