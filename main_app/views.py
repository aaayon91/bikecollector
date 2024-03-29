from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Bike, Component, Photo
from .forms import OrderForm
import uuid
import boto3
import os

# Add the Bike class & list and view function below the imports
# class Bike:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, brand, model, year, condition):
#     self.brand = brand
#     self.model = model
#     self.year = year
#     self.condition = condition

# bikes = [
#   Bike('Peugeot', 'PGN 10', 1979, 'Used'),
#   Bike('Vitus', '787 Futural', 1987, 'NOS'),
#   Bike('Bianchi', 'Pista', 1990, 'New')
# ]

# Create your views here.
def home(request):
    # return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def bikes_index(request):
    bikes = Bike.objects.all()
    return render(request, 'bikes/index.html', { 'bikes': bikes})

def bikes_detail(request, bike_id):
  bike = Bike.objects.get(id=bike_id)
  # Get the components that the bike doesn't have
  components_bike_doesnt_have = Component.objects.exclude(id__in = bike.components.all().values_list('id'))
  # instantiate OrderForm to be renderes in the template
  order_form = OrderForm()
  t = 0
  for order in bike.order_set.all():
      t = t + order.total
  return render(request, 'bikes/detail.html', { 
      'bike': bike, 'order_form': order_form,
      # Add the components to be displayed
      'components': components_bike_doesnt_have,
      't': t
      })

def add_order(request, bike_id):
    # create a ModelForm instance using the data in request.POST
    form = OrderForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't send the form to the db until it has the bike_id assigned
        new_order = form.save(commit=False)
        new_order.bike_id = bike_id
        new_order.save()
    return redirect('detail', bike_id=bike_id)

def assoc_component(request, bike_id, component_id):
    # Note that you can pass a toy's id instead of the whole toy object
    Bike.objects.get(id=bike_id).components.add(component_id)
    return redirect('detail', bike_id=bike_id)

def add_photo(request, bike_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, bike_id=bike_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', bike_id=bike_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


# Class-Based Views
class BikeCreate(CreateView):
    model = Bike
    fields = ['brand', 'model', 'year', 'condition']

    # This inherited method is called when a
    # valid bike form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the bike
        # Let the CreateView do its job as usual
        return super().form_valid(form)

class BikeUpdate(UpdateView):
    model = Bike
    fields = '__all__'

class BikeDelete(DeleteView):
    model = Bike
    success_url = '/bikes/'

class ComponentList(ListView):
    model = Component

class ComponentDetail(DetailView):
    model = Component

class ComponentCreate(CreateView):
    model = Component
    fields = '__all__'

class ComponentUpdate(UpdateView):
    model = Component
    fields = ['type', 'functionality']

class ComponentDelete(DeleteView):
    model = Component
    success_url = '/components/'