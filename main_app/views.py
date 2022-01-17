from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Bike, Component
from .forms import OrderForm

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

class BikeCreate(CreateView):
    model = Bike
    fields = ['brand', 'model', 'year', 'condition']

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